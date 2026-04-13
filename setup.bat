@echo off
echo ============================================================
echo   💧 Ferghana Valley WSI Prototype - Environment Setup
echo ============================================================
echo.
echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Error: Python is not installed or not in PATH.
    pause
    exit /b
)

echo [2/3] Installing/Updating required libraries...
pip install -r requirements.txt

echo [3/3] Verifying critical libraries...
python -c "import streamlit; import pandas; import sklearn; import shap; import plotly; print('Success: All libraries verified.')"

echo.
echo ============================================================
echo   ✅ Setup Complete! 
echo   To run the dashboard, type: streamlit run dashboard.py
echo ============================================================
pause
