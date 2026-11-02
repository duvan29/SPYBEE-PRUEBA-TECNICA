using System;
using System.Collections.Generic;

namespace Spybee.Scan2BIM.Core
{
    /// <summary>Unit conversions that do not need the Revit API (Revit code uses UnitUtils).</summary>
    public static class Units
    {
        public const double MetersPerFoot = 0.3048;

        public static double MetersToFeet(double meters) => meters / MetersPerFoot;

        public static double FeetToMeters(double feet) => feet * MetersPerFoot;

        public static double DegreesToRadians(double degrees) => degrees * Math.PI / 180.0;
    }

    /// <summary>2D helpers for wall axes given as two [x, y] points (metres).</summary>
    public static class AxisMath
    {
        public static double Length(IReadOnlyList<double[]> axis)
        {
            Require(axis);
            double dx = axis[1][0] - axis[0][0];
            double dy = axis[1][1] - axis[0][1];
            return Math.Sqrt((dx * dx) + (dy * dy));
        }

        /// <summary>Unit direction from axis[0] to axis[1].</summary>
        public static (double X, double Y) Direction(IReadOnlyList<double[]> axis)
        {
            double length = Length(axis);
            if (length <= 1e-9) { throw new ArgumentException("Zero-length axis.", nameof(axis)); }
            return ((axis[1][0] - axis[0][0]) / length, (axis[1][1] - axis[0][1]) / length);
        }

        /// <summary>Point at distance <paramref name="u"/> (metres) from axis[0] along the axis.</summary>
        public static (double X, double Y) PointAlong(IReadOnlyList<double[]> axis, double u)
        {
            var (dx, dy) = Direction(axis);
            return (axis[0][0] + (dx * u), axis[0][1] + (dy * u));
        }

        /// <summary>Largest endpoint displacement between two axes, ignoring orientation (metres).</summary>
        public static double EndpointShift(IReadOnlyList<double[]> a, IReadOnlyList<double[]> b)
        {
            Require(a);
            Require(b);
            double same = Math.Max(Distance(a[0], b[0]), Distance(a[1], b[1]));
            double flipped = Math.Max(Distance(a[0], b[1]), Distance(a[1], b[0]));
            return Math.Min(same, flipped);
        }

        public static double Distance(double[] p, double[] q)
        {
            double dx = q[0] - p[0];
            double dy = q[1] - p[1];
            return Math.Sqrt((dx * dx) + (dy * dy));
        }

        private static void Require(IReadOnlyList<double[]> axis)
        {
            if (axis == null || axis.Count != 2 || axis[0].Length != 2 || axis[1].Length != 2)
            {
                throw new ArgumentException("Axis must contain exactly two [x, y] points.", nameof(axis));
            }
        }
    }
}
