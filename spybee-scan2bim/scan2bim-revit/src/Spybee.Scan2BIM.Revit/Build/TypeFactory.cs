using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;
using Spybee.Scan2BIM.Core;
using Spybee.Scan2BIM.Revit.Infrastructure;

namespace Spybee.Scan2BIM.Revit.Build
{
    /// <summary>
    /// Finds or creates single-layer generic types by thickness ("Spybee Wall 15 cm"). Types are
    /// cached per run. Must be called inside an open transaction.
    /// </summary>
    internal sealed class TypeFactory
    {
        private readonly Document _doc;
        private readonly Dictionary<string, WallType> _wallTypes = new Dictionary<string, WallType>(StringComparer.Ordinal);
        private readonly Dictionary<string, FloorType> _floorTypes = new Dictionary<string, FloorType>(StringComparer.Ordinal);

        public TypeFactory(Document doc)
        {
            _doc = doc;
        }

        public WallType GetWallType(double thicknessM)
        {
            string name = TypeNaming.Wall(thicknessM);
            if (_wallTypes.TryGetValue(name, out WallType cached)) { return cached; }

            WallType? type = new FilteredElementCollector(_doc)
                .OfClass(typeof(WallType))
                .Cast<WallType>()
                .FirstOrDefault(t => t.Name == name);
            if (type == null)
            {
                WallType baseType = new FilteredElementCollector(_doc)
                    .OfClass(typeof(WallType))
                    .Cast<WallType>()
                    .FirstOrDefault(t => t.Kind == WallKind.Basic)
                    ?? throw new InvalidOperationException("The project has no basic wall type to duplicate. Use a project template with walls.");
                type = (WallType)baseType.Duplicate(name);
                type.SetCompoundStructure(CompoundStructure.CreateSingleLayerCompoundStructure(
                    MaterialFunctionAssignment.Structure, RevitUnits.ToInternal(thicknessM), ElementId.InvalidElementId));
            }
            _wallTypes[name] = type;
            return type;
        }

        public FloorType GetFloorType(double thicknessM)
        {
            string name = TypeNaming.Floor(thicknessM);
            if (_floorTypes.TryGetValue(name, out FloorType cached)) { return cached; }

            FloorType? type = new FilteredElementCollector(_doc)
                .OfClass(typeof(FloorType))
                .Cast<FloorType>()
                .FirstOrDefault(t => t.Name == name);
            if (type == null)
            {
                FloorType baseType = new FilteredElementCollector(_doc)
                    .OfClass(typeof(FloorType))
                    .Cast<FloorType>()
                    .FirstOrDefault(t => !t.IsFoundationSlab)
                    ?? throw new InvalidOperationException("The project has no floor type to duplicate. Use a project template with floors.");
                type = (FloorType)baseType.Duplicate(name);
                type.SetCompoundStructure(CompoundStructure.CreateSingleLayerCompoundStructure(
                    MaterialFunctionAssignment.Structure, RevitUnits.ToInternal(thicknessM), ElementId.InvalidElementId));
            }
            _floorTypes[name] = type;
            return type;
        }
    }
}
