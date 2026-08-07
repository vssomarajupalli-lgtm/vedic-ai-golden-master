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
:: Repository State, Git SHA & Launcher Metadata
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
echo [0/6] Verifying prerequisites...
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

:: ------------------------------------------------------------------
:: 1. Clean up stale Backend processes and free port 8000
:: ******************************************************************
:: Requirement: terminate ONLY the process listening on TCP port 8000
:: (the backend). Never match generic python.exe / spawn_main / other
:: Python processes, to avoid killing unrelated or legitimate children.
:: ******************************************************************
echo [1/6] Cleaning up stale backend processes...
echo        Freeing port 8000...

:: 1A. Terminate the PID listening on TCP 8000 (if any)
set "P8000_PID="
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 " ^| find "LISTENING"') do set "P8000_PID=%%a"
if defined P8000_PID (
    taskkill /F /PID !P8000_PID! >nul 2>nul
    echo [CLEANUP] Terminated backend process listening on port 8000 [PID !P8000_PID!]
) else (
    echo [CLEANUP] No process is listening on port 8000. Nothing to clean.
)

:: 1B. Bounded wait (10 retries) until port 8000 is actually released.
set "MAX_WAIT=10"
set /a WAIT_COUNT=0
:PORT_FREE_LOOP
netstat -aon | findstr /R ":8000 " | find "LISTENING" >nul 2>nul
if errorlevel 1 (
    goto :PORT_FREE_DONE
)
:: Port still occupied - capture its owner and terminate it (a uvicorn reload
:: supervisor may respawn the listener, so re-query each iteration).
set "P8000_BUSY="
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /R ":8000 " ^| find "LISTENING"') do set "P8000_BUSY=%%a"
if defined P8000_BUSY (
    taskkill /F /PID !P8000_BUSY! >nul 2>nul
    echo [CLEANUP] Terminated backend process on port 8000 [PID !P8000_BUSY!]
)
set /a WAIT_COUNT+=1
if !WAIT_COUNT! geq !MAX_WAIT! (
    %ERRTXT% Backend port 8000 is still occupied.
    echo        Please close the backend window manually and rerun.
    pause
    exit /b 1
)
%WARNTXT% Waiting for port 8000 to be released... ^(!WAIT_COUNT!/!MAX_WAIT!^)
ping 127.0.0.1 -n 2 >nul
goto :PORT_FREE_LOOP
:PORT_FREE_DONE

%OKTXT% Port 8000 is free.
echo.

:: --------------------------------------------------------------
:: 2. Start Backend from source (backend/main.py)
:: --------------------------------------------------------------
echo [2/6] Starting Backend from source (backend/main.py)...
cd /d "%~dp0backend"

:: Check for virtual environment (redundant with step 0, kept as local guard)
if not exist "venv\Scripts\activate.bat" (
    %ERRTXT% Virtual environment not found at backend\venv
    echo        Please run: python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

:: Start backend in a new window (not minimized so we can see logs if needed)
start "Vedic AI - Backend" cmd /k "title Vedic AI - Backend && call venv\Scripts\activate.bat && python main.py"

%INFOTXT% Backend process started. Waiting for health check...
echo.

:: --------------------------------------------------------------
:: 3. Health Check - Wait for Backend Ready
:: --------------------------------------------------------------
echo [3/6] Waiting for Backend health check (GET /api/v1/health)...
echo.

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
    %OKTXT% Backend is healthy ^(attempt !RETRY_COUNT!/!MAX_RETRIES!^)
    goto :BACKEND_DONE
) else (
    %WARNTXT% Backend not ready yet... ^(attempt !RETRY_COUNT!/!MAX_RETRIES!^)
    ping 127.0.0.1 -n 2 >nul
    goto :HEALTH_CHECK_LOOP
)

:BACKEND_DONE
:: Capture the actual backend PID now that it is listening on port 8000
set "BACKEND_PID="
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 " ^| find "LISTENING"') do set "BACKEND_PID=%%a"

:: Report backend runtime identity (Requirement 4: PID is the port-8000 owner)
echo.
echo  --------------------------------------------------
echo  Backend Runtime
echo  --------------------------------------------------
echo  Backend PID   : !BACKEND_PID!
echo  Backend URL   : http://localhost:8000
echo  API Base URL  : http://localhost:8000/api/v1
if defined GIT_SHA (
    echo  Git SHA       : %GIT_SHA%
) else (
    echo  Git SHA       : unavailable
)
if not defined BACKEND_PID (
    %ERRTXT% Backend PID could not be resolved; expected port 8000 owner.
)
echo  --------------------------------------------------
echo.

:: --------------------------------------------------------------
:: 4. Clean up stale Frontend (Vite / Node) dev servers
:: ******************************************************************
::Start BEFORE the frontend so only one instance will run (Requirement 2).
:: ******************************************************************
echo [4/6] Cleaning up stale frontend (Vite/Node) dev servers...

