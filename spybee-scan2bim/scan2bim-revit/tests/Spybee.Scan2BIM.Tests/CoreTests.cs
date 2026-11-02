using System;
using System.Collections.Generic;
using System.Globalization;
using Spybee.Scan2BIM.Contracts;
using Spybee.Scan2BIM.Core;
using Xunit;

namespace Spybee.Scan2BIM.Tests
{
    public class CoreTests
    {
        private static List<double[]> Axis(double x0, double y0, double x1, double y1) =>
            new List<double[]> { new[] { x0, y0 }, new[] { x1, y1 } };

        [Fact]
        public void Axis_length_direction_and_point_along()
        {
            var axis = Axis(0, 0, 3, 4);
            Assert.Equal(5.0, AxisMath.Length(axis), 9);
            var (x, y) = AxisMath.PointAlong(axis, 2.5);
            Assert.Equal(1.5, x, 9);
            Assert.Equal(2.0, y, 9);
        }

        [Fact]
        public void Endpoint_shift_ignores_orientation()
        {
            Assert.Equal(0.0, AxisMath.EndpointShift(Axis(0, 0, 5, 0), Axis(5, 0, 0, 0)), 9);
            Assert.Equal(0.1, AxisMath.EndpointShift(Axis(0, 0, 5, 0), Axis(0, 0.1, 5, 0.1)), 9);
        }

        [Fact]
        public void Units_round_trip()
        {
            Assert.Equal(1.0, Units.FeetToMeters(Units.MetersToFeet(1.0)), 12);
            Assert.Equal(3.28084, Units.MetersToFeet(1.0), 5);
        }

        [Fact]
        public void Names_and_labels_are_culture_invariant_under_es_CO()
        {
            CultureInfo previous = CultureInfo.CurrentCulture;
            try
            {
                CultureInfo.CurrentCulture = new CultureInfo("es-CO"); // decimal comma
                Assert.Equal("Spybee Wall 15 cm", TypeNaming.Wall(0.15));
                Assert.Equal("Spybee Column 30x50 cm", TypeNaming.RectColumn(0.30, 0.50));

                var wall = new WallData { Id = "W-0001", Confidence = 0.62, Status = "review", Reasons = new List<string> { "one_face" } };
                Assert.Equal("REVIEW conf=0.62 reasons=one_face", ReviewLabel.For(wall));
                Assert.True(ReviewLabel.IsReview(ReviewLabel.For(wall)));

                var ok = new WallData { Id = "W-0002", Confidence = 0.93, Status = "auto" };
                Assert.Equal("AUTO conf=0.93", ReviewLabel.For(ok));
            }
            finally
            {
                CultureInfo.CurrentCulture = previous;
            }
        }
    }
}
