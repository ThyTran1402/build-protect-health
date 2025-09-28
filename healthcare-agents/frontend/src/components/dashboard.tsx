import React, { useState } from 'react';
import { Upload, Calendar, FileText, Activity, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

interface Task {
  title: string;
  due_date?: string;
  source: string;
  confidence: number;
}

interface CoachGuidance {
  checklist: string[];
  cautions: string[];
  questions_for_doctor: string[];
}

interface AgentResponse {
  tasks: Task[];
  guidance: CoachGuidance;
  report: string;
}

export default function HealthcareAgentDashboard() {
  const [transcript, setTranscript] = useState('');
  const [condition, setCondition] = useState('');
  const [visitType, setVisitType] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<AgentResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'tasks' | 'coach' | 'report'>('tasks');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!transcript || !condition || !visitType) return;
    
    setLoading(true);
    setResponse(null); // Clear previous results
    setError(null); // Clear previous errors

    try {
      // Call the backend AI agents API
      const result = await fetch('/api/agents/process', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          transcript,
          condition,
          visit_type: visitType,
          current_metrics: { 
            blood_sugar: 145, 
            weight: 185,
            blood_pressure: "120/80",
            heart_rate: 72
          },
          prior_metrics: { 
            blood_sugar: 160, 
            weight: 190,
            blood_pressure: "130/85",
            heart_rate: 75
          },
          session_id: `session_${Date.now()}` // Unique session ID
        })
      });

      if (!result.ok) {
        throw new Error(`HTTP error! status: ${result.status}`);
      }

      const data = await result.json();
      
      // Validate response structure
      if (data && (data.tasks || data.guidance || data.report)) {
        setResponse(data);
        setActiveTab('tasks');
        console.log('AI Agents Response:', data);
      } else {
        throw new Error('Invalid response format from AI agents');
      }

    } catch (error) {
      console.error('Error processing with AI agents:', error);
      
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      setError(`Failed to connect with AI agents: ${errorMessage}`);
      
      // Show user-friendly error message in response
      setResponse({
        tasks: [],
        guidance: {
          checklist: ['Unable to process transcript at this time'],
          cautions: ['Please check your connection and try again'],
          questions_for_doctor: ['Contact your healthcare provider directly if urgent']
        },
        report: `Connection Error: Could not reach AI agents service. ${errorMessage}`
      });
      setActiveTab('report');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-7xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
            <h1 className="text-3xl font-bold flex items-center gap-3">
              <Activity className="w-8 h-8" />
              Protect Health Dashboard
            </h1>
            <p className="text-blue-100 mt-2">Multi-agent system for patient care coordination</p>
          </div>

          <div className="p-6 bg-gray-50 border-b">
            <div className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Patient Condition
                  </label>
                  <input
                    type="text"
                    value={condition}
                    onChange={(e) => setCondition(e.target.value)}
                    placeholder="e.g., Type 2 Diabetes"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Visit Type
                  </label>
                  <select
                    value={visitType}
                    onChange={(e) => setVisitType(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select visit type</option>
                    <option value="Follow-up">Follow-up</option>
                    <option value="Initial">Initial Consultation</option>
                    <option value="Emergency">Emergency</option>
                    <option value="Routine">Routine Check-up</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Visit Transcript
                </label>
                <textarea
                  value={transcript}
                  onChange={(e) => setTranscript(e.target.value)}
                  placeholder="Paste the doctor's visit transcript here..."
                  rows={4}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <button
                onClick={handleSubmit}
                disabled={loading || !transcript || !condition || !visitType}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Upload className="w-5 h-5" />
                    Process with AI Agents
                  </>
                )}
              </button>
              
              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex items-center gap-2">
                    <AlertCircle className="w-5 h-5 text-red-500" />
                    <span className="text-red-700 font-medium">Error</span>
                  </div>
                  <p className="text-red-600 mt-1">{error}</p>
                </div>
              )}
            </div>
          </div>

          {response && (
            <div className="p-6">
              <div className="flex gap-2 mb-6 border-b">
                <button
                  onClick={() => setActiveTab('tasks')}
                  className={`px-4 py-2 font-medium transition-colors ${
                    activeTab === 'tasks'
                      ? 'text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <Calendar className="w-4 h-4 inline mr-2" />
                  Tasks ({response.tasks?.length || 0})
                </button>
                <button
                  onClick={() => setActiveTab('coach')}
                  className={`px-4 py-2 font-medium transition-colors ${
                    activeTab === 'coach'
                      ? 'text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <CheckCircle className="w-4 h-4 inline mr-2" />
                  Pre-Visit Coaching
                </button>
                <button
                  onClick={() => setActiveTab('report')}
                  className={`px-4 py-2 font-medium transition-colors ${
                    activeTab === 'report'
                      ? 'text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <FileText className="w-4 h-4 inline mr-2" />
                  Health Report
                </button>
              </div>

              {activeTab === 'tasks' && (
                <div className="space-y-3">
                  <h3 className="text-xl font-bold text-gray-800 mb-4">Extracted Tasks</h3>
                  {response.tasks?.map((task, idx) => (
                    <div key={idx} className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-lg">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="font-semibold text-gray-800">{task.title}</h4>
                          {task.due_date && (
                            <p className="text-sm text-gray-600 mt-1">Due: {task.due_date}</p>
                          )}
                          <p className="text-xs text-gray-500 mt-1">Source: {task.source}</p>
                        </div>
                        <div className="ml-4">
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            {Math.round(task.confidence * 100)}% confidence
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'coach' && response.guidance && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-xl font-bold text-gray-800 mb-3">Pre-Visit Checklist</h3>
                    <ul className="space-y-2">
                      {response.guidance.checklist?.map((item, idx) => (
                        <li key={idx} className="flex items-start gap-2">
                          <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-700">{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-800 mb-3">Important Cautions</h3>
                    <ul className="space-y-2">
                      {response.guidance.cautions?.map((item, idx) => (
                        <li key={idx} className="flex items-start gap-2">
                          <AlertCircle className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-700">{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-800 mb-3">Questions for Your Doctor</h3>
                    <ul className="space-y-2">
                      {response.guidance.questions_for_doctor?.map((item, idx) => (
                        <li key={idx} className="bg-purple-50 p-3 rounded-lg text-gray-700">
                          {idx + 1}. {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              {activeTab === 'report' && (
                <div className="prose max-w-none">
                  <div className="bg-gradient-to-r from-indigo-50 to-blue-50 p-6 rounded-lg">
                    <div className="whitespace-pre-wrap text-gray-700">
                      {response.report || 'No report available'}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}