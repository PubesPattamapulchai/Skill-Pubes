<#
Install all Skill-Pubes skills into a Claude Code skills directory.

Usage:
  .\install.ps1              # copy all skills into $HOME\.claude\skills (global)
  .\install.ps1 -Project     # copy all skills into .\.claude\skills (this project only)
  .\install.ps1 -Link        # symlink instead of copy (global; picks up `git pull` updates)
  .\install.ps1 -Dest DIR    # install into a custom directory
#>

param(
    [switch]$Project,
    [switch]$Link,
    [string]$Dest
)

$ErrorActionPreference = "Stop"

$repoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillsSrc = Join-Path $repoDir "skills"

if (-not $Dest) {
    $Dest = if ($Project) { Join-Path (Get-Location) ".claude\skills" } else { Join-Path $HOME ".claude\skills" }
}

New-Item -ItemType Directory -Force -Path $Dest | Out-Null

$skillDirs = Get-ChildItem -Path $skillsSrc -Directory
foreach ($skillDir in $skillDirs) {
    $name = $skillDir.Name
    $target = Join-Path $Dest $name

    if (Test-Path $target) {
        Remove-Item -Recurse -Force $target
    }

    if ($Link) {
        New-Item -ItemType SymbolicLink -Path $target -Target $skillDir.FullName | Out-Null
        Write-Host "linked  $name -> $target"
    } else {
        Copy-Item -Recurse -Path $skillDir.FullName -Destination $target
        Write-Host "copied  $name -> $target"
    }
}

Write-Host ""
Write-Host "Done. Installed $($skillDirs.Count) skills into $Dest"
