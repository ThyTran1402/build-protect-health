Protect Health
A comprehensive multi-agent healthcare system that processes patient data through AI agents for task extraction, coaching recommendations, and health reporting. Built with React frontend and FastAPI backend.

🏥 Overview
The Protect Health Dashboard is a modern healthcare application that leverages multiple AI agents to:

Extract actionable tasks from doctor visit transcripts
Provide pre-visit coaching and personalized guidance
Generate comprehensive health reports based on patient data
Coordinate care through intelligent agent orchestration
🚀 Features
Multi-Agent Processing: Orchestrates specialized AI agents for different healthcare tasks
Intelligent Task Extraction: Automatically identifies and prioritizes healthcare tasks
Personalized Coaching: Provides tailored pre-visit guidance and checklists
Comprehensive Reporting: Generates detailed health summaries and recommendations
Modern UI: Beautiful, responsive dashboard built with React and Tailwind CSS
Real-time Processing: Fast API responses with live status updates
🏗️ Architecture
Protect Health Dashboard/
├── healthcare-agents/
│   ├── backend/                 # FastAPI backend
│   │   ├── main.py             # Main FastAPI application
│   │   ├── multi-agents/       # AI agent modules
│   │   │   ├── orchestration.py
│   │   │   ├── intake-agent.py
│   │   │   ├── coach-agent.py
│   │   │   ├── report-agent.py
│   │   │   └── A2A-remote.py
│   │   └── requirements.txt    # Python dependencies
│   └── frontend/               # React frontend
│       ├── src/
│       │   ├── components/
│       │   │   └── dashboard.tsx
│       │   ├── App.tsx
│       │   ├── index.tsx
│       │   └── index.css
│       ├── public/
│       └── package.json
├── install-dependencies.bat    # Windows dependency installer
├── start-backend.bat          # Backend server starter
├── start-frontend.bat         # Frontend server starter
├── start-both.bat             # Start both servers
└── README.md
🛠️ Prerequisites
Python 3.8+ with pip
Node.js 16+ with npm
Git for version control
📦 Installation
Quick Start (Windows)
Clone the repository:

git clone <repository-url>
cd build-protect-health
Install all dependencies:

install-dependencies.bat
Manual Installation
Backend Setup:

cd healthcare-agents/backend
pip install -r requirements.txt
Frontend Setup:

cd healthcare-agents/frontend
npm install
🚀 Running the Application
Option 1: Start Both Servers (Recommended)
start-both.bat
Option 2: Start Servers Separately
Terminal 1 - Backend:

start-backend.bat
# or: cd healthcare-agents/backend && python -m uvicorn main:app --reload --port 8000
Terminal 2 - Frontend:

start-frontend.bat
# or: cd healthcare-agents/frontend && npm start
🌐 Access Points
Frontend Dashboard: http://localhost:3000
Backend API: http://localhost:8000
API Documentation: http://localhost:8000/docs
Health Check: http://localhost:8000/health
📱 Usage
Open the dashboard at http://localhost:3000
Fill in the patient information:
Patient Condition: Enter the medical condition (e.g., "Type 2 Diabetes")
Visit Type: Select from Follow-up, Initial, Emergency, or Routine
Visit Transcript: Paste the doctor's visit notes or transcript
Click "Process with AI Agents" to analyze the data
Review results across three tabs:
Tasks: Extracted actionable healthcare tasks with confidence scores
Pre-Visit Coaching: Personalized checklist, cautions, and doctor questions
Health Report: Comprehensive health summary and recommendations
🔌 API Endpoints
Main Processing
POST /api/agents/process - Process healthcare data through all agents
Individual Agent Endpoints
POST /api/ingest/transcript - Process visit transcript
POST /api/coach - Get coaching recommendations
POST /api/skin/analyze - Analyze skin images
GET /api/report/{session_id} - Get health report
Utility Endpoints
GET / - API status
GET /health - Health check
🧠 AI Agents
The system includes specialized AI agents:

Intake Agent: Processes and analyzes visit transcripts
Coach Agent: Provides personalized coaching recommendations
Report Agent: Generates comprehensive health reports
Orchestration: Coordinates all agents for seamless processing
🛠️ Development
Backend Development
Framework: FastAPI with automatic API documentation
Agent System: Google ADK for multi-agent orchestration
CORS: Enabled for frontend communication
Hot Reload: Automatic server restart on code changes
Frontend Development
Framework: React 18 with TypeScript
Styling: Tailwind CSS for modern, responsive design
Icons: Lucide React for consistent iconography
Proxy: Configured for seamless API communication
Adding New Agents
Create agent module in healthcare-agents/backend/multi-agents/
Import and add to orchestration in orchestration.py
Add corresponding API endpoint in main.py
Update frontend to handle new agent responses
🐛 Troubleshooting
Common Issues
Port Already in Use:

# Backend - change port in start-backend.bat
python -m uvicorn main:app --reload --port 8001

# Frontend - React will prompt for different port
CORS Errors:

Ensure backend is running on port 8000
Check CORS configuration in main.py
Module Import Errors:

Verify you're in the correct directory
Check Python path and virtual environment
Ensure all dependencies are installed
Frontend Build Errors:

Run npm install in frontend directory
Check Node.js version compatibility
Clear npm cache: npm cache clean --force
Debugging
Backend Logs: Check terminal running backend server
Frontend Logs: Check browser developer console
API Testing: Use http://localhost:8000/docs for interactive testing
📊 Dependencies
Backend Dependencies
FastAPI: Modern, fast web framework
Uvicorn: ASGI server for FastAPI
Google ADK: Multi-agent orchestration
Google Cloud: Firestore, Storage, Pub/Sub integration
AI/ML: OpenAI, Anthropic, Google GenAI
Frontend Dependencies
React: UI framework
TypeScript: Type safety
Tailwind CSS: Utility-first CSS framework
Lucide React: Icon library
🤝 Contributing
Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Make your changes
Test both frontend and backend
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🆘 Support
For support and questions:

Check the troubleshooting section above
Review the API documentation at http://localhost:8000/docs
Open an issue in the repository
🔮 Roadmap
 Enhanced AI agent capabilities
 Mobile-responsive improvements
 Advanced analytics dashboard
 Integration with electronic health records
 Real-time collaboration features
Protect Health Dashboard - Empowering healthcare through intelligent multi-agent systems.
