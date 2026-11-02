<#
.SYNOPSIS
  Create the Visual Studio solution (if missing), restore, build the Revit-free projects and run tests.
#>
param([string]$RevitVersion = "2025")
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
    if (-not (Get-ChildItem -Filter "Spybee.Scan2BIM.sln*" -ErrorAction SilentlyContinue)) {
        dotnet new sln -n Spybee.Scan2BIM
        dotnet sln add `
            src/Spybee.Scan2BIM.Contracts/Spybee.Scan2BIM.Contracts.csproj `
            src/Spybee.Scan2BIM.Core/Spybee.Scan2BIM.Core.csproj `
            src/Spybee.Scan2BIM.Revit/Spybee.Scan2BIM.Revit.csproj `
            tests/Spybee.Scan2BIM.Tests/Spybee.Scan2BIM.Tests.csproj
    }
    dotnet test tests/Spybee.Scan2BIM.Tests/Spybee.Scan2BIM.Tests.csproj
    if ($LASTEXITCODE -ne 0) { throw "Tests failed." }
    dotnet build src/Spybee.Scan2BIM.Revit/Spybee.Scan2BIM.Revit.csproj -c Debug -p:RevitVersion=$RevitVersion
    if ($LASTEXITCODE -ne 0) { throw "Revit add-in build failed (is Revit $RevitVersion installed?)." }
    Write-Host "OK. Next: ./scripts/install.ps1 -RevitVersion $RevitVersion"
}
finally {
    Pop-Location
}
