using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Spybee.Scan2BIM.Contracts
{
    /// <summary>
    /// Integrity checks equivalent to integrity_errors() in model.py. The pipeline already validates
    /// before writing; this is a second line of defence for hand-edited or older files.
    /// </summary>
    public static class BuildingValidator
    {
        private const double FitToleranceM = 0.01;

        public static IReadOnlyList<string> Validate(BuildingModel model)
        {
            var errors = new List<string>();
            if (!ContractInfo.IsCompatible(model.SchemaVersion))
            {
                errors.Add($"schema_version {model.SchemaVersion} incompatible with {ContractInfo.SupportedSchemaVersion}");
            }

            foreach (var group in model.AllElements().GroupBy(e => e.Id, StringComparer.Ordinal).Where(g => g.Count() > 1))
            {
                errors.Add($"duplicate id '{group.Key}'");
            }

            var levels = new HashSet<string>(model.Levels.Select(l => l.Id), StringComparer.Ordinal);
            void NeedLevel(string owner, string? reference, bool optional)
            {
                if (reference == null && optional) { return; }
                if (reference == null || !levels.Contains(reference)) { errors.Add($"{owner}: unknown level '{reference}'"); }
            }

            foreach (var s in model.Slabs)
            {
                NeedLevel(s.Id, s.Level, false);
                if (s.Thickness <= 0) { errors.Add($"{s.Id}: thickness must be > 0"); }
                if (!IsPolygon(s.Outline)) { errors.Add($"{s.Id}: outline needs >= 3 [x, y] points"); }
            }

            var wallLengths = new Dictionary<string, double>(StringComparer.Ordinal);
            foreach (var w in model.Walls)
            {
                NeedLevel(w.Id, w.BaseLevel, false);
                NeedLevel(w.Id, w.TopLevel, true);
                if (w.Axis.Count != 2 || w.Axis.Any(p => p == null || p.Length != 2))
                {
                    errors.Add($"{w.Id}: axis must be exactly two [x, y] points");
                    continue;
                }
                double length = Length(w.Axis[0], w.Axis[1]);
                if (length <= 1e-6) { errors.Add($"{w.Id}: zero-length axis"); }
                if (w.Thickness <= 0) { errors.Add($"{w.Id}: thickness must be > 0"); }
                if (w.Height <= 0) { errors.Add($"{w.Id}: height must be > 0"); }
                wallLengths[w.Id] = length;
            }

            foreach (var c in model.Columns)
            {
                NeedLevel(c.Id, c.BaseLevel, false);
                NeedLevel(c.Id, c.TopLevel, true);
                int expected = string.Equals(c.Shape, "rect", StringComparison.Ordinal) ? 2 : 1;
                if (c.Size.Count != expected) { errors.Add($"{c.Id}: shape '{c.Shape}' needs {expected} size value(s)"); }
            }

            foreach (var o in model.Openings)
            {
                if (!wallLengths.TryGetValue(o.Host, out double hostLength))
                {
                    errors.Add($"{o.Id}: unknown host wall '{o.Host}'");
                }
                else if (o.OffsetAlong + o.Width > hostLength + FitToleranceM)
                {
                    errors.Add(string.Format(CultureInfo.InvariantCulture,
                        "{0}: does not fit in host wall {1} ({2:0.00} m)", o.Id, o.Host, hostLength));
                }
            }

            foreach (var sp in model.Spaces)
            {
                NeedLevel(sp.Id, sp.Level, false);
                if (!IsPolygon(sp.Polygon)) { errors.Add($"{sp.Id}: polygon needs >= 3 [x, y] points"); }
            }
            return errors;
        }

        private static bool IsPolygon(List<double[]> points) =>
            points.Count >= 3 && points.All(p => p != null && p.Length == 2);

        private static double Length(double[] a, double[] b)
        {
            double dx = b[0] - a[0];
            double dy = b[1] - a[1];
            return Math.Sqrt((dx * dx) + (dy * dy));
        }
    }
}
