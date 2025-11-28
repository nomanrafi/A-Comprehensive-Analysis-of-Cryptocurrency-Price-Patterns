#!/usr/bin/env pwsh
# Cryptocurrency Price Prediction - PowerShell Launcher

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host ""
Write-Host "================================================================"
Write-Host " CRYPTOCURRENCY PRICE PREDICTION - Flask Application"
Write-Host "================================================================"
Write-Host ""

# Check if models exist
$modelsPath = Join-Path $ScriptDir "models"
$requiredFiles = @(
    "xgboost_model.pkl",
    "lightgbm_model.pkl",
    "random_forest_model.pkl",
    "svr_model.pkl"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    $filePath = Join-Path $modelsPath $file
    if (-not (Test-Path $filePath)) {
        $allFilesExist = $false
        break
    }
}

if (-not $allFilesExist) {
    Write-Host "WARNING: Models not found!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please train the models first:"
    Write-Host "  1. Run: jupyter notebook CRYPTO_PRICE_PREDICTION.ipynb"
    Write-Host "  2. Execute all cells"
    Write-Host "  3. Models will be saved to: ./models/"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Models found successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Starting Flask application..." -ForegroundColor Cyan
Write-Host "Local URL: http://127.0.0.1:5000"
Write-Host ""
Write-Host "Press Ctrl+C to stop"
Write-Host ""

python run_app.py
