@echo off
setlocal

title Vedic AI - Batch Report Launcher

:: Use the Golden Master backend Python (has Playwright/Chromium for PDF)
set "PY=%~dp0backend\venv\Scripts\python.exe"

if not exist "%PY%" (
    echo [ERROR] Backend venv python not found: %PY%
    echo         Please create backend\venv and install requirements.txt first.
    pause
    exit /b 1
)

echo ==========================================
echo  Vedic AI Golden Master - Batch Reports
echo ==========================================
echo.

"%PY%" "%~dp0backend\batch_reports.py"

echo.
echo ==========================================
echo  Batch report run finished.
echo ==========================================
pause
exit /b 0