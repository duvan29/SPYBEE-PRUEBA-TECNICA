using System;
using System.Globalization;
using Spybee.Scan2BIM.Contracts;

namespace Spybee.Scan2BIM.Core
{
    /// <summary>Names of the Revit types the add-in creates. Always culture-invariant.</summary>
    public static class TypeNaming
    {
        public const string Prefix = "Spybee";

        public static string Wall(double thicknessM) => $"{Prefix} Wall {Cm(thicknessM)} cm";

        public static string Floor(double thicknessM) => $"{Prefix} Floor {Cm(thicknessM)} cm";

        public static string RectColumn(double bM, double hM) => $"{Prefix} Column {Cm(bM)}x{Cm(hM)} cm";

        public static string RoundColumn(double diameterM) => $"{Prefix} Column D{Cm(diameterM)} cm";

        /// <summary>Whole centimetres, invariant culture ("15", never "15,0").</summary>
        public static string Cm(double meters) =>
            Math.Round(meters * 100.0, MidpointRounding.AwayFromZero).ToString("0", CultureInfo.InvariantCulture);
    }

    /// <summary>Text written to the Revit "Comments" parameter so modellers see AUTO / REVIEW.</summary>
    public static class ReviewLabel
    {
        public const string AutoTag = "AUTO";
        public const string ReviewTag = "REVIEW";

        public static string For(ElementData element)
        {
            string confidence = element.Confidence.ToString("0.00", CultureInfo.InvariantCulture);
            if (!element.NeedsReview) { return $"{AutoTag} conf={confidence}"; }
            string reasons = element.Reasons.Count == 0 ? "low_confidence" : string.Join(",", element.Reasons);
            return $"{ReviewTag} conf={confidence} reasons={reasons}";
        }

        public static bool IsReview(string? comment) =>
            comment != null && comment.StartsWith(ReviewTag, StringComparison.Ordinal);
    }
}
