import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000/predict"

df = pd.read_csv("data/ai4i2020.csv")

# Select 30 realistic sensor records
sample_data = df.sample(30, random_state=10)

success_count = 0

for _, row in sample_data.iterrows():

    payload = {
        "equipment_id": 1,
        "Type": row["Type"],
        "air_temperature": row["Air temperature [K]"],
        "process_temperature": row["Process temperature [K]"],
        "rotational_speed": row["Rotational speed [rpm]"],
        "torque": row["Torque [Nm]"],
        "tool_wear": row["Tool wear [min]"]
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        success_count += 1

print(f"Successfully generated {success_count} sensor readings.")