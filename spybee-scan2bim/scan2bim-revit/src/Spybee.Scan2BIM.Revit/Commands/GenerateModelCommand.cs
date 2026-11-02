using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Spybee.Scan2BIM.Contracts;
using Spybee.Scan2BIM.Revit.Build;
using Spybee.Scan2BIM.Revit.Infrastructure;

namespace Spybee.Scan2BIM.Revit.Commands
{
    /// <summary>"Spybee: Generate model" — building.json → native Revit elements (tasks T5.2–T5.4, T6.4).</summary>
    [Transaction(TransactionMode.Manual)]
    public sealed class GenerateModelCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            Document? doc = commandData.Application.ActiveUIDocument?.Document;
            if (doc == null || doc.IsFamilyDocument)
            {
                message = "Open a Revit PROJECT (not a family) before generating the model.";
                return Result.Failed;
            }

            string? path = FileDialogs.PickBuildingJson();
            if (path == null) { return Result.Cancelled; }

            BuildingModel model;
            try
            {
                model = BuildingJson.Load(path);
            }
            catch (ContractException ex)
            {
                TaskDialog.Show("Spybee Scan2BIM", ex.Message);
                Log.Error($"Cannot load {path}", ex);
                return Result.Failed;
            }

            IReadOnlyList<string> errors = BuildingValidator.Validate(model);
            if (errors.Count > 0)
            {
                TaskDialog.Show("Spybee Scan2BIM", "building.json has integrity errors:" + Environment.NewLine +
                    string.Join(Environment.NewLine, errors.Take(20)));
                Log.Error($"Integrity errors in {path}: {string.Join("; ", errors)}");
                return Result.Failed;
            }

            var report = new GenerationReport();
            var swallower = new WarningSwallower();
            using (var transaction = new Transaction(doc, "Spybee: Generate model"))
            {
                FailureHandlingOptions options = transaction.GetFailureHandlingOptions();
                options.SetFailuresPreprocessor(swallower);
                transaction.SetFailureHandlingOptions(options);
                transaction.Start();
                try
                {
                    new ModelBuilder(doc, model, report).Run();
                    transaction.Commit();
                }
                catch (Exception ex)
                {
                    if (transaction.HasStarted() && !transaction.HasEnded()) { transaction.RollBack(); }
                    Log.Error("Generate model failed", ex);
                    message = $"Generate model failed: {ex.Message} (see log in {Log.Folder})";
                    return Result.Failed;
                }
            }

            report.WarningsSuppressed = swallower.Count;
            string summary = report.ToSummary();
            Log.Info($"Generated from {path}{Environment.NewLine}{summary}");
            foreach (string failure in report.Failures) { Log.Warn(failure); }
            TaskDialog.Show("Spybee Scan2BIM", summary);
            return Result.Succeeded;
        }
    }
}
