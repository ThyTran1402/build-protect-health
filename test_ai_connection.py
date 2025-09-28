"""
Simple test to verify AI agents connection
Run this after starting your backend to test the connection
"""

import requests
import json

def test_ai_agents_connection():
    """Test the AI agents API endpoint"""
    
    # Test data matching what the frontend sends
    test_data = {
        "transcript": "Patient came in for a routine diabetes checkup. Blood sugar levels have improved from 180 to 145 mg/dL. Continue current medication regimen. Schedule follow-up appointment in 3 months. Patient should monitor blood sugar daily.",
        "condition": "Type 2 Diabetes", 
        "visit_type": "Follow-up",
        "current_metrics": {
            "blood_sugar": 145,
            "weight": 185,
            "blood_pressure": "120/80",
            "heart_rate": 72
        },
        "prior_metrics": {
            "blood_sugar": 160,
            "weight": 190,
            "blood_pressure": "130/85", 
            "heart_rate": 75
        },
        "session_id": "test_session_123"
    }
    
    try:
        print("🔗 Testing AI Agents Connection...")
        print("=" * 50)
        
        # Make request to backend
        response = requests.post(
            "http://localhost:8000/api/agents/process",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS: AI Agents responded correctly!")
            print(f"\n📋 Tasks found: {len(result.get('tasks', []))}")
            print(f"🩺 Guidance provided: {'Yes' if result.get('guidance') else 'No'}")
            print(f"📄 Report generated: {'Yes' if result.get('report') else 'No'}")
            
            print("\n📝 Sample Tasks:")
            for i, task in enumerate(result.get('tasks', [])[:2]):
                print(f"   {i+1}. {task.get('title', 'No title')}")
                print(f"      Due: {task.get('due_date', 'No date')}")
                print(f"      Confidence: {int(task.get('confidence', 0) * 100)}%")
                
            print(f"\n✅ Your frontend will successfully connect to the AI agents!")
            
        else:
            print(f"❌ ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Cannot reach backend")
        print("💡 Make sure your backend is running:")
        print("   cd healthcare-agents/backend")
        print("   python -m uvicorn main:app --reload --port 8000")
        
    except requests.exceptions.Timeout:
        print("⏰ TIMEOUT: AI agents took too long to respond")
        print("💡 This might indicate an issue with the AI processing")
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    test_ai_agents_connection()