using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;
using Spybee.Scan2BIM.Core;

namespace Spybee.Scan2BIM.Revit.Build
{
    /// <summary>
    /// v1 review marking without shared parameters:
    ///   Mark     = Spybee id (e.g. W-0001)  -> lets "Export corrections" match elements later
    ///   Comments = "AUTO conf=0.93" | "REVIEW conf=0.62 reasons=one_face"
    /// plus a 3D view "00_REVIEW" and one plan per level where REVIEW elements are drawn in red.
    /// </summary>
    internal static class ReviewMarker
    {
        public const string ReviewViewName = "00_REVIEW";
        public const string PlanPrefix = "Spybee - ";

        public static void Apply(Document doc, IReadOnlyList<CreatedElement> created, IEnumerable<Level> levels)
        {
            foreach (CreatedElement item in created)
            {
                Element? element = doc.GetElement(item.Id);
                if (element == null) { continue; }
                SetText(element, BuiltInParameter.ALL_MODEL_MARK, item.Source.Id);
                SetText(element, BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS, ReviewLabel.For(item.Source));
            }

            OverrideGraphicSettings red = RedOverride(doc);
            var reviewIds = created.Where(c => c.Source.NeedsReview).Select(c => c.Id).ToList();

            View3D view3D = GetOrCreate3DView(doc, ReviewViewName);
            foreach (ElementId id in reviewIds) { view3D.SetElementOverrides(id, red); }

            foreach (Level level in levels)
            {
                ViewPlan? plan = GetOrCreatePlan(doc, level, PlanPrefix + level.Name);
                if (plan == null) { continue; }
                foreach (ElementId id in reviewIds) { plan.SetElementOverrides(id, red); }
            }
        }

        private static void SetText(Element element, BuiltInParameter parameter, string value)
        {
            Parameter? p = element.get_Parameter(parameter);
            if (p != null && !p.IsReadOnly && p.StorageType == StorageType.String) { p.Set(value); }
        }

        private static OverrideGraphicSettings RedOverride(Document doc)
        {
            // Look the solid fill up by property, never by name (the name is localised: "<Relleno sólido>").
            FillPatternElement? solid = new FilteredElementCollector(doc)
                .OfClass(typeof(FillPatternElement))
                .Cast<FillPatternElement>()
                .FirstOrDefault(f => f.GetFillPattern().IsSolidFill);
            var red = new Color(220, 30, 30);
            var settings = new OverrideGraphicSettings();
            settings.SetProjectionLineColor(red);
            settings.SetCutLineColor(red);
            if (solid != null)
            {
                settings.SetSurfaceForegroundPatternId(solid.Id);
                settings.SetSurfaceForegroundPatternColor(new Color(255, 120, 120));
                settings.SetCutForegroundPatternId(solid.Id);
                settings.SetCutForegroundPatternColor(new Color(255, 120, 120));
            }
            return settings;
        }

        private static View3D GetOrCreate3DView(Document doc, string name)
        {
            View3D? existing = new FilteredElementCollector(doc)
                .OfClass(typeof(View3D))
                .Cast<View3D>()
                .FirstOrDefault(v => !v.IsTemplate && v.Name == name);
            if (existing != null) { return existing; }
            ViewFamilyType type = new FilteredElementCollector(doc)
                .OfClass(typeof(ViewFamilyType))
                .Cast<ViewFamilyType>()
                .First(v => v.ViewFamily == ViewFamily.ThreeDimensional);
            View3D view = View3D.CreateIsometric(doc, type.Id);
            view.Name = name;
            return view;
        }

        private static ViewPlan? GetOrCreatePlan(Document doc, Level level, string name)
        {
            ViewPlan? existing = new FilteredElementCollector(doc)
                .OfClass(typeof(ViewPlan))
                .Cast<ViewPlan>()
                .FirstOrDefault(v => !v.IsTemplate && v.Name == name);
            if (existing != null) { return existing; }
            ViewFamilyType? type = new FilteredElementCollector(doc)
                .OfClass(typeof(ViewFamilyType))
                .Cast<ViewFamilyType>()
                .FirstOrDefault(v => v.ViewFamily == ViewFamily.FloorPlan);
            if (type == null) { return null; }
            ViewPlan plan = ViewPlan.Create(doc, type.Id, level.Id);
            plan.Name = name;
            return plan;
        }
    }
}
