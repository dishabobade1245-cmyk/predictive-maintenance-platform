import pandas as pd

from src.predict import predict_failure


def test_prediction_output():
    data = pd.DataFrame([{
        "Type": "M",
        "Air temperature [K]": 300.0,
        "Process temperature [K]": 310.0,
        "Rotational speed [rpm]": 1500.0,
        "Torque [Nm]": 45.0,
        "Tool wear [min]": 120.0
    }])

    result = predict_failure(data)

    assert len(result) == 1
    assert "failure_prediction" in result[0]
    assert "failure_probability" in result[0]
    assert "risk_level" in result[0]
    assert "maintenance_recommendation" in result[0]

    assert result[0]["failure_prediction"] in [0, 1]
    assert 0.0 <= result[0]["failure_probability"] <= 1.0
    assert result[0]["risk_level"] in ["Low", "Medium", "High"]