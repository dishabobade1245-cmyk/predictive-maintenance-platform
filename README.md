# AI-Powered Predictive Maintenance & Equipment Intelligence Platform

An end-to-end machine learning platform that predicts equipment failures from sensor data, assigns equipment risk levels, provides maintenance recommendations, and monitors changes in sensor data distributions.

## 🚀 Live Demo

**Dashboard:** https://predictive-maintenance-dashboard-vghn.onrender.com

**API:** https://predictive-maintenance-platform-t70g.onrender.com

**API Documentation:** https://predictive-maintenance-platform-t70g.onrender.com/docs

---

## 📌 Project Overview

Unexpected equipment failures can lead to production downtime, maintenance costs, and operational losses.

This project uses machine learning to analyze equipment sensor readings and predict whether a machine is likely to fail.

The platform provides:

- Equipment failure prediction
- Failure probability
- Equipment risk classification
- Maintenance recommendations
- Historical sensor readings
- Equipment health monitoring
- Data drift monitoring
- REST APIs for predictions and equipment data
- Interactive monitoring dashboard

The complete system is containerized using Docker and deployed using Render.

---

## 🎯 Problem Statement

Traditional maintenance approaches often rely on fixed maintenance schedules or reacting after equipment failure.

The goal of this project is to build a predictive maintenance system that uses sensor data to identify potential equipment failures early and support proactive maintenance decisions.

---

## ✨ Key Features

### 1. Equipment Failure Prediction

The machine learning model analyzes:

- Air temperature
- Process temperature
- Rotational speed
- Torque
- Tool wear
- Equipment type

and predicts whether equipment failure is likely.

### 2. Failure Probability

The model provides a probability score between 0 and 1 representing the estimated likelihood of failure.

### 3. Risk Classification

Based on the predicted probability, equipment is classified into:

- **Low Risk**
- **Medium Risk**
- **High Risk**

### 4. Maintenance Recommendations

The system automatically generates recommendations based on the predicted risk level.

Examples:

- Continue normal operation
- Schedule maintenance soon
- Immediate maintenance recommended

### 5. Equipment Monitoring Dashboard

The Streamlit dashboard provides:

- Total equipment
- Total sensor readings
- Risk distribution
- Equipment history
- Sensor trends
- Latest equipment status
- Prediction history

### 6. Model Monitoring

Evidently is used to generate a data drift report by comparing historical reference sensor data with current sensor readings stored in PostgreSQL.

---

## 🧠 Machine Learning

### Dataset

The project uses the **AI4I 2020 Predictive Maintenance Dataset**.

The dataset contains equipment sensor measurements and machine failure information.

### Input Features

The following features are used for prediction:

- `Type`
- `Air temperature [K]`
- `Process temperature [K]`
- `Rotational speed [rpm]`
- `Torque [Nm]`
- `Tool wear [min]`

### Feature Engineering

Additional features were created to capture relationships between sensor values:

- Temperature Difference
- Mechanical Load
- Wear Load

The final model input contains 11 features after feature engineering and one-hot encoding.

### Models Evaluated

Multiple machine learning approaches were evaluated, including:

- Logistic Regression
- Random Forest
- Neural Network

Random Forest was selected for the deployed prediction pipeline.

### Class Imbalance

The dataset contains significantly more non-failure observations than failure observations.

Model evaluation therefore considers metrics such as:

- Precision
- Recall
- F1-score
- Accuracy

rather than relying only on accuracy.

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │   Sensor / Input     │
                 │       Data           │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Feature Engineering │
                 │   & Preprocessing    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   ML Prediction     │
                 │   Random Forest     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Risk Assessment &   │
                 │ Recommendations      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      FastAPI        │
                 │    REST Backend     │
                 └──────────┬──────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
       ┌─────────────────┐     ┌─────────────────┐
       │   PostgreSQL    │     │    Streamlit    │
       │    Database     │     │    Dashboard    │
       └─────────────────┘     └─────────────────┘
                                      │
                                      ▼
                             ┌─────────────────┐
                             │    Evidently    │
                             │ Data Monitoring │
                             └─────────────────┘