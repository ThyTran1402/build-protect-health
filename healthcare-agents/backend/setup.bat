@echo off
REM Setup script for Google ADK Healthcare Agents (Windows)

echo 🏥 Setting up Healthcare AI Agents with Google ADK
echo ==================================================

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Check if gcloud is installed
where gcloud >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Google Cloud SDK not found. Please install it:
    echo    https://cloud.google.com/sdk/docs/install
    exit /b 1
)

REM Set up authentication info
echo 🔐 Setting up Google Cloud authentication...
echo Please make sure you have:
echo 1. Created a Google Cloud project
echo 2. Enabled the required APIs (Firestore, Gemini AI)
echo 3. Created a service account with proper permissions
echo 4. Downloaded the service account key JSON file

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from example...
    copy .env.example .env
    echo Please edit .env file with your configuration
)

echo.
echo ✅ Setup complete! Next steps:
echo 1. Edit .env file with your Google Cloud configuration
echo 2. Set GOOGLE_APPLICATION_CREDENTIALS to your service account key path
echo 3. Set GOOGLE_AI_API_KEY for Gemini AI access
echo 4. Run: python -m uvicorn main:app --reload --port 8000

pause