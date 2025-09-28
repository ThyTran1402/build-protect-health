# Healthcare AI Agents - Full Stack Application

A multi-agent healthcare system with a React frontend and FastAPI backend that processes patient data through AI agents for task extraction, coaching recommendations, and health reporting.

## Project Structure

```
healthcare-agents/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main FastAPI application
│   ├── multi-agents/       # AI agent modules
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── dashboard.tsx
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── index.css
│   ├── public/
│   └── package.json
└── README.md
```

## Features

- **Multi-Agent Processing**: Orchestrates multiple AI agents for healthcare data processing
- **Task Extraction**: Extracts actionable tasks from doctor visit transcripts
- **Coaching Recommendations**: Provides pre-visit coaching and guidance
- **Health Reporting**: Generates comprehensive health reports
- **Modern UI**: Beautiful React dashboard with Tailwind CSS

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd healthcare-agents
   ```

2. **Install all dependencies:**
   ```bash
   # Windows
   install-dependencies.bat
   
   # Or manually:
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

### Running the Application

#### Option 1: Start Both Servers (Recommended)
```bash
# Windows
start-both.bat
```

#### Option 2: Start Servers Separately
```bash
# Terminal 1 - Backend
start-backend.bat
# or: cd backend && python -m uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend  
start-frontend.bat
# or: cd frontend && npm start
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## API Endpoints

### Main Processing Endpoint
- `POST /api/agents/process` - Process healthcare data through all agents

### Individual Agent Endpoints
- `POST /api/ingest/transcript` - Process visit transcript
- `POST /api/coach` - Get coaching recommendations
- `POST /api/skin/analyze` - Analyze skin images
- `GET /api/report/{session_id}` - Get health report

### Utility Endpoints
- `GET /` - API status
- `GET /health` - Health check

## Usage

1. **Open the frontend** at http://localhost:3000
2. **Fill in the form**:
   - Patient Condition (e.g., "Type 2 Diabetes")
   - Visit Type (Follow-up, Initial, Emergency, Routine)
   - Visit Transcript (paste doctor's notes)
3. **Click "Process with AI Agents"**
4. **View results** in the three tabs:
   - **Tasks**: Extracted actionable items
   - **Pre-Visit Coaching**: Checklist, cautions, and questions
   - **Health Report**: Comprehensive health summary

## Development

### Backend Development
- FastAPI with automatic API documentation
- Multi-agent orchestration using Google ADK
- CORS enabled for frontend communication
- Hot reload enabled during development

### Frontend Development
- React with TypeScript
- Tailwind CSS for styling
- Lucide React for icons
- Proxy configuration for API calls

### Adding New Agents
1. Create agent module in `backend/multi-agents/`
2. Import and add to orchestration in `orchestration.py`
3. Add corresponding API endpoint in `main.py`

## Troubleshooting

### Common Issues

1. **Port already in use**:
   - Backend: Change port in `start-backend.bat` (e.g., `--port 8001`)
   - Frontend: React will prompt to use different port

2. **CORS errors**:
   - Ensure backend is running on port 8000
   - Check CORS configuration in `main.py`

3. **Module import errors**:
   - Ensure you're in the correct directory
   - Check Python path and virtual environment

4. **Frontend build errors**:
   - Run `npm install` in frontend directory
   - Check Node.js version compatibility

### Logs and Debugging

- **Backend logs**: Check the terminal running the backend server
- **Frontend logs**: Check browser developer console
- **API testing**: Use http://localhost:8000/docs for interactive API testing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both frontend and backend
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
