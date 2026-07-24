$rootDir = $PSScriptRoot
$backendDir = Join-Path $rootDir "backend"
$frontendDir = Join-Path $rootDir "frontend"

# Find python executable
$pythonExe = "python"
if (Test-Path (Join-Path $backendDir "venv\Scripts\python.exe")) {
    $pythonExe = Join-Path $backendDir "venv\Scripts\python.exe"
}

# Start backend hidden
Start-Process -FilePath $pythonExe -ArgumentList "main.py" -WorkingDirectory $backendDir -WindowStyle Hidden

# Start frontend hidden
Start-Process -FilePath "npm.cmd" -ArgumentList "run dev -- --host" -WorkingDirectory $frontendDir -WindowStyle Hidden

Start-Sleep -Seconds 3
Start-Process "http://localhost:5173"
