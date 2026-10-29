param([switch]$SkipTests)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$runtime = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $runtime)) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Création de .venv impossible. Python 3.12 Windows x64 et ensurepip sont nécessaires.' }
}
& $runtime -c "import sys,struct; assert sys.version_info[:2] == (3,12) and struct.calcsize('P') == 8"
if ($LASTEXITCODE -ne 0) { throw 'Python 3.12 x64 requis.' }
if (Get-Command uv -ErrorAction SilentlyContinue) {
    uv pip sync --python $runtime --cache-dir .build-cache requirements-lock.txt
} else {
    & $runtime -m pip install -r requirements-lock.txt
}
if ($LASTEXITCODE -ne 0) { throw 'Installation des dépendances impossible.' }
if (-not $SkipTests) {
    & $runtime scripts\run_tests.py
    if ($LASTEXITCODE -ne 0) { throw 'Tests en échec : construction arrêtée.' }
}
& $runtime scripts\collect_licenses.py
if ($LASTEXITCODE -ne 0) { throw 'Collecte des licences impossible.' }
& (Join-Path $PSScriptRoot 'scripts\build_icon.ps1') | Out-Null
& (Join-Path $PSScriptRoot 'scripts\build_sidebar_image.ps1') | Out-Null
$env:PYINSTALLER_CONFIG_DIR = Join-Path $PSScriptRoot '.build-cache\pyinstaller'
& $runtime -m PyInstaller --noconfirm --clean GARDAVU.spec
if ($LASTEXITCODE -ne 0) { throw 'Échec de PyInstaller.' }
$smokeFolder = Join-Path $PSScriptRoot ('artifacts\recette-construction-' + [guid]::NewGuid().ToString('N'))
$builtExe = Join-Path $PSScriptRoot 'dist\GARDAVU.exe'
$smokeProcess = Start-Process -FilePath $builtExe -ArgumentList @('--self-test', ('"' + $smokeFolder + '"')) -WindowStyle Hidden -Wait -PassThru
if ($smokeProcess.ExitCode -ne 0) { throw "Recette du binaire en échec : $smokeFolder" }
$smokeReport = Get-Content -LiteralPath (Join-Path $smokeFolder 'rapport.json') -Raw | ConvertFrom-Json
if (-not $smokeReport.success -or -not $smokeReport.frozen -or $smokeReport.assignments -ne 32) {
    throw "Recette du binaire non conforme : $smokeFolder"
}
& $runtime scripts\package_release.py
if ($LASTEXITCODE -ne 0) { throw 'Création de la distribution impossible.' }
Get-Item -LiteralPath 'dist\GARDAVU.exe','dist\GARDAVU-portable.zip' | Select-Object Name,Length
