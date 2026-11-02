<#
.SYNOPSIS
  Build the add-in for one Revit version and install it for the current user.
.EXAMPLE
  ./scripts/install.ps1 -RevitVersion 2025
#>
param(
    [string]$RevitVersion = "2025",
    [string]$Configuration = "Release"
)
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot

if (Get-Process -Name "Revit" -ErrorAction SilentlyContinue) {
    throw "Close Revit first: Revit locks the add-in DLL while it is running."
}

$project = Join-Path $repo "src/Spybee.Scan2BIM.Revit/Spybee.Scan2BIM.Revit.csproj"
dotnet build $project -c $Configuration -p:RevitVersion=$RevitVersion
if ($LASTEXITCODE -ne 0) { throw "Build failed." }

$buildDir = Join-Path $repo "src/Spybee.Scan2BIM.Revit/bin/$Configuration/Revit$RevitVersion"
$addinRoot = Join-Path $env:APPDATA "Autodesk/Revit/Addins/$RevitVersion"
$installDir = Join-Path $addinRoot "Spybee.Scan2BIM"

# Copy the build output to a private folder (so rebuilding never fights with a running Revit).
New-Item -ItemType Directory -Force -Path $installDir | Out-Null
Copy-Item -Path (Join-Path $buildDir "*") -Destination $installDir -Recurse -Force

$dll = Join-Path $installDir "Spybee.Scan2BIM.Revit.dll"
if (-not (Test-Path $dll)) { throw "Add-in DLL not found after copy: $dll" }

$template = Get-Content (Join-Path $repo "addin/Spybee.Scan2BIM.addin.template") -Raw
$manifest = $template.Replace("__DLL_PATH__", $dll)
Set-Content -Path (Join-Path $addinRoot "Spybee.Scan2BIM.addin") -Value $manifest -Encoding UTF8

Write-Host "Installed Spybee Scan2BIM for Revit $RevitVersion"
Write-Host "  manifest: $(Join-Path $addinRoot 'Spybee.Scan2BIM.addin')"
Write-Host "  binaries: $installDir"
Write-Host "Open Revit -> Add-Ins (Complementos) -> External Tools (Herramientas externas)."
