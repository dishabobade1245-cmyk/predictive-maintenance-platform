import pandas as pd

from src.monitoring import generate_drift_report
from src.database import get_connection


# Load historical reference data
df = pd.read_csv("data/ai4i2020.csv")

monitoring_columns = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

# Historical data = reference
reference_data = df[monitoring_columns].sample(
    1000,
    random_state=42
)

# Connect to PostgreSQL
connection = get_connection()
cursor = connection.cursor()

# Get actual sensor readings from the database
cursor.execute(
    """
    SELECT
        air_temperature AS "Air temperature [K]",
        process_temperature AS "Process temperature [K]",
        rotational_speed AS "Rotational speed [rpm]",
        torque AS "Torque [Nm]",
        tool_wear AS "Tool wear [min]"
    FROM sensor_readings
    ORDER BY recorded_at DESC
    """
)

rows = cursor.fetchall()

cursor.close()
connection.close()

# Convert database readings into a DataFrame
current_data = pd.DataFrame(
    rows,
    columns=monitoring_columns
)

if current_data.empty:
    print("No current sensor readings found in PostgreSQL.")
    exit()

# Generate drift report
report = generate_drift_report(
    reference_data,
    current_data
)

# Save report
report.save_html("models/data_drift_report.html")

print("Model monitoring completed.")
print("Data drift report saved to models/data_drift_report.html")
print()
print("Monitoring status:")
print("Reference records:", len(reference_data))
print("Current database records:", len(current_data))
print("Sensors monitored:", len(monitoring_columns))
print()
print("Current sensor data was retrieved from PostgreSQL.")