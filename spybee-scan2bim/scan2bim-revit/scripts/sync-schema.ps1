<#
.SYNOPSIS
  Copy the building.json contract (schema + example) from the Python repo, which owns it.
  Run after every `uv run scan2bim schema` in scan2bim-pipeline, then run the tests.
#>
param([string]$PipelineRepo = (Join-Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)) "scan2bim-pipeline"))
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$source = Join-Path $PipelineRepo "schema"
if (-not (Test-Path (Join-Path $source "building.schema.json"))) { throw "Schema not found under $source" }

Copy-Item (Join-Path $source "building.schema.json") (Join-Path $repo "schema/building.schema.json") -Force
New-Item -ItemType Directory -Force -Path (Join-Path $repo "schema/examples") | Out-Null
Copy-Item (Join-Path $source "examples/building.example.json") (Join-Path $repo "schema/examples/building.example.json") -Force

$version = (Get-Content (Join-Path $repo "schema/building.schema.json") -Raw | ConvertFrom-Json).'x-schema-version'
Write-Host "Synced building.json schema $version. If MAJOR/MINOR changed, update ContractInfo.SupportedSchemaVersion and BuildingModel.cs."
dotnet test (Join-Path $repo "tests/Spybee.Scan2BIM.Tests/Spybee.Scan2BIM.Tests.csproj")
