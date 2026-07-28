@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Stopping Samartha Vedic AI System
echo ========================================
echo.

:: --------------------------------------------------------------
:: 1. Stop Frontend (Vite on port 5173)
:: --------------------------------------------------------------
echo [1/3] Stopping Frontend (Port 5173)...

set FRONTEND_KILLED=0
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5173 " ^| find "LISTENING"') do (
    set PID=%%a
    tasklist /FI "PID eq %%a" /FO CSV /NH 2>nul | findstr /I "node.exe npm.cmd vite" >nul
    if !errorlevel! equ 0 (
        taskkill /F /PID %%a >nul 2>nul
        echo [SUCCESS] Stopped Frontend process PID %%a
        set FRONTEND_KILLED=1
    ) else (
        echo [SKIP] PID %%a on port 5173 is not a Node/Vite process
    )
)

if !FRONTEND_KILLED! equ 0 (
    echo [INFO] No Frontend process found on port 5173
)

:: --------------------------------------------------------------
:: 2. Stop Backend (Python/Uvicorn on port 8000)
:: --------------------------------------------------------------
echo [2/3] Stopping Backend (Port 8000)...

set BACKEND_KILLED=0
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 " ^| find "LISTENING"') do (
    set PID=%%a
    tasklist /FI "PID eq %%a" /FO CSV /NH 2>nul | findstr /I "python.exe uvicorn.exe vedic-ai-backend.exe" >nul
    if !errorlevel! equ 0 (
        taskkill /F /PID %%a >nul 2>nul
        echo [SUCCESS] Stopped Backend process PID %%a
        set BACKEND_KILLED=1
    ) else (
        echo [SKIP] PID %%a on port 8000 is not a Backend process
    )
)

:: Also kill vedic-ai-backend.exe explicitly (stale sidecar binary)
tasklist /FI "IMAGENAME eq vedic-ai-backend.exe" /FO CSV /NH 2>nul | findstr /I "vedic-ai-backend.exe" >nul
if !errorlevel! equ 0 (
    taskkill /F /IM vedic-ai-backend.exe >nul 2>nul
    echo [SUCCESS] Stopped vedic-ai-backend.exe (stale sidecar)
    set BACKEND_KILLED=1
)

if !BACKEND_KILLED! equ 0 (
    echo [INFO] No Backend process found on port 8000
)

:: --------------------------------------------------------------
:: 3. Cleanup
:: --------------------------------------------------------------
echo [3/3] Cleanup complete.

:: Brief wait for ports to fully release
ping 127.0.0.1 -n 2 >nul

echo.
echo ========================================
echo All Samartha AI services stopped cleanly.
echo ========================================
echo.
pause