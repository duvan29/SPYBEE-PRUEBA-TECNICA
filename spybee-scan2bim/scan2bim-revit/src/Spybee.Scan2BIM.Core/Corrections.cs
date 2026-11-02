using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Serialization;
using Spybee.Scan2BIM.Contracts;

namespace Spybee.Scan2BIM.Core
{
    /// <summary>A wall as it exists in the Revit model after the modeller's review (metres, local).</summary>
    public sealed class ObservedWall
    {
        /// <summary>Spybee id read from the Mark parameter; null for walls the modeller created.</summary>
        public string? SpybeeId { get; set; }
        public long RevitId { get; set; }
        public List<double[]> Axis { get; set; } = new List<double[]>();
        public double Thickness { get; set; }
        public double Height { get; set; }
    }

    public sealed class CorrectionItem
    {
        [JsonPropertyName("id")] public string? Id { get; set; }
        [JsonPropertyName("class")] public string Class { get; set; } = string.Empty;
        /// <summary>unchanged | modified | deleted | created</summary>
        [JsonPropertyName("action")] public string Action { get; set; } = string.Empty;
        [JsonPropertyName("revit_id")] public long? RevitId { get; set; }
        [JsonPropertyName("was_review")] public bool WasReview { get; set; }
        [JsonPropertyName("changes")] public Dictionary<string, double> Changes { get; set; } = new Dictionary<string, double>();
    }

    public sealed class ClassSummary
    {
        [JsonPropertyName("total_generated")] public int TotalGenerated { get; set; }
        [JsonPropertyName("unchanged")] public int Unchanged { get; set; }
        [JsonPropertyName("modified")] public int Modified { get; set; }
        [JsonPropertyName("deleted")] public int Deleted { get; set; }
        [JsonPropertyName("created")] public int Created { get; set; }
        /// <summary>Elements flagged "auto" that the modeller still had to fix (silent errors).</summary>
        [JsonPropertyName("silent_errors")] public int SilentErrors { get; set; }

        /// <summary>(modified + deleted + created) / (generated + created).</summary>
        [JsonPropertyName("correction_rate")]
        public double CorrectionRate
        {
            get
            {
                int denominator = TotalGenerated + Created;
                return denominator == 0 ? 0.0 : (double)(Modified + Deleted + Created) / denominator;
            }
        }
    }

    public sealed class CorrectionsReport
    {
        [JsonPropertyName("source")] public string Source { get; set; } = "building.json";
        [JsonPropertyName("rvt")] public string? Rvt { get; set; }
        [JsonPropertyName("exported")] public DateTimeOffset Exported { get; set; } = DateTimeOffset.Now;
        [JsonPropertyName("summary")] public Dictionary<string, ClassSummary> Summary { get; set; } = new Dictionary<string, ClassSummary>();
        [JsonPropertyName("items")] public List<CorrectionItem> Items { get; set; } = new List<CorrectionItem>();

        public string ToJson() => JsonSerializer.Serialize(this, new JsonSerializerOptions { WriteIndented = true });
    }

    /// <summary>Tolerances below which a change is considered noise, not a correction.</summary>
    public sealed class DiffTolerances
    {
        public double AxisShiftM { get; set; } = 0.02;
        public double ThicknessM { get; set; } = 0.005;
        public double HeightM { get; set; } = 0.02;
    }

    /// <summary>Compares the generated model with what the modeller left in Revit (task T7.4).</summary>
    public static class CorrectionsDiff
    {
        public static CorrectionsReport CompareWalls(
            BuildingModel original, IEnumerable<ObservedWall> observed, DiffTolerances? tolerances = null)
        {
            var tol = tolerances ?? new DiffTolerances();
            var report = new CorrectionsReport();
            var summary = new ClassSummary { TotalGenerated = original.Walls.Count };
            report.Summary["walls"] = summary;

            var byId = new Dictionary<string, ObservedWall>(StringComparer.Ordinal);
            var created = new List<ObservedWall>();
            foreach (var wall in observed)
            {
                if (string.IsNullOrEmpty(wall.SpybeeId)) { created.Add(wall); }
                else { byId[wall.SpybeeId!] = wall; }
            }

            foreach (var source in original.Walls)
            {
                var item = new CorrectionItem { Id = source.Id, Class = "wall", WasReview = source.NeedsReview };
                if (!byId.TryGetValue(source.Id, out var now))
                {
                    item.Action = "deleted";
                    summary.Deleted++;
                }
                else
                {
                    item.RevitId = now.RevitId;
                    double shift = AxisMath.EndpointShift(source.Axis, now.Axis);
                    if (shift > tol.AxisShiftM) { item.Changes["axis_shift_m"] = shift; }
                    if (Math.Abs(now.Thickness - source.Thickness) > tol.ThicknessM) { item.Changes["thickness_m"] = now.Thickness; }
                    if (Math.Abs(now.Height - source.Height) > tol.HeightM) { item.Changes["height_m"] = now.Height; }
                    item.Action = item.Changes.Count == 0 ? "unchanged" : "modified";
                    if (item.Changes.Count == 0) { summary.Unchanged++; } else { summary.Modified++; }
                }
                if (item.Action != "unchanged" && !source.NeedsReview) { summary.SilentErrors++; }
                report.Items.Add(item);
            }

            foreach (var wall in created)
            {
                summary.Created++;
                report.Items.Add(new CorrectionItem
                {
                    Id = null,
                    Class = "wall",
                    Action = "created",
                    RevitId = wall.RevitId,
                    Changes = new Dictionary<string, double> { ["thickness_m"] = wall.Thickness },
                });
            }
            report.Items = report.Items.OrderBy(i => i.Action, StringComparer.Ordinal).ThenBy(i => i.Id, StringComparer.Ordinal).ToList();
            return report;
        }
    }
}
