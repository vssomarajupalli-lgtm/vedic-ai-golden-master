@echo off
setlocal

:: Verify dependencies
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
    echo [ERROR] npm Node.js is not installed or not in PATH.
    pause
    exit /b 1
)

:: Run Backend in a minimized window
cd /d "%~dp0backend"
start "Vedic AI - Backend" /MIN cmd /c "if exist venv\Scripts\activate.bat (call venv\Scripts\activate.bat) && python main.py"

:: Run Frontend in a minimized window
cd /d "%~dp0frontend"
start "Vedic AI - Frontend" /MIN cmd /c "npm run dev -- --host"

:: Wait a few seconds to ensure servers are up
ping 127.0.0.1 -n 4 >nul

:: Open Browser
start http://localhost:5173

exit
