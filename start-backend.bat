@echo off
echo Starting Healthcare AI Agents Backend...
cd healthcare-agents\backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