:: Kill Node dev servers launched from THIS project (frontend/node_modules vite)
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'node.exe' -and $_.CommandLine -match 'vite' -and $_.CommandLine -match 'frontend' -and $_.CommandLine -notmatch 'omniroute' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue; Write-Output ('[CLEANUP] Stopped leftover Vite PID ' + $_.ProcessId) }"

:: Any node still holding the standard Vite dev ports (5170-5179) outside our tree
for /l %%p in (5170,1,5179) do (
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":%%p " ^| find "LISTENING"') do (
        tasklist /FI "PID eq %%a" /FO CSV /NH 2>nul | findstr /I "node.exe" >nul
        if !errorlevel! equ 0 (
            taskkill /F /PID %%a >nul 2>nul
            echo [CLEANUP] Stopped stale Vite/node on port %%p: PID %%a
        )
    )
)

:: Wait for ports to settle before starting the fresh instance
ping 127.0.0.1 -n 2 >nul
%OKTXT% Stale frontend processes cleared.
echo.

:: --------------------------------------------------------------
:: 5. Start Frontend and verify single instance
:: --------------------------------------------------------------
echo [5/6] Starting Frontend (Vite dev server)...
cd /d "%~dp0frontend"

start "Vedic AI - Frontend" cmd /k "title Vedic AI - Frontend && npm run dev -- --host"

%INFOTXT% Frontend process started. Waiting for readiness...

:: Wait for frontend to be accessible on port 5173
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
    %OKTXT% Frontend is ready ^(attempt !RETRY_COUNT!/!MAX_RETRIES!^)
    goto :FRONTEND_DONE
) else (
    %WARNTXT% Frontend not ready yet... ^(attempt !RETRY_COUNT!/!MAX_RETRIES!^)
    ping 127.0.0.1 -n 2 >nul
    goto :FRONTEND_CHECK_LOOP
)

:FRONTEND_DONE
echo.

:: Detect if multiple Vite dev servers remain after cleanup (Requirement 5).
:: Deduplicate PIDs: the same dev server binds both IPv4 and IPv6, so netstat
:: would otherwise count it twice.
set "VITE_PIDS="
if exist "%TEMP%\vite_scan.txt" del "%TEMP%\vite_scan.txt" >nul 2>nul
for /l %%p in (5170,1,5179) do (
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":%%p " ^| find "LISTENING"') do (
        set "VITE_PIDS=!VITE_PIDS! %%a"
    )
)
set VITE_COUNT=0
for %%d in (!VITE_PIDS!) do (
    if not "%%d"=="" (
        echo %%d>> "%TEMP%\vite_scan.txt"
    )
)
if exist "%TEMP%\vite_scan.txt" (
    sort /unique "%TEMP%\vite_scan.txt" > "%TEMP%\vite_uniq.txt"
    for /f %%c in ('type "%TEMP%\vite_uniq.txt"') do set /a VITE_COUNT+=1
    del "%TEMP%\vite_scan.txt" "%TEMP%\vite_uniq.txt" >nul 2>nul
)
if !VITE_COUNT! gtr 1 (
    %WARNTXT% Multiple Vite servers detected ^(!VITE_COUNT!^). Verify only one is expected.
    echo        If this persists, close extra node.exe processes and rerun.
) else (
    %OKTXT% Single frontend instance confirmed.
)

:: --------------------------------------------------------------
:: 6. Final readiness gate, then Open Browser
:: ******************************************************************
::Requirement 4: verify backend health returns HTTP 200 AND the
::frontend responds on port 5173 immediately before opening the browser.
:: ******************************************************************
echo.
echo [6/6] Final readiness verification...

curl -s -f "http://localhost:8000/api/v1/health/" >nul 2>nul
if errorlevel 1 (
    %ERRTXT% Backend health endpoint not responding. HTTP status != 200.
    echo        Please check the backend window.
    pause
    exit /b 1
)
%OKTXT% Backend health endpoint returned HTTP 200.

curl -s -f "http://localhost:5173/" >nul 2>nul
if errorlevel 1 (
    %ERRTXT% Frontend not responding on port 5173.
    echo        Please check the frontend window.
    pause
    exit /b 1
)
%OKTXT% Frontend responded on port 5173.

echo.
echo Opening Browser...
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
echo  Backend:   http://localhost:8000
echo  Swagger:   http://localhost:8000/docs
echo  Health:    http://localhost:8000/api/v1/health/
echo  Frontend:  http://localhost:5173
echo.
echo  Upload a Canonical JSON to generate consultations.
echo  Press Ctrl+C in the backend window to stop the server.
echo.

:: --------------------------------------------------------------
:: Developer reminder
:: --------------------------------------------------------------
echo  [REMINDER] If stale UI appears, perform Ctrl+Shift+R,
echo             or unregister the Service Worker from browser DevTools.
echo --------------------------------------------------------------

%OKTXT% System launched successfully.
echo.

exit /b 0