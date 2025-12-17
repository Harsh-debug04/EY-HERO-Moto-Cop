from fastapi.testclient import TestClient
from src.backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Vidyutt Orchestrator API is Running"}

def test_ingest_normal_data():
    payload = {"vehicle_id": "TEST-01", "engine_temp": 90, "rpm": 2000}
    response = client.post("/ingest/telematics", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "NORMAL"

def test_ingest_anomaly_data():
    # Temp > 105 triggers anomaly
    payload = {"vehicle_id": "TEST-02", "engine_temp": 115, "rpm": 3500}
    response = client.post("/ingest/telematics", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ANOMALY_HANDLED"
    assert response.json()["action"] == "Appointment Booked"

def test_ueba_alert():
    response = client.get("/security/test-ueba")
    assert response.status_code == 200
    assert response.json()["status"] == "BLOCKED"
