from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

from src.predict import predict_failure
from src.database import get_connection


app = FastAPI(title="Predictive Maintenance API")


class MachineData(BaseModel):
    equipment_id: int
    Type: str
    air_temperature: float
    process_temperature: float
    rotational_speed: float
    torque: float
    tool_wear: float


@app.get("/")
def home():
    return {
        "message": "Predictive Maintenance API is running"
    }


@app.post("/predict")
def predict(machine: MachineData):

    connection = None

    try:
        data = pd.DataFrame([{
            "Type": machine.Type,
            "Air temperature [K]": machine.air_temperature,
            "Process temperature [K]": machine.process_temperature,
            "Rotational speed [rpm]": machine.rotational_speed,
            "Torque [Nm]": machine.torque,
            "Tool wear [min]": machine.tool_wear
        }])

        result = predict_failure(data)
        prediction = result[0]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO sensor_readings (
                equipment_id,
                air_temperature,
                process_temperature,
                rotational_speed,
                torque,
                tool_wear,
                failure_prediction,
                failure_probability,
                risk_level,
                maintenance_recommendation
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                machine.equipment_id,
                machine.air_temperature,
                machine.process_temperature,
                machine.rotational_speed,
                machine.torque,
                machine.tool_wear,
                prediction["failure_prediction"],
                prediction["failure_probability"],
                prediction["risk_level"],
                prediction["maintenance_recommendation"]
            )
        )

        connection.commit()
        cursor.close()
        connection.close()

        return prediction

    except Exception as error:

        if connection:
            connection.rollback()
            connection.close()

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )


@app.get("/readings")
def get_readings():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            equipment_id,
            air_temperature,
            process_temperature,
            rotational_speed,
            torque,
            tool_wear,
            failure_prediction,
            failure_probability,
            risk_level,
            maintenance_recommendation,
            recorded_at
        FROM sensor_readings
        ORDER BY recorded_at DESC
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    readings = []

    for row in rows:
        readings.append({
            "id": row[0],
            "equipment_id": row[1],
            "air_temperature": row[2],
            "process_temperature": row[3],
            "rotational_speed": row[4],
            "torque": row[5],
            "tool_wear": row[6],
            "failure_prediction": row[7],
            "failure_probability": row[8],
            "risk_level": row[9],
            "maintenance_recommendation": row[10],
            "recorded_at": row[11]
        })

    return readings


@app.get("/equipment")
def get_equipment():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            equipment_name,
            equipment_type,
            created_at
        FROM equipment
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    equipment_list = []

    for row in rows:
        equipment_list.append({
            "id": row[0],
            "equipment_name": row[1],
            "equipment_type": row[2],
            "created_at": row[3]
        })

    return equipment_list


@app.get("/equipment/{equipment_id}/readings")
def get_equipment_readings(equipment_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            equipment_id,
            air_temperature,
            process_temperature,
            rotational_speed,
            torque,
            tool_wear,
            failure_prediction,
            failure_probability,
            risk_level,
            maintenance_recommendation,
            recorded_at
        FROM sensor_readings
        WHERE equipment_id = %s
        ORDER BY recorded_at DESC
        """,
        (equipment_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    readings = []

    for row in rows:
        readings.append({
            "id": row[0],
            "equipment_id": row[1],
            "air_temperature": row[2],
            "process_temperature": row[3],
            "rotational_speed": row[4],
            "torque": row[5],
            "tool_wear": row[6],
            "failure_prediction": row[7],
            "failure_probability": row[8],
            "risk_level": row[9],
            "maintenance_recommendation": row[10],
            "recorded_at": row[11]
        })

    return readings


@app.get("/health")
def health_check():

    connection = None

    try:
        connection = get_connection()

        return {
            "status": "healthy",
            "database": "connected",
            "model": "loaded"
        }

    except Exception as error:

        return {
            "status": "unhealthy",
            "database": "disconnected",
            "model": "loaded",
            "error": str(error)
        }

    finally:
        if connection:
            connection.close()


@app.get("/dashboard/summary")
def dashboard_summary():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM equipment")
    total_equipment = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sensor_readings")
    total_readings = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM sensor_readings WHERE risk_level = 'High'"
    )
    high_risk = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM sensor_readings WHERE risk_level = 'Medium'"
    )
    medium_risk = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM sensor_readings WHERE risk_level = 'Low'"
    )
    low_risk = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return {
        "total_equipment": total_equipment,
        "total_readings": total_readings,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk
    }