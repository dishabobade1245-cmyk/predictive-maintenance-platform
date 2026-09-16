import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    layout="wide"
)


st.title("🏭 Predictive Maintenance Dashboard")
st.write("AI-powered equipment health and maintenance monitoring")


# --------------------------------------------------
# Dashboard Summary
# --------------------------------------------------

summary_response = requests.get(f"{API_URL}/dashboard/summary")

if summary_response.status_code == 200:

    summary = summary_response.json()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Equipment", summary["total_equipment"])
    col2.metric("Total Readings", summary["total_readings"])
    col3.metric("High Risk", summary["high_risk"])
    col4.metric("Low Risk", summary["low_risk"])

else:
    st.error("Unable to connect to the Predictive Maintenance API.")
    st.stop()


# --------------------------------------------------
# Risk Distribution
# --------------------------------------------------

st.subheader("Risk Distribution")

risk_data = {
    "High Risk": summary["high_risk"],
    "Medium Risk": summary["medium_risk"],
    "Low Risk": summary["low_risk"]
}

st.bar_chart(risk_data)


st.divider()


# --------------------------------------------------
# Equipment
# --------------------------------------------------

st.subheader("Equipment")

equipment_response = requests.get(f"{API_URL}/equipment")

if equipment_response.status_code == 200:

    equipment = equipment_response.json()

    if equipment:

        equipment_options = {
            f"{machine['equipment_name']} (Type: {machine['equipment_type']})":
            machine["id"]
            for machine in equipment
        }

        selected_machine = st.selectbox(
            "Select Equipment",
            list(equipment_options.keys())
        )

        selected_equipment_id = equipment_options[selected_machine]

        st.write(
            f"Selected Equipment ID: **{selected_equipment_id}**"
        )

    else:
        st.info("No equipment available.")
        st.stop()

else:
    st.error("Unable to retrieve equipment information.")
    st.stop()


st.divider()


# --------------------------------------------------
# Selected Equipment History
# --------------------------------------------------

st.subheader("Selected Equipment History")

history_response = requests.get(
    f"{API_URL}/equipment/{selected_equipment_id}/readings"
)

if history_response.status_code == 200:

    history = history_response.json()

    if history:

        st.dataframe(
            history,
            use_container_width=True
        )

                # --------------------------------------------------
        # Sensor Trends
        # --------------------------------------------------

        st.subheader("Sensor Trends")

        trend_data = {
            "Air Temperature (K)": [
                reading["air_temperature"] for reading in history
            ],
            "Process Temperature (K)": [
                reading["process_temperature"] for reading in history
            ],
            "Rotational Speed (rpm)": [
                reading["rotational_speed"] for reading in history
            ],
            "Torque (Nm)": [
                reading["torque"] for reading in history
            ],
            "Tool Wear (min)": [
                reading["tool_wear"] for reading in history
            ]
        }

        st.line_chart(trend_data)

        # Latest Equipment Status
        latest = history[0]

        st.subheader("Latest Equipment Status")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Air Temperature",
            f"{latest['air_temperature']} K"
        )

        col2.metric(
            "Process Temperature",
            f"{latest['process_temperature']} K"
        )

        col3.metric(
            "Rotational Speed",
            f"{latest['rotational_speed']} rpm"
        )

        col4.metric(
            "Torque",
            f"{latest['torque']} Nm"
        )

        col5, col6, col7 = st.columns(3)

        col5.metric(
            "Tool Wear",
            f"{latest['tool_wear']} min"
        )

        col6.metric(
            "Failure Probability",
            f"{latest['failure_probability']:.2%}"
        )

        col7.metric(
            "Risk Level",
            latest["risk_level"]
        )

        st.write(
            "**Maintenance Recommendation:**",
            latest["maintenance_recommendation"]
        )

    else:
        st.info("No readings available for this equipment.")

else:
    st.error("Unable to retrieve equipment history.")


st.divider()


# --------------------------------------------------
# Complete Prediction History
# --------------------------------------------------

st.subheader("Prediction History")

readings_response = requests.get(f"{API_URL}/readings")

if readings_response.status_code == 200:

    readings = readings_response.json()

    if readings:

        st.dataframe(
            readings,
            use_container_width=True
        )

    else:
        st.info("No prediction records available.")

else:
    st.error("Unable to retrieve prediction history.")

# Model Monitoring
st.divider()
st.subheader("🔍 Model Monitoring")

import streamlit.components.v1 as components
from pathlib import Path

report_path = Path("models/data_drift_report.html")

if report_path.exists():
    with open(report_path, "r", encoding="utf-8") as file:
        report_html = file.read()

    components.html(
        report_html,
        height=800,
        scrolling=True
    )
else:
    st.info("No monitoring report available yet.")