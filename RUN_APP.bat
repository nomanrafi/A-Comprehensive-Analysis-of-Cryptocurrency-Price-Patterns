@echo off
REM Cryptocurrency Price Prediction - Windows Batch Launcher
REM This script starts the Flask web application

cd /d "%~dp0"

echo.
echo ================================================================
echo  CRYPTOCURRENCY PRICE PREDICTION - Flask Application
echo ================================================================
echo.

REM Check if models exist
if not exist "models\xgboost_model.pkl" (
    echo WARNING: Models not found!
    echo.
    echo Please train the models first:
    echo   1. Run: jupyter notebook CRYPTO_PRICE_PREDICTION.ipynb
    echo   2. Execute all cells
    echo   3. Models will be saved to: ./models/
    echo.
    pause
    exit /b 1
)

echo Models found successfully!
echo.
echo Starting Flask application...
echo Local URL: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop
echo.

python run_app.py

pause
