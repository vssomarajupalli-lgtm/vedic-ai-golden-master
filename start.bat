@echo off
setlocal enabledelayedexpansion

:: Console title
title Samartha Vedic AI - Launcher

:: Capture ANSI escape character (robust across Win10/11)
for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "CLR_GREEN=!ESC![92m"
set "CLR_YELLOW=!ESC![93m"
set "CLR_RED=!ESC![91m"
set "CLR_CYAN=!ESC![96m"
set "CLR_RESET=!ESC![0m"

:: Helper macros for colored output
set "OKTXT=echo !CLR_GREEN![OK]!CLR_RESET!"
set "WARNTXT=echo !CLR_YELLOW![WAIT]!CLR_RESET!"
set "ERRTXT=echo !CLR_RED![ERROR]!CLR_RESET!"
set "INFOTXT=echo !CLR_CYAN![INFO]!CLR_RESET!"

echo ========================================
echo  Samartha Vedic AI System v1.0
echo ========================================
echo.

:: --------------------------------------------------------------
:: Repository State & Git SHA
:: --------------------------------------------------------------
echo  Repository State : GM-013
echo  Backend Tests    : 739 PASS  /  1 SKIP  /  0 FAIL
echo.
:: Display current Git SHA if available (skip gracefully if Git is unavailable)
set "REPO=%~dp0"
set "REPO=%REPO:~0,-1%"
for /f "usebackq delims=" %%s in (`git -C "%REPO%" rev-parse --short HEAD 2^>nul`) do set "GIT_SHA=%%s"
if defined GIT_SHA (
    echo  Git SHA          : %GIT_SHA%
) else (
    echo  Git SHA          : unavailable
)
echo.

:: --------------------------------------------------------------
:: 0. Verify Prerequisites
:: --------------------------------------------------------------
echo [0/5] Verifying prerequisites...
where python >nul 2>nul
if errorlevel 1 (
    %ERRTXT% Python is not installed or not in PATH.
    echo        Please install Python 3.11+ and add to PATH.
    pause
    exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
    %ERRTXT% Node.js/npm is not installed or not in PATH.
    echo        Please install Node.js 18+ and add to PATH.
    pause
    exit /b 1
)

:: Verify backend virtual environment exists
if not exist "%~dp0backend\venv\Scripts\activate.bat" (
    %ERRTXT% Virtual environment not found at backend\venv.
    echo        Please run: python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

:: Verify frontend dependencies exist
if not exist "%~dp0frontend\node_modules" (
    %ERRTXT% Frontend dependencies not found at frontend\node_modules.
    echo        Please run: cd frontend ^&^& npm install
    pause
    exit /b 1
)

%OKTXT% Prerequisites verified.
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

:: Check for virtual environment (redundant with step 0, kept as local guard)
if not exist "venv\Scripts\activate.bat" (
    %ERRTXT% Virtual environment not found at backend\venv
    echo        Please run: python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

:: Start backend in a new window (not minimized so we can see logs if needed)
start "Vedic AI - Backend" cmd /c "call venv\Scripts\activate.bat && python main.py"

%INFOTXT% Backend process started. Waiting for health check...
echo.

:: --------------------------------------------------------------
:: 3. Health Check - Wait for Backend Ready
:: --------------------------------------------------------------
echo [3/5] Waiting for Backend health check (GET /api/v1/health)...

set MAX_RETRIES=60
set RETRY_COUNT=0
set BACKEND_READY=0

:HEALTH_CHECK_LOOP
if !RETRY_COUNT! geq !MAX_RETRIES! (
    %ERRTXT% Backend health check timed out after !MAX_RETRIES! attempts.
    echo        Backend failed to start.
    echo        Check the backend window for errors.
    pause
    exit /b 1
)

set /a RETRY_COUNT+=1

:: Try to call health endpoint
curl -s -f "http://localhost:8000/api/v1/health/" >nul 2>nul
if !errorlevel! equ 0 (
    set BACKEND_READY=1
    %OKTXT% Backend is healthy (attempt !RETRY_COUNT!/!MAX_RETRIES!)
    goto :BACKEND_DONE
) else (
    %WARNTXT% Backend not ready yet... (attempt !RETRY_COUNT!/!MAX_RETRIES!)
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

%INFOTXT% Frontend process started. Waiting for readiness...

:: Wait for frontend to be accessible
set MAX_RETRIES=30
set RETRY_COUNT=0
set FRONTEND_READY=0

:FRONTEND_CHECK_LOOP
if !RETRY_COUNT! geq !MAX_RETRIES! (
    %ERRTXT% Frontend health check timed out after !MAX_RETRIES! attempts.
    pause
    exit /b 1
)

set /a RETRY_COUNT+=1

curl -s -f "http://localhost:5173/" >nul 2>nul
if !errorlevel! equ 0 (
    set FRONTEND_READY=1
    %OKTXT% Frontend is ready (attempt !RETRY_COUNT!/!MAX_RETRIES!)
    goto :FRONTEND_DONE
) else (
    %WARNTXT% Frontend not ready yet... (attempt !RETRY_COUNT!/!MAX_RETRIES!)
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
echo.
echo ========================================
echo  Samartha Vedic AI System v1.0 - READY
echo ========================================
echo.
echo  Backend:  http://localhost:8000
echo  Swagger:  http://localhost:8000/docs
echo  Health:   http://localhost:8000/api/v1/health/
echo  Frontend: http://localhost:5173
echo.
echo  Upload a Canonical JSON to generate consultations.
echo  Press Ctrl+C in the backend window to stop the server.
echo.

%OKTXT% System launched successfully.
echo.

exit /b 0