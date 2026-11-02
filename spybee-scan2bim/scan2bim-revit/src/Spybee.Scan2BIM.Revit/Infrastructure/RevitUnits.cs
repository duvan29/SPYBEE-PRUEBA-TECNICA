using Autodesk.Revit.DB;

namespace Spybee.Scan2BIM.Revit.Infrastructure
{
    /// <summary>
    /// Revit stores lengths internally in FEET. Every metre value from building.json goes through
    /// <see cref="ToInternal"/>; every value read from Revit goes through <see cref="ToMeters"/>.
    /// </summary>
    internal static class RevitUnits
    {
        public static double ToInternal(double meters) => UnitUtils.ConvertToInternalUnits(meters, UnitTypeId.Meters);

        public static double ToMeters(double internalFeet) => UnitUtils.ConvertFromInternalUnits(internalFeet, UnitTypeId.Meters);

        public static XYZ Point(double xM, double yM, double zM) => new XYZ(ToInternal(xM), ToInternal(yM), ToInternal(zM));

        public static XYZ Point(double[] xy, double zM) => Point(xy[0], xy[1], zM);
    }
}
