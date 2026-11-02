using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Spybee.Scan2BIM.Contracts;
using Spybee.Scan2BIM.Core;
using Xunit;

namespace Spybee.Scan2BIM.Tests
{
    public class CorrectionsDiffTests
    {
        private static BuildingModel Example() =>
            BuildingJson.Load(Path.Combine(AppContext.BaseDirectory, "Fixtures", "building.example.json"));

        private static ObservedWall Observe(WallData w) => new ObservedWall
        {
            SpybeeId = w.Id,
            Axis = w.Axis.Select(p => new[] { p[0], p[1] }).ToList(),
            Thickness = w.Thickness,
            Height = w.Height,
        };

        [Fact]
        public void Untouched_model_has_zero_correction_rate()
        {
            BuildingModel model = Example();
            CorrectionsReport report = CorrectionsDiff.CompareWalls(model, model.Walls.Select(Observe));
            ClassSummary s = report.Summary["walls"];
            Assert.Equal(model.Walls.Count, s.Unchanged);
            Assert.Equal(0.0, s.CorrectionRate);
        }

        [Fact]
        public void Detects_modified_deleted_and_created_walls()
        {
            BuildingModel model = Example();
            var observed = model.Walls.Select(Observe).ToList();
            observed[0].Axis[0][1] += 0.06;                // moved 6 cm   -> modified
            observed[1].Thickness = 0.12;                  // retyped      -> modified
            observed.RemoveAt(2);                          // deleted
            observed.Add(new ObservedWall                  // created by the modeller (no Spybee id)
            {
                Axis = new List<double[]> { new[] { 0.0, 0.0 }, new[] { 1.0, 0.0 } },
                Thickness = 0.10,
                Height = 2.4,
            });

            CorrectionsReport report = CorrectionsDiff.CompareWalls(model, observed);
            ClassSummary s = report.Summary["walls"];

            Assert.Equal(2, s.Modified);
            Assert.Equal(1, s.Deleted);
            Assert.Equal(1, s.Created);
            Assert.Equal(model.Walls.Count - 3, s.Unchanged);
            Assert.Equal(3, s.SilentErrors); // all example walls are "auto"
            Assert.Equal(4.0 / (model.Walls.Count + 1), s.CorrectionRate, 9);
            Assert.Contains("\"correction_rate\"", report.ToJson());
        }
    }
}
