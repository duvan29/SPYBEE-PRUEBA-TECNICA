using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Spybee.Scan2BIM.Contracts;
using Spybee.Scan2BIM.Core;
using Spybee.Scan2BIM.Revit.Infrastructure;

namespace Spybee.Scan2BIM.Revit.Commands
{
    /// <summary>
    /// "Spybee: Export corrections" — compares the reviewed Revit model with the original building.json
    /// and writes corrections.json next to it (task T7.4). v1 covers WALLS; other classes are TODO.
    /// </summary>
    [Transaction(TransactionMode.ReadOnly)]
    public sealed class ExportCorrectionsCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            Document? doc = commandData.Application.ActiveUIDocument?.Document;
            if (doc == null) { message = "Open the reviewed Revit project first."; return Result.Failed; }

            string? path = FileDialogs.PickBuildingJson();
            if (path == null) { return Result.Cancelled; }

            try
            {
                BuildingModel original = BuildingJson.Load(path);
                List<ObservedWall> walls = new FilteredElementCollector(doc)
                    .OfClass(typeof(Wall))
                    .Cast<Wall>()
                    .Select(ToObserved)
                    .Where(w => w != null)
                    .Select(w => w!)
                    .ToList();

                CorrectionsReport report = CorrectionsDiff.CompareWalls(original, walls);
                report.Source = Path.GetFileName(path);
                report.Rvt = doc.Title;
                string output = Path.Combine(Path.GetDirectoryName(path) ?? ".", "corrections.json");
                File.WriteAllText(output, report.ToJson());

                ClassSummary s = report.Summary["walls"];
                string text =
                    $"Walls: {s.Unchanged} unchanged, {s.Modified} modified, {s.Deleted} deleted, {s.Created} created.{Environment.NewLine}" +
                    $"Correction rate: {s.CorrectionRate:P0}; silent errors (AUTO but fixed): {s.SilentErrors}{Environment.NewLine}" +
                    $"Written to {output}";
                Log.Info(text);
                TaskDialog.Show("Spybee Scan2BIM", text);
                return Result.Succeeded;
            }
            catch (Exception ex) when (ex is ContractException || ex is IOException || ex is UnauthorizedAccessException)
            {
                Log.Error("Export corrections failed", ex);
                message = ex.Message;
                return Result.Failed;
            }
        }

        private static ObservedWall? ToObserved(Wall wall)
        {
            if (!(wall.Location is LocationCurve location) || !(location.Curve is Line line)) { return null; }
            XYZ a = line.GetEndPoint(0);
            XYZ b = line.GetEndPoint(1);
            BoundingBoxXYZ? box = wall.get_BoundingBox(null);
            string? mark = wall.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)?.AsString();
            return new ObservedWall
            {
                SpybeeId = string.IsNullOrWhiteSpace(mark) ? null : mark,
                RevitId = ElementIdValue(wall.Id),
                Axis = new List<double[]>
                {
                    new[] { RevitUnits.ToMeters(a.X), RevitUnits.ToMeters(a.Y) },
                    new[] { RevitUnits.ToMeters(b.X), RevitUnits.ToMeters(b.Y) },
                },
                Thickness = RevitUnits.ToMeters(wall.Width),
                Height = box == null ? 0.0 : RevitUnits.ToMeters(box.Max.Z - box.Min.Z),
            };
        }

        private static long ElementIdValue(ElementId id)
        {
#if REVIT2021 || REVIT2022 || REVIT2023
            return id.IntegerValue;
#else
            return id.Value; // ElementId.Value (Int64) since Revit 2024
#endif
        }
    }
}
