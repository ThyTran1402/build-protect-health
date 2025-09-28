@echo off
echo Installing Healthcare AI Agents Dependencies...
echo.

echo Installing Backend Dependencies...
cd healthcare-agents\backend
pip install -r requirements.txt
cd ..\..

echo.
echo Installing Frontend Dependencies...
cd healthcare-agents\frontend
npm install
cd ..\..

echo.
echo All dependencies installed successfully!
echo.
echo Next steps:
echo 1. Run start-both.bat to start both servers
echo 2. Or run start-backend.bat and start-frontend.bat separately
echo.
pause
