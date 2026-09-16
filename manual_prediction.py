import pandas as pd

from src.predict import predict_failure


# Sample machine data
machine = pd.DataFrame([{
    "Type": "M",
    "Air temperature [K]": 300.0,
    "Process temperature [K]": 310.0,
    "Rotational speed [rpm]": 1500,
    "Torque [Nm]": 45.0,
    "Tool wear [min]": 120
}])


# Make prediction
result = predict_failure(machine)

print("\nMachine Prediction:")
print("Failure Prediction:", result[0]["failure_prediction"])
print("Failure Probability:", result[0]["failure_probability"])
print("Risk Level:", result[0]["risk_level"])
print("Maintenance Recommendation:", result[0]["maintenance_recommendation"])