@echo off
setlocal

echo ========================================
echo Stopping Vedic AI System (Background Services)
echo ========================================

echo Stopping Frontend (Port 5173)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5173 " ^| find "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>nul
    echo [SUCCESS] Frontend server stopped.
)

echo Stopping Backend (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 " ^| find "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>nul
    echo [SUCCESS] Backend server stopped.
)

echo.
echo ========================================
echo All background services have been stopped.
echo ========================================
ping 127.0.0.1 -n 4 >nul
