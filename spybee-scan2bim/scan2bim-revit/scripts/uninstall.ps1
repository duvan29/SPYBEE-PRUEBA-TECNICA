param([string]$RevitVersion = "2025")
$ErrorActionPreference = "Stop"
$addinRoot = Join-Path $env:APPDATA "Autodesk/Revit/Addins/$RevitVersion"
Remove-Item -Force -ErrorAction SilentlyContinue (Join-Path $addinRoot "Spybee.Scan2BIM.addin")
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $addinRoot "Spybee.Scan2BIM")
Write-Host "Removed Spybee Scan2BIM from Revit $RevitVersion"
