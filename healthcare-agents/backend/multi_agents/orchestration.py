"""
Healthcare Agents Orchestration using Google ADK and A2A
This module defines the multi-agent system for healthcare processing
"""

import asyncio
from typing import Dict, Any, List
from google.adk.core import Agent, State
from google.adk.agents import SequentialAgent, ParallelAgent
from google.adk.a2a import A2AAgent, AgentMessage
from google.genai import generative_models as genai

# Agent types for healthcare system
class IntakeAgent(A2AAgent):
    """Agent responsible for processing patient intake data"""
    
    def __init__(self, name: str = "intake_agent"):
        super().__init__(name)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def process(self, state: State) -> State:
        """Process transcript and extract key medical information"""
        transcript = state.get("transcript_snippet", "")
        
        if transcript:
            prompt = f"""
            Analyze this medical transcript and extract key information:
            
            Transcript: {transcript}
            
            Extract:
            1. Patient symptoms
            2. Medications mentioned
            3. Vital signs or measurements
            4. Doctor's recommendations
            5. Follow-up actions needed
            
            Return as structured JSON with clear categories.
            """
            
            try:
                response = await self.model.generate_content_async(prompt)
                state["intake_analysis"] = response.text
                state["intake_status"] = "completed"
            except Exception as e:
                state["intake_analysis"] = f"Error processing transcript: {str(e)}"
                state["intake_status"] = "error"
        
        return state

class CoachAgent(A2AAgent):
    """Agent responsible for pre-visit coaching and guidance"""
    
    def __init__(self, name: str = "coach_agent"):
        super().__init__(name)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def process(self, state: State) -> State:
        """Generate coaching recommendations based on condition and visit type"""
        condition = state.get("condition", "")
        visit_type = state.get("visit_type", "")
        intake_analysis = state.get("intake_analysis", "")
        
        if condition and visit_type:
            prompt = f"""
            Create pre-visit coaching guidance for a patient with:
            
            Condition: {condition}
            Visit Type: {visit_type}
            Previous Analysis: {intake_analysis}
            
            Provide JSON response with:
            1. "checklist": Array of items patient should bring/prepare
            2. "cautions": Array of important warnings or things to watch
            3. "questions_for_doctor": Array of suggested questions to ask
            
            Make it practical and specific to the condition and visit type.
            """
            
            try:
                response = await self.model.generate_content_async(prompt)
                # Parse the JSON response
                import json
                try:
                    coach_data = json.loads(response.text.strip())
                    state["coach_json"] = coach_data
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    state["coach_json"] = {
                        "checklist": ["Bring current medication list", "Prepare symptom timeline"],
                        "cautions": ["Monitor symptoms carefully", "Take medications as prescribed"],
                        "questions_for_doctor": ["How is my condition progressing?", "Any medication adjustments needed?"]
                    }
                state["coach_status"] = "completed"
            except Exception as e:
                state["coach_json"] = {
                    "checklist": [f"Error generating checklist: {str(e)}"],
                    "cautions": ["Contact healthcare provider if symptoms worsen"],
                    "questions_for_doctor": ["Discuss current symptoms with doctor"]
                }
                state["coach_status"] = "error"
        
        return state

class TaskExtractionAgent(A2AAgent):
    """Agent responsible for extracting actionable tasks from medical information"""
    
    def __init__(self, name: str = "task_agent"):
        super().__init__(name)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def process(self, state: State) -> State:
        """Extract actionable tasks from the medical analysis"""
        intake_analysis = state.get("intake_analysis", "")
        condition = state.get("condition", "")
        
        if intake_analysis or condition:
            prompt = f"""
            Extract actionable tasks from this medical information:
            
            Analysis: {intake_analysis}
            Condition: {condition}
            
            Return JSON array of tasks, each with:
            - "title": Clear, actionable task description
            - "due_date": Estimated due date (YYYY-MM-DD format)
            - "source": Where this task came from
            - "confidence": Confidence score 0.0-1.0
            
            Focus on tasks like: medication refills, lab tests, follow-up appointments, lifestyle changes.
            """
            
            try:
                response = await self.model.generate_content_async(prompt)
                import json
                try:
                    tasks = json.loads(response.text.strip())
                    state["extracted_tasks"] = tasks
                except json.JSONDecodeError:
                    # Fallback tasks
                    state["extracted_tasks"] = [
                        {
                            "title": "Schedule follow-up appointment",
                            "due_date": "2024-02-15",
                            "source": "Medical recommendation",
                            "confidence": 0.8
                        }
                    ]
                state["task_extraction_status"] = "completed"
            except Exception as e:
                state["extracted_tasks"] = [{
                    "title": f"Task extraction failed: {str(e)}",
                    "due_date": "2024-01-30",
                    "source": "System error",
                    "confidence": 0.0
                }]
                state["task_extraction_status"] = "error"
        
        return state

class ReportAgent(A2AAgent):
    """Agent responsible for generating comprehensive health reports"""
    
    def __init__(self, name: str = "report_agent"):
        super().__init__(name)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def process(self, state: State) -> State:
        """Generate comprehensive health report from all agent outputs"""
        intake_analysis = state.get("intake_analysis", "")
        coach_json = state.get("coach_json", {})
        extracted_tasks = state.get("extracted_tasks", [])
        condition = state.get("condition", "")
        
        prompt = f"""
        Generate a comprehensive health report based on:
        
        Condition: {condition}
        Medical Analysis: {intake_analysis}
        Coaching Guidance: {coach_json}
        Extracted Tasks: {extracted_tasks}
        
        Create a markdown-formatted report that includes:
        1. Executive Summary
        2. Key Findings
        3. Recommended Actions
        4. Next Steps
        5. Important Notes
        
        Make it professional but patient-friendly.
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            state["report_markdown"] = response.text
            state["report_status"] = "completed"
        except Exception as e:
            state["report_markdown"] = f"""
# Health Report

## Summary
Report generation encountered an error: {str(e)}

## Recommendations
- Continue following your healthcare provider's instructions
- Keep track of symptoms and medications
- Schedule regular check-ups as recommended

## Next Steps
- Contact your healthcare provider for personalized guidance
            """
            state["report_status"] = "error"
        
        return state

# Initialize individual agents
intake_agent = IntakeAgent()
coach_agent = CoachAgent()
task_agent = TaskExtractionAgent()
report_agent = ReportAgent()

# Create parallel processing for coach and task extraction
parallel_agents = ParallelAgent(
    name="parallel_processing",
    sub_agents=[coach_agent, task_agent]
)

# Full workflow: Intake -> Parallel (Coach + Tasks) -> Report
root_agent = SequentialAgent(
    name="healthcare_orchestrator", 
    sub_agents=[intake_agent, parallel_agents, report_agent]
)
