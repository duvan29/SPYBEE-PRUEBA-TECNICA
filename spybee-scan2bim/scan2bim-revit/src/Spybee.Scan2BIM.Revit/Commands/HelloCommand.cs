using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Spybee.Scan2BIM.Contracts;
using Spybee.Scan2BIM.Revit.Infrastructure;

namespace Spybee.Scan2BIM.Revit.Commands
{
    /// <summary>Installation smoke test (task T0.4).</summary>
    [Transaction(TransactionMode.ReadOnly)]
    public sealed class HelloCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            string revit = commandData.Application.Application.VersionNumber;
            string assembly = typeof(HelloCommand).Assembly.GetName().Version?.ToString() ?? "?";
            Log.Info($"Hello from Spybee Scan2BIM {assembly} in Revit {revit}");
            TaskDialog.Show(
                "Spybee Scan2BIM",
                $"Add-in {assembly} loaded in Revit {revit}.{System.Environment.NewLine}" +
                $"building.json schema supported: {ContractInfo.SupportedSchemaVersion}{System.Environment.NewLine}" +
                $"Log folder: {Log.Folder}");
            return Result.Succeeded;
        }
    }
}
