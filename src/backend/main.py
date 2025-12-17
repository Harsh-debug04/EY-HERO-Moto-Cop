from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from .agents import run_simulation, trigger_ueba_alert

app = FastAPI(title="Vidyutt Backend", version="1.0")

# Enable CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class TelematicsData(BaseModel):
    vehicle_id: str
    engine_temp: float
    rpm: float

class SimulationResponse(BaseModel):
    status: str
    details: Dict

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Vidyutt Orchestrator API is Running"}

@app.post("/ingest/telematics")
def ingest_telematics(data: TelematicsData):
    """
    Receives sensor data. If anomaly detected, triggers the Agentic Workflow.
    """
    print(f"Received Data: {data}")

    # Run the agent workflow
    # In a real system, this would be async/background task
    result_state = run_simulation(engine_temp=data.engine_temp)

    if result_state.get("anomaly_detected"):
        return {
            "status": "ANOMALY_HANDLED",
            "diagnosis": result_state.get("diagnosis_result"),
            "action": "Appointment Booked" if result_state.get("appointment_booked") else "Customer Declined",
            "root_cause_analysis": result_state.get("rfa_data")
        }
    else:
        return {"status": "NORMAL", "message": "Vehicle parameters within healthy range."}

@app.get("/security/test-ueba")
def test_ueba():
    """
    Triggers the simulated security breach.
    """
    result = trigger_ueba_alert()
    return result

@app.get("/dashboard/stats")
def get_stats():
    """
    Returns mock stats for the dashboard.
    """
    return {
        "uptime": "98.2%",
        "critical_alerts": 14,
        "active_calls": 8,
        "service_bay_utilization": "85%"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
