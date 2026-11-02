using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;
using Spybee.Scan2BIM.Contracts;
using Spybee.Scan2BIM.Core;
using Spybee.Scan2BIM.Revit.Infrastructure;

namespace Spybee.Scan2BIM.Revit.Build
{
    /// <summary>
    /// Creates native Revit elements from a validated <see cref="BuildingModel"/>.
    /// No UI code here (keeps it reusable in APS Design Automation later).
    /// Must run inside ONE open transaction.
    ///
    /// Status: levels, walls, floors, review marking, views, shared coordinates = implemented (T5.2-T5.4,
    /// NOT yet compiled against Revit - first build happens in task T0.4).
    /// Columns, openings, rooms = TODO (T6.4).
    /// </summary>
    internal sealed class ModelBuilder
    {
        private const double LevelMatchToleranceM = 0.01;

        private readonly Document _doc;
        private readonly BuildingModel _model;
        private readonly GenerationReport _report;
        private readonly TypeFactory _types;
        private readonly Dictionary<string, Level> _levels = new Dictionary<string, Level>(StringComparer.Ordinal);
        private readonly Dictionary<string, double> _levelElevationM = new Dictionary<string, double>(StringComparer.Ordinal);
        private readonly Dictionary<string, Wall> _walls = new Dictionary<string, Wall>(StringComparer.Ordinal);
        private readonly List<CreatedElement> _created = new List<CreatedElement>();

        public ModelBuilder(Document doc, BuildingModel model, GenerationReport report)
        {
            _doc = doc;
            _model = model;
            _report = report;
            _types = new TypeFactory(doc);
        }

        public void Run()
        {
            CreateLevels();
            CreateWalls();
            CreateFloors();
            _doc.Regenerate();
            CreateColumns();   // TODO(T6.4)
            CreateOpenings();  // TODO(T6.4)
            CreateRooms();     // TODO(T6.4)
            ReviewMarker.Apply(_doc, _created, _levels.Values);
            ApplySharedCoordinates();
        }

        // ---------------------------------------------------------------- levels
        private void CreateLevels()
        {
            List<Level> existing = new FilteredElementCollector(_doc).OfClass(typeof(Level)).Cast<Level>().ToList();
            double tolerance = RevitUnits.ToInternal(LevelMatchToleranceM);
            foreach (LevelData data in _model.Levels.OrderBy(l => l.Elevation))
            {
                double elevation = RevitUnits.ToInternal(data.Elevation);
                // Reuse template levels ("Level 1", "Nivel 1"...) at the same elevation instead of duplicating.
                Level level = existing.FirstOrDefault(l => Math.Abs(l.ProjectElevation - elevation) < tolerance)
                              ?? Level.Create(_doc, elevation);
                TryRename(level, data.Name);
                _levels[data.Id] = level;
                _levelElevationM[data.Id] = data.Elevation;
                _report.Created("levels");
            }
        }

        private static void TryRename(Element element, string name)
        {
            try
            {
                element.Name = name;
            }
            catch (Autodesk.Revit.Exceptions.ArgumentException)
            {
                element.Name = $"{name} ({element.Id})"; // names must be unique in Revit
            }
        }

        // ---------------------------------------------------------------- walls
        private void CreateWalls()
        {
            double shortCurve = _doc.Application.ShortCurveTolerance;
            foreach (WallData data in _model.Walls)
            {
                if (!_levels.TryGetValue(data.BaseLevel, out Level baseLevel))
                {
                    _report.Fail(data.Id, $"unknown base level {data.BaseLevel}");
                    continue;
                }
                double baseElevationM = _levelElevationM[data.BaseLevel];
                XYZ start = RevitUnits.Point(data.Axis[0], baseElevationM);
                XYZ end = RevitUnits.Point(data.Axis[1], baseElevationM);
                if (start.DistanceTo(end) < shortCurve)
                {
                    _report.Fail(data.Id, "axis shorter than Revit's short curve tolerance");
                    continue;
                }
                try
                {
                    WallType type = _types.GetWallType(data.Thickness);
                    Wall wall = Wall.Create(_doc, Line.CreateBound(start, end), type.Id, baseLevel.Id,
                        RevitUnits.ToInternal(data.Height), RevitUnits.ToInternal(data.BaseOffset), false, false);

                    // The location line must be the wall CENTRE LINE (0 = Wall Centerline). Report, don't "fix":
                    // changing it after creation would shift the wall by half its thickness.
                    Parameter? keyRef = wall.get_Parameter(BuiltInParameter.WALL_KEY_REF_PARAM);
                    if (keyRef != null && keyRef.AsInteger() != 0)
                    {
                        _report.Fail(data.Id, "wall location line is not 'Wall Centerline' - check the project template");
                    }

                    if (data.TopLevel != null && _levels.TryGetValue(data.TopLevel, out Level topLevel))
                    {
                        double topOffsetM = baseElevationM + data.BaseOffset + data.Height - _levelElevationM[data.TopLevel];
                        wall.get_Parameter(BuiltInParameter.WALL_HEIGHT_TYPE)?.Set(topLevel.Id);
                        wall.get_Parameter(BuiltInParameter.WALL_TOP_OFFSET)?.Set(RevitUnits.ToInternal(topOffsetM));
                    }
                    _walls[data.Id] = wall;
                    _created.Add(new CreatedElement(wall.Id, data, "walls"));
                    _report.Created("walls");
                }
                catch (Autodesk.Revit.Exceptions.ApplicationException ex)
                {
                    _report.Fail(data.Id, ex.Message);
                }
            }
        }

