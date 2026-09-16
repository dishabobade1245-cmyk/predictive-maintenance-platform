import pandas as pd

from src.monitoring import generate_drift_report


# Load training/reference data
df = pd.read_csv("data/ai4i2020.csv")

# Sensor features we want to monitor
monitoring_columns = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

# Reference data = normal historical/training data
reference_data = df[monitoring_columns].sample(
    1000,
    random_state=42
)

# Create simulated current production data
current_data = reference_data.copy()

# Simulate a change in torque distribution
current_data["Torque [Nm]"] = current_data["Torque [Nm]"] * 1.20

# Generate data drift report
report = generate_drift_report(
    reference_data,
    current_data
)

# Save the monitoring report
report.save_html("models/data_drift_report.html")

print("Data drift report generated successfully.")
print("Saved to: models/data_drift_report.html")