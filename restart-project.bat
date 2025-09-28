@echo off
echo Restarting Healthcare AI Agents Project...
echo.

echo Stopping any running processes...
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul

echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "cd healthcare-agents\backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd healthcare-agents\frontend && npm start"

echo.
echo Both servers are starting up...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo If you see module errors, try:
echo 1. Stop the frontend (Ctrl+C)
echo 2. Run: cd healthcare-agents\frontend && npm install
echo 3. Run: npm start
echo.
pause
