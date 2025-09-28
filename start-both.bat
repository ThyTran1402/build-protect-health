@echo off
echo Starting Healthcare AI Agents - Full Stack Application
echo.
echo This will start both backend and frontend servers.
echo Backend will run on http://localhost:8000
echo Frontend will run on http://localhost:3000
echo.
echo Press Ctrl+C in each window to stop the servers.
echo.

start "Backend Server" cmd /k "cd healthcare-agents\backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd healthcare-agents\frontend && npm start"

echo.
echo Both servers are starting up...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
pause