        // ---------------------------------------------------------------- floors (Revit 2022+ API)
        private void CreateFloors()
        {
            foreach (SlabData data in _model.Slabs)
            {
                if (!_levels.TryGetValue(data.Level, out Level level))
                {
                    _report.Fail(data.Id, $"unknown level {data.Level}");
                    continue;
                }
                try
                {
                    double zM = _levelElevationM[data.Level];
                    var loops = new List<CurveLoop> { ToCurveLoop(data.Outline, zM) };
                    loops.AddRange(data.Holes.Select(hole => ToCurveLoop(hole, zM)));
                    FloorType type = _types.GetFloorType(data.Thickness);
                    Floor floor = Floor.Create(_doc, loops, type.Id, level.Id);
                    floor.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)?.Set(RevitUnits.ToInternal(data.TopOffset));
                    _created.Add(new CreatedElement(floor.Id, data, "floors"));
                    _report.Created("floors");
                }
                catch (Exception ex) when (ex is Autodesk.Revit.Exceptions.ApplicationException || ex is ArgumentException)
                {
                    _report.Fail(data.Id, ex.Message);
                }
            }
        }

        private CurveLoop ToCurveLoop(List<double[]> polygon, double zM)
        {
            double shortCurve = _doc.Application.ShortCurveTolerance;
            var points = new List<XYZ>();
            foreach (double[] p in polygon)
            {
                XYZ point = RevitUnits.Point(p, zM);
                if (points.Count == 0 || points[points.Count - 1].DistanceTo(point) >= shortCurve) { points.Add(point); }
            }
            if (points.Count > 2 && points[0].DistanceTo(points[points.Count - 1]) < shortCurve) { points.RemoveAt(points.Count - 1); }
            if (points.Count < 3) { throw new ArgumentException("Polygon has fewer than 3 distinct vertices."); }

            var loop = new CurveLoop();
            for (int i = 0; i < points.Count; i++)
            {
                loop.Append(Line.CreateBound(points[i], points[(i + 1) % points.Count]));
            }
            return loop;
        }

        // ---------------------------------------------------------------- TODO (T6.4)
        private void CreateColumns()
        {
            // TODO(T6.4): structural column family (rect/circle) -> duplicate type per section via TypeNaming,
            // NewFamilyInstance(point, symbol, baseLevel, StructuralType.Column), FAMILY_TOP_LEVEL_PARAM,
            // rotation with ElementTransformUtils.RotateElement. See docs/REVIT_ADDIN_SPEC.md §5.
            foreach (ColumnData data in _model.Columns) { _report.Fail(data.Id, "columns not implemented yet (T6.4)"); }
        }

        private void CreateOpenings()
        {
            // TODO(T6.4): v1 = doc.Create.NewOpening(wall, bottomLeft, topRight) using AxisMath.PointAlong
            // on the host axis. See docs/REVIT_ADDIN_SPEC.md §6.
            foreach (OpeningData data in _model.Openings) { _report.Fail(data.Id, "openings not implemented yet (T6.4)"); }
        }

        private void CreateRooms()
        {
            // TODO(T6.4): doc.Create.NewRoom(level, new UV(x, y)) at each space seed (after Regenerate).
            foreach (SpaceData data in _model.Spaces) { _report.Fail(data.Id, "rooms not implemented yet (T6.4)"); }
        }

        // ---------------------------------------------------------------- georeference (T5.4)
        private void ApplySharedCoordinates()
        {
            if (!_model.Georef.IsGeoreferenced) { return; }
            OffsetData o = _model.Georef.Offset;
            // Internal origin (local 0,0,0) == real-world offset. Angle 0: the cloud is never rotated (ADR-0004).
            // VERIFY the sign convention with a control point the first time a rotated project is used.
            var position = new ProjectPosition(
                RevitUnits.ToInternal(o.X),
                RevitUnits.ToInternal(o.Y),
                RevitUnits.ToInternal(o.Z),
                Units.DegreesToRadians(_model.Georef.TrueNorthDeg));
            _doc.ActiveProjectLocation.SetProjectPosition(XYZ.Zero, position);
            Log.Info($"Shared coordinates set: {_model.Georef.Crs} offset ({o.X}, {o.Y}, {o.Z})");
        }
    }
}
