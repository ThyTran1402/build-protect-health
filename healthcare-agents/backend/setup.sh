#!/bin/bash
# Setup script for Google ADK Healthcare Agents

echo "🏥 Setting up Healthcare AI Agents with Google ADK"
echo "=================================================="

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check for Google Cloud SDK
if ! command -v gcloud &> /dev/null; then
    echo "⚠️  Google Cloud SDK not found. Please install it:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set up Google Cloud authentication
echo "🔐 Setting up Google Cloud authentication..."
echo "Please make sure you have:"
echo "1. Created a Google Cloud project"
echo "2. Enabled the required APIs (Firestore, Gemini AI)"
echo "3. Created a service account with proper permissions"
echo "4. Downloaded the service account key JSON file"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

echo ""
echo "✅ Setup complete! Next steps:"
echo "1. Edit .env file with your Google Cloud configuration"
echo "2. Set GOOGLE_APPLICATION_CREDENTIALS to your service account key path"
echo "3. Set GOOGLE_AI_API_KEY for Gemini AI access"
echo "4. Run: python -m uvicorn main:app --reload --port 8000"