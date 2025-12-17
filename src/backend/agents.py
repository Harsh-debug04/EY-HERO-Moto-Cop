from typing import TypedDict, Annotated, Literal, Dict
from langgraph.graph import StateGraph, END
import random
import time

# --- State Definition ---
class AgentState(TypedDict):
    vehicle_id: str
    telematics: Dict[str, float]
    anomaly_detected: bool
    diagnosis_result: str
    customer_engaged: bool
    appointment_booked: bool
    rfa_data: Dict
    messages: list

# --- Nodes (Agents) ---

def ingest_sensor_data(state: AgentState):
    """Simulates receiving data from Kafka."""
    print(f"\n[Ingest Agent] Processing Stream for Vehicle: {state['vehicle_id']}")
    # No logic here, just passing through as start node
    return state

def diagnosis_agent(state: AgentState):
    """
    Simulates the LSTM-Autoencoder.
    Rule-based mock: If engine_temp > 105, it's an anomaly.
    """
    telematics = state['telematics']
    print(f"[Diagnosis Agent] Analyzing Telematics: {telematics}")

    if telematics.get("engine_temp", 90) > 105:
        print("[Diagnosis Agent] 🚨 ANOMALY DETECTED. Probability of Failure: 88%")
        return {
            "anomaly_detected": True,
            "diagnosis_result": "Critical Water Pump Failure Risk"
        }
    else:
        print("[Diagnosis Agent] Status Normal.")
        return {"anomaly_detected": False}

def engagement_agent(state: AgentState):
    """
    Simulates the Voice Agent (S2S).
    Since this is a backend script, we simulate the 'Call' logic.
    """
    print(f"\n[Engagement Agent] 📞 Initiating Call to Owner of {state['vehicle_id']}...")
    time.sleep(1) # Simulate dialing

    # Simulate User Interaction (Mock)
    # In a real app, this would trigger the Vapi/Twilio call
    print("[Voice Bot] 'Hello, I noticed your engine temp is high. Can I book a service?'")

    # Mock Customer Acceptance
    customer_accepts = True # Hardcoded for happy path

    if customer_accepts:
        print("[Customer] 'Yes, please book it.'")
        return {"customer_engaged": True}
    else:
        print("[Customer] 'No, I'm busy.'")
        return {"customer_engaged": False}

def scheduling_agent(state: AgentState):
    """
    Simulates checking Calendar API and booking slot.
    """
    print("[Scheduling Agent] 📅 Checking Workshop Bay Availability...")
    time.sleep(0.5)

    # Mock UEBA Check
    # In the report, this agent is watched by UEBA.
    # We will simulate a legitimate action here.

    print("[Scheduling Agent] Slot Confirmed: Tuesday, 10:00 AM @ Indiranagar Hub.")
    return {"appointment_booked": True}

def manufacturing_agent(state: AgentState):
    """
    Simulates updating the Knowledge Graph.
    """
    print(f"[Manufacturing Agent] 🏭 Logging Failure: {state['diagnosis_result']}")
    print("[Manufacturing Agent] Correlating with Supplier Batch #992... Match Found.")
    return {"rfa_data": {"root_cause": "Supplier Batch #992", "component": "Water Pump"}}

def ueba_monitor(state: AgentState):
    """
    Simulates the Security Layer.
    We'll implement a separate function to 'attack' the system to show this working,
    but in the normal flow, it just monitors.
    """
    # Passive monitoring in the graph
    return {}

# --- Graph Construction ---

def build_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("ingest", ingest_sensor_data)
    workflow.add_node("diagnose", diagnosis_agent)
    workflow.add_node("engage", engagement_agent)
    workflow.add_node("schedule", scheduling_agent)
    workflow.add_node("manufacturing", manufacturing_agent)

    # Add Edges
    workflow.set_entry_point("ingest")
    workflow.add_edge("ingest", "diagnose")

    def check_anomaly(state):
        return "engage" if state["anomaly_detected"] else END

    workflow.add_conditional_edges(
        "diagnose",
        check_anomaly,
        {
            "engage": "engage",
            END: END
        }
    )

    def check_engagement(state):
        return "schedule" if state["customer_engaged"] else END

    workflow.add_conditional_edges(
        "engage",
        check_engagement,
        {
            "schedule": "schedule",
            END: END
        }
    )

    # Parallel path: Diagnose -> Manufacturing (Fire and forget style, but here sequential for simplicity)
    workflow.add_edge("diagnose", "manufacturing")

    # Re-route: Manufacturing -> End (It's a side process)
    workflow.add_edge("manufacturing", END)

    # Schedule -> End
    workflow.add_edge("schedule", END)

    app = workflow.compile()
    return app

# --- Simulation Helper ---
def run_simulation(engine_temp=110):
    app = build_graph()
    initial_state = {
        "vehicle_id": "KA-05-MJ-2023",
        "telematics": {"engine_temp": engine_temp, "rpm": 3000},
        "anomaly_detected": False,
        "diagnosis_result": "",
        "customer_engaged": False,
        "appointment_booked": False,
        "rfa_data": {},
        "messages": []
    }

    print("--- STARTING VIDYUTT ORCHESTRATION ---")
    result = app.invoke(initial_state)
    print("\n--- WORKFLOW COMPLETE ---")
    return result

# --- Security Test Helper ---
def trigger_ueba_alert():
    """
    Simulates the specific 'UEBA ALERT' scenario from the report.
    """
    print("\n[Security Test] ⚠️  Simulating Unauthorized Access...")
    print("[Scheduling Agent] Attempting to read 'passwords.txt' (OUT OF SCOPE)...")

    # Logic simulating UEBA interception
    allowed_actions = ["read_calendar", "write_appointment"]
    attempted_action = "read_file_system"

    if attempted_action not in allowed_actions:
        print("\033[91m[UEBA ALERT] UNAUTHORIZED ACCESS BLOCKED. AGENT QUARANTINED.\033[0m")
        return {"status": "BLOCKED", "agent": "Scheduling Agent"}
    return {"status": "ALLOWED"}

if __name__ == "__main__":
    # Test Run
    run_simulation(engine_temp=115)
    trigger_ueba_alert()
