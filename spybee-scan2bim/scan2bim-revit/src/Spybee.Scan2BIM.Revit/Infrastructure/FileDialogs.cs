using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace Spybee.Scan2BIM.Revit.Infrastructure
{
    /// <summary>Uses Revit's own file dialog (no WinForms/WPF dependency, works on net48 and net8).</summary>
    internal static class FileDialogs
    {
        public static string? PickBuildingJson()
        {
            var dialog = new FileOpenDialog("Spybee building JSON (*.json)|*.json")
            {
                Title = "Select building.json",
            };
            if (dialog.Show() != ItemSelectionDialogResult.Confirmed) { return null; }
            ModelPath selected = dialog.GetSelectedModelPath();
            return ModelPathUtils.ConvertModelPathToUserVisiblePath(selected);
        }
    }
}
