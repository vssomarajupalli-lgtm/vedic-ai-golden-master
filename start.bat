@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Starting Samartha Vedic AI System v1.0
echo ========================================
echo.

:: --------------------------------------------------------------
:: 0. Verify Prerequisites
:: --------------------------------------------------------------
echo [0/5] Verifying prerequisites...
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.11+ and add to PATH.
    pause
    exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Node.js/npm is not installed or not in PATH.
    echo Please install Node.js 18+ and add to PATH.
    pause
    exit /b 1
)

echo [OK] Prerequisites verified.
echo.

:: --------------------------------------------------------------
:: 1. Clean up stale backend processes on port 8000
:: --------------------------------------------------------------
echo [1/5] Cleaning up stale backend processes on port 8000...

:: Kill only known backend process types on port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 " ^| find "LISTENING"') do (
    set PID=%%a
    tasklist /FI "PID eq %%a" /FO CSV /NH 2>nul | findstr /I "vedic-ai-backend.exe python.exe uvicorn.exe" >nul
    if !errorlevel! equ 0 (
        taskkill /F /PID %%a >nul 2>nul
        echo [CLEANUP] Stopped stale process PID %%a
    )
)

:: Also kill any vedic-ai-backend.exe processes regardless of port
tasklist /FI "IMAGENAME eq vedic-ai-backend.exe" /FO CSV /NH 2>nul | findstr /I "vedic-ai-backend.exe" >nul
if !errorlevel! equ 0 (
    taskkill /F /IM vedic-ai-backend.exe >nul 2>nul
    echo [CLEANUP] Stopped vedic-ai-backend.exe
)

:: Wait briefly for port to be released
ping 127.0.0.1 -n 2 >nul

echo [OK] Port 8000 cleared.
echo.

:: --------------------------------------------------------------
:: 2. Start Backend from source (backend/main.py)
:: --------------------------------------------------------------
echo [2/5] Starting Backend from source (backend/main.py)...
cd /d "%~dp0backend"

:: Check for virtual environment
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found at backend\venv
    echo Please run: python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
    pause
    exit /b 1
)

:: Start backend in a new window (not minimized so we can see logs if needed)
start "Vedic AI - Backend" cmd /c "call venv\Scripts\activate.bat && python main.py"

echo [LAUNCH] Backend process started. Waiting for health check...
echo.

:: --------------------------------------------------------------
:: 3. Health Check - Wait for Backend Ready
:: --------------------------------------------------------------
echo [3/5] Waiting for Backend health check (GET /api/v1/health)...

set MAX_RETRIES=30
set RETRY_COUNT=0
set BACKEND_READY=0

:HEALTH_CHECK_LOOP
if !RETRY_COUNT! geq !MAX_RETRIES! (
    echo [ERROR] Backend health check timed out after !MAX_RETRIES! attempts.
    echo Backend may have failed to start. Check the backend window for errors.
    pause
    exit /b 1
)

set /a RETRY_COUNT+=1

:: Try to call health endpoint
curl -s -f "http://localhost:8000/api/v1/health/" >nul 2>nul
if !errorlevel! equ 0 (
    set BACKEND_READY=1
    echo [OK] Backend is healthy (attempt !RETRY_COUNT!/!MAX_RETRIES!)
    goto :BACKEND_DONE
) else (
    echo [WAIT] Backend not ready yet... (attempt !RETRY_COUNT!/!MAX_RETRIES!)
    ping 127.0.0.1 -n 2 >nul
    goto :HEALTH_CHECK_LOOP
)

:BACKEND_DONE
echo.

:: --------------------------------------------------------------
:: 4. Start Frontend
:: --------------------------------------------------------------
echo [4/5] Starting Frontend (Vite dev server)...
cd /d "%~dp0frontend"

start "Vedic AI - Frontend" cmd /c "npm run dev -- --host"

echo [LAUNCH] Frontend process started. Waiting for readiness...

:: Wait for frontend to be accessible
set MAX_RETRIES=30
set RETRY_COUNT=0
set FRONTEND_READY=0

:FRONTEND_CHECK_LOOP
if !RETRY_COUNT! geq !MAX_RETRIES! (
    echo [ERROR] Frontend health check timed out after !MAX_RETRIES! attempts.
    pause
    exit /b 1
)

set /a RETRY_COUNT+=1

curl -s -f "http://localhost:5173/" >nul 2>nul
if !errorlevel! equ 0 (
    set FRONTEND_READY=1
    echo [OK] Frontend is ready (attempt !RETRY_COUNT!/!MAX_RETRIES!)
    goto :FRONTEND_DONE
) else (
    echo [WAIT] Frontend not ready yet... (attempt !RETRY_COUNT!/!MAX_RETRIES!)
    ping 127.0.0.1 -n 2 >nul
    goto :FRONTEND_CHECK_LOOP
)

:FRONTEND_DONE
echo.

:: --------------------------------------------------------------
:: 5. Open Browser
:: --------------------------------------------------------------
echo [5/5] Opening Browser...
start http://localhost:5173
echo [OK] Browser launched.
echo.

:: --------------------------------------------------------------
:: System Ready
:: --------------------------------------------------------------
echo ========================================
echo Samartha Vedic AI System v1.0 - READY
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/api/v1/openapi.json
echo.
echo Upload a Canonical JSON to generate consultations.
echo Press Ctrl+C in the backend window to stop the server.
echo.

exit /b 0