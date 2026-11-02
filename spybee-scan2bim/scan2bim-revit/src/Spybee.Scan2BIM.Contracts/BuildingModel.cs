using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace Spybee.Scan2BIM.Contracts
{
    // C# mirror of scan2bim-pipeline/src/scan2bim/model.py (the source of truth).
    // Units: metres, degrees. Coordinates are LOCAL (world - georef.offset), z up.
    // Types end in "Data" to avoid clashing with Revit API types (Level, Wall, Floor...).
    // Unknown JSON properties are ignored on purpose: MINOR schema versions only ADD fields.

    /// <summary>Root object of building.json.</summary>
    public sealed class BuildingModel
    {
        [JsonPropertyName("schema_version")] public string SchemaVersion { get; set; } = string.Empty;
        [JsonPropertyName("generator")] public GeneratorInfo Generator { get; set; } = new GeneratorInfo();
        [JsonPropertyName("project")] public ProjectInfo Project { get; set; } = new ProjectInfo();
        [JsonPropertyName("georef")] public GeorefData Georef { get; set; } = new GeorefData();
        [JsonPropertyName("dominant_direction_deg")] public double? DominantDirectionDeg { get; set; }
        [JsonPropertyName("levels")] public List<LevelData> Levels { get; set; } = new List<LevelData>();
        [JsonPropertyName("slabs")] public List<SlabData> Slabs { get; set; } = new List<SlabData>();
        [JsonPropertyName("walls")] public List<WallData> Walls { get; set; } = new List<WallData>();
        [JsonPropertyName("columns")] public List<ColumnData> Columns { get; set; } = new List<ColumnData>();
        [JsonPropertyName("openings")] public List<OpeningData> Openings { get; set; } = new List<OpeningData>();
        [JsonPropertyName("spaces")] public List<SpaceData> Spaces { get; set; } = new List<SpaceData>();
        [JsonPropertyName("summary")] public SummaryData? Summary { get; set; }

        /// <summary>Every element of every class, in file order.</summary>
        public IEnumerable<ElementData> AllElements()
        {
            foreach (var e in Levels) { yield return e; }
            foreach (var e in Slabs) { yield return e; }
            foreach (var e in Walls) { yield return e; }
            foreach (var e in Columns) { yield return e; }
            foreach (var e in Openings) { yield return e; }
            foreach (var e in Spaces) { yield return e; }
        }
    }

    public sealed class GeneratorInfo
    {
        [JsonPropertyName("name")] public string Name { get; set; } = "scan2bim";
        [JsonPropertyName("version")] public string Version { get; set; } = string.Empty;
        [JsonPropertyName("git")] public string? Git { get; set; }
        [JsonPropertyName("created")] public DateTimeOffset? Created { get; set; }
        [JsonPropertyName("config_hash")] public string? ConfigHash { get; set; }
    }

    public sealed class ProjectInfo
    {
        [JsonPropertyName("id")] public string Id { get; set; } = string.Empty;
        [JsonPropertyName("name")] public string Name { get; set; } = string.Empty;
        /// <summary>ISO date (yyyy-MM-dd) kept as text.</summary>
        [JsonPropertyName("capture_date")] public string? CaptureDate { get; set; }
        [JsonPropertyName("scanner")] public string? Scanner { get; set; }
        /// <summary>shell | finishing | occupied | unknown</summary>
        [JsonPropertyName("building_state")] public string BuildingState { get; set; } = "unknown";
    }

    public sealed class OffsetData
    {
        [JsonPropertyName("x")] public double X { get; set; }
        [JsonPropertyName("y")] public double Y { get; set; }
        [JsonPropertyName("z")] public double Z { get; set; }
    }

    public sealed class GeorefData
    {
        /// <summary>"EPSG:9377" (CTM12), another EPSG code, "local" or "unknown".</summary>
        [JsonPropertyName("crs")] public string Crs { get; set; } = "local";
        /// <summary>world = local + offset.</summary>
        [JsonPropertyName("offset")] public OffsetData Offset { get; set; } = new OffsetData();
        [JsonPropertyName("true_north_deg")] public double TrueNorthDeg { get; set; }
        /// <summary>orthometric | ellipsoidal | local | unknown</summary>
        [JsonPropertyName("vertical")] public string Vertical { get; set; } = "unknown";

        [JsonIgnore]
        public bool IsGeoreferenced => !string.Equals(Crs, "local", StringComparison.OrdinalIgnoreCase)
                                       && !string.Equals(Crs, "unknown", StringComparison.OrdinalIgnoreCase);
    }

    /// <summary>Fields shared by every detected element.</summary>
    public abstract class ElementData
    {
        [JsonPropertyName("id")] public string Id { get; set; } = string.Empty;
        [JsonPropertyName("confidence")] public double Confidence { get; set; }
        /// <summary>"auto" or "review".</summary>
        [JsonPropertyName("status")] public string Status { get; set; } = "auto";
        [JsonPropertyName("reasons")] public List<string> Reasons { get; set; } = new List<string>();
        [JsonPropertyName("metrics")] public Dictionary<string, JsonElement> Metrics { get; set; } = new Dictionary<string, JsonElement>();

        [JsonIgnore]
        public bool NeedsReview => string.Equals(Status, "review", StringComparison.Ordinal);
    }

    public sealed class LevelData : ElementData
    {
        [JsonPropertyName("name")] public string Name { get; set; } = string.Empty;
        [JsonPropertyName("elevation")] public double Elevation { get; set; }
    }

    public sealed class SlabData : ElementData
    {
        [JsonPropertyName("level")] public string Level { get; set; } = string.Empty;
        /// <summary>Counter-clockwise [x, y] vertices, first not repeated.</summary>
        [JsonPropertyName("outline")] public List<double[]> Outline { get; set; } = new List<double[]>();
        [JsonPropertyName("holes")] public List<List<double[]>> Holes { get; set; } = new List<List<double[]>>();
        [JsonPropertyName("top_offset")] public double TopOffset { get; set; }
        [JsonPropertyName("thickness")] public double Thickness { get; set; }
    }

    public sealed class WallData : ElementData
    {
        [JsonPropertyName("base_level")] public string BaseLevel { get; set; } = string.Empty;
        [JsonPropertyName("top_level")] public string? TopLevel { get; set; }
        /// <summary>Wall centre line: exactly two [x, y] points.</summary>
        [JsonPropertyName("axis")] public List<double[]> Axis { get; set; } = new List<double[]>();
        [JsonPropertyName("thickness")] public double Thickness { get; set; }
        [JsonPropertyName("base_offset")] public double BaseOffset { get; set; }
        /// <summary>Clear height from base to the underside of the slab above.</summary>
        [JsonPropertyName("height")] public double Height { get; set; }
        [JsonPropertyName("faces_seen")] public int FacesSeen { get; set; } = 2;
        [JsonPropertyName("material_guess")] public string MaterialGuess { get; set; } = "unknown";
    }

    public sealed class ColumnData : ElementData
    {
        [JsonPropertyName("base_level")] public string BaseLevel { get; set; } = string.Empty;
        [JsonPropertyName("top_level")] public string? TopLevel { get; set; }
        [JsonPropertyName("center")] public double[] Center { get; set; } = new double[2];
        /// <summary>"rect" (size = [b, h]) or "circle" (size = [diameter]).</summary>
        [JsonPropertyName("shape")] public string Shape { get; set; } = "rect";
        [JsonPropertyName("size")] public List<double> Size { get; set; } = new List<double>();
        [JsonPropertyName("rotation_deg")] public double RotationDeg { get; set; }
        [JsonPropertyName("embedded_in")] public string? EmbeddedIn { get; set; }
    }

    public sealed class OpeningData : ElementData
    {
        [JsonPropertyName("host")] public string Host { get; set; } = string.Empty;
        /// <summary>door | window | opening</summary>
        [JsonPropertyName("kind")] public string Kind { get; set; } = "opening";
        /// <summary>Distance from host axis[0] to the opening edge closest to axis[0].</summary>
        [JsonPropertyName("offset_along")] public double OffsetAlong { get; set; }
        [JsonPropertyName("width")] public double Width { get; set; }
        [JsonPropertyName("height")] public double Height { get; set; }
        /// <summary>Sill height above the host wall base.</summary>
        [JsonPropertyName("sill")] public double Sill { get; set; }
    }

    public sealed class SpaceData : ElementData
    {
        [JsonPropertyName("level")] public string Level { get; set; } = string.Empty;
        [JsonPropertyName("polygon")] public List<double[]> Polygon { get; set; } = new List<double[]>();
        [JsonPropertyName("seed")] public double[] Seed { get; set; } = new double[2];
        [JsonPropertyName("area")] public double Area { get; set; }
        [JsonPropertyName("name_guess")] public string? NameGuess { get; set; }
    }

    public sealed class SummaryData
    {
        [JsonPropertyName("counts")] public Dictionary<string, int> Counts { get; set; } = new Dictionary<string, int>();
        [JsonPropertyName("review_counts")] public Dictionary<string, int> ReviewCounts { get; set; } = new Dictionary<string, int>();
        [JsonPropertyName("timings_s")] public Dictionary<string, double> TimingsS { get; set; } = new Dictionary<string, double>();
    }
}
