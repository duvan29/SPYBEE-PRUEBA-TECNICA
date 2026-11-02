using System;
using System.IO;
using System.Text.Json;

namespace Spybee.Scan2BIM.Contracts
{
    /// <summary>Thrown when building.json cannot be read or is incompatible.</summary>
    public sealed class ContractException : Exception
    {
        public ContractException(string message) : base(message) { }
        public ContractException(string message, Exception inner) : base(message, inner) { }
    }

    /// <summary>Version information of the contract this assembly understands.</summary>
    public static class ContractInfo
    {
        /// <summary>Must match SCHEMA_VERSION in scan2bim-pipeline/src/scan2bim/model.py.</summary>
        public const string SupportedSchemaVersion = "0.1.0";

        /// <summary>Same MAJOR version = compatible (MINOR versions only add optional fields).</summary>
        public static bool IsCompatible(string? schemaVersion)
        {
            if (string.IsNullOrWhiteSpace(schemaVersion)) { return false; }
            return string.Equals(Major(schemaVersion!), Major(SupportedSchemaVersion), StringComparison.Ordinal);
        }

        private static string Major(string version)
        {
            int dot = version.IndexOf('.');
            return dot < 0 ? version : version.Substring(0, dot);
        }
    }

    /// <summary>Reads building.json files.</summary>
    public static class BuildingJson
    {
        public static readonly JsonSerializerOptions Options = new JsonSerializerOptions
        {
            ReadCommentHandling = JsonCommentHandling.Skip,
            AllowTrailingCommas = true,
            PropertyNameCaseInsensitive = false,
        };

        public static BuildingModel Parse(string json)
        {
            BuildingModel? model;
            try
            {
                model = JsonSerializer.Deserialize<BuildingModel>(json, Options);
            }
            catch (JsonException ex)
            {
                throw new ContractException($"building.json is not valid JSON for the contract: {ex.Message}", ex);
            }
            if (model == null) { throw new ContractException("building.json is empty."); }
            if (!ContractInfo.IsCompatible(model.SchemaVersion))
            {
                throw new ContractException(
                    $"building.json schema {model.SchemaVersion} is not compatible with this add-in " +
                    $"(supports {ContractInfo.SupportedSchemaVersion}). Update the add-in or re-export.");
            }
            return model;
        }

        public static BuildingModel Load(string path)
        {
            if (!File.Exists(path)) { throw new ContractException($"File not found: {path}"); }
            return Parse(File.ReadAllText(path));
        }
    }
}
