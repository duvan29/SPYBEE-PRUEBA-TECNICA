using System.Collections.Generic;
using System.Linq;
using System.Text;
using Autodesk.Revit.DB;
using Spybee.Scan2BIM.Contracts;

namespace Spybee.Scan2BIM.Revit.Build
{
    /// <summary>A Revit element created from a building.json element (used for marking and overrides).</summary>
    internal sealed class CreatedElement
    {
        public CreatedElement(ElementId id, ElementData source, string elementClass)
        {
            Id = id;
            Source = source;
            Class = elementClass;
        }

        public ElementId Id { get; }
        public ElementData Source { get; }
        public string Class { get; }
    }

    /// <summary>What happened during "Generate model"; shown to the user and written to the log.</summary>
    internal sealed class GenerationReport
    {
        private readonly Dictionary<string, int> _created = new Dictionary<string, int>();
        private readonly List<string> _failures = new List<string>();

        public int WarningsSuppressed { get; set; }

        public void Created(string elementClass) =>
            _created[elementClass] = (_created.TryGetValue(elementClass, out int n) ? n : 0) + 1;

        public void Fail(string elementId, string reason) => _failures.Add($"{elementId}: {reason}");

        public string ToSummary()
        {
            var sb = new StringBuilder();
            sb.AppendLine("Created:");
            foreach (var pair in _created.OrderBy(p => p.Key))
            {
                sb.AppendLine($"  {pair.Key}: {pair.Value}");
            }
            sb.AppendLine($"Revit warnings suppressed: {WarningsSuppressed}");
            sb.AppendLine($"Failures: {_failures.Count}");
            foreach (string failure in _failures.Take(15))
            {
                sb.AppendLine($"  {failure}");
            }
            if (_failures.Count > 15) { sb.AppendLine("  ... see the log file for the full list"); }
            return sb.ToString();
        }

        public IReadOnlyList<string> Failures => _failures;
    }

    /// <summary>
    /// Deletes Revit warnings (e.g. "walls overlap") during generation so the user is not flooded with
    /// dialogs; they are counted in the report instead. Errors are NOT swallowed.
    /// </summary>
    internal sealed class WarningSwallower : IFailuresPreprocessor
    {
        public int Count { get; private set; }

        public FailureProcessingResult PreprocessFailures(FailuresAccessor failuresAccessor)
        {
            foreach (FailureMessageAccessor failure in failuresAccessor.GetFailureMessages())
            {
                if (failure.GetSeverity() == FailureSeverity.Warning)
                {
                    failuresAccessor.DeleteWarning(failure);
                    Count++;
                }
            }
            return FailureProcessingResult.Continue;
        }
    }
}
