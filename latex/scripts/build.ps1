$ErrorActionPreference = "Continue"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$scoopPdfLatex = Join-Path $env:USERPROFILE "scoop\apps\miktex\current\texmfs\install\miktex\bin\x64"
if (Test-Path (Join-Path $scoopPdfLatex "pdflatex.exe")) {
    $env:Path = "$scoopPdfLatex;" + $env:Path
}

Write-Host "Building portfolio.tex..." -ForegroundColor Cyan
& pdflatex -interaction=nonstopmode portfolio.tex
Write-Host "Second pass for table of contents..." -ForegroundColor Cyan
& pdflatex -interaction=nonstopmode portfolio.tex

if (Test-Path "portfolio.pdf") {
    Move-Item -Path "portfolio.pdf" -Destination "PORTFOLIO.pdf" -Force
    Write-Host "Build finished: PORTFOLIO.pdf" -ForegroundColor Green
} else {
    Write-Host "PDF was not created. Install a LaTeX distribution (MiKTeX or TeX Live)." -ForegroundColor Red
    exit 1
}
