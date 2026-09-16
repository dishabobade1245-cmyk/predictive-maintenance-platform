from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Predictive Maintenance API is running"


def test_predict_endpoint():
    payload = {
        "equipment_id": 1,
        "Type": "M",
        "air_temperature": 300.0,
        "process_temperature": 310.0,
        "rotational_speed": 1500.0,
        "torque": 45.0,
        "tool_wear": 120.0
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert "failure_prediction" in result
    assert "failure_probability" in result
    assert "risk_level" in result
    assert "maintenance_recommendation" in result

    assert result["failure_prediction"] in [0, 1]
    assert 0.0 <= result["failure_probability"] <= 1.0
    assert result["risk_level"] in ["Low", "Medium", "High"]