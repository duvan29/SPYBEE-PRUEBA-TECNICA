using System;
using System.IO;
using System.Linq;
using System.Text.Json;
using Spybee.Scan2BIM.Contracts;
using Xunit;

namespace Spybee.Scan2BIM.Tests
{
    public class ContractTests
    {
        private static string Fixture(string name) => Path.Combine(AppContext.BaseDirectory, "Fixtures", name);

        [Fact]
        public void Example_file_loads_and_is_valid()
        {
            BuildingModel model = BuildingJson.Load(Fixture("building.example.json"));

            Assert.Equal(ContractInfo.SupportedSchemaVersion, model.SchemaVersion);
            Assert.Equal(new[] { "L1", "LR" }, model.Levels.Select(l => l.Id));
            Assert.Equal(5, model.Walls.Count);
            Assert.Equal(2, model.Openings.Count);
            Assert.Single(model.Columns);
            Assert.Equal(2, model.Spaces.Count);
            Assert.True(model.Georef.IsGeoreferenced);
            Assert.Equal(4_880_000.0, model.Georef.Offset.X);
            Assert.Empty(BuildingValidator.Validate(model));
        }

        [Fact]
        public void Schema_file_declares_the_version_this_assembly_supports()
        {
            using JsonDocument schema = JsonDocument.Parse(File.ReadAllText(Fixture("building.schema.json")));
            string? version = schema.RootElement.GetProperty("x-schema-version").GetString();
            Assert.Equal(ContractInfo.SupportedSchemaVersion, version);
        }

        [Theory]
        [InlineData("0.1.0", true)]
        [InlineData("0.4.2", true)]
        [InlineData("1.0.0", false)]
        [InlineData("", false)]
        public void Compatibility_is_decided_by_major_version(string version, bool expected)
        {
            Assert.Equal(expected, ContractInfo.IsCompatible(version));
        }

        [Fact]
        public void Incompatible_major_version_is_rejected_on_parse()
        {
            string json = File.ReadAllText(Fixture("building.example.json")).Replace("\"schema_version\": \"0.1.0\"", "\"schema_version\": \"9.0.0\"");
            Assert.Throws<ContractException>(() => BuildingJson.Parse(json));
        }

        [Fact]
        public void Validator_reports_dangling_level_and_opening_overflow()
        {
            BuildingModel model = BuildingJson.Load(Fixture("building.example.json"));
            model.Walls[0].BaseLevel = "L99";
            model.Openings[0].OffsetAlong = 50.0;

            var errors = BuildingValidator.Validate(model);

            Assert.Contains(errors, e => e.Contains("unknown level 'L99'"));
            Assert.Contains(errors, e => e.Contains("does not fit"));
        }

        [Fact]
        public void Unknown_properties_are_ignored_for_forward_compatibility()
        {
            string json = File.ReadAllText(Fixture("building.example.json")).Replace("\"walls\": [", "\"future_field\": 1, \"walls\": [");
            BuildingModel model = BuildingJson.Parse(json);
            Assert.Equal(5, model.Walls.Count);
        }
    }
}
