import joblib

from .feature_engineering import create_features


# Load trained model
model = joblib.load("models/predictive_maintenance_model.pkl")


def predict_failure(data):
    """
    Predict machine failure risk and maintenance recommendation.
    """

    features = create_features(data)

    probability = model.predict_proba(features)[:, 1]

    prediction = (probability >= 0.45).astype(int)

    results = []

    for pred, prob in zip(prediction, probability):

        if prob >= 0.70:
            risk_level = "High"
            recommendation = "Immediate maintenance recommended."

        elif prob >= 0.45:
            risk_level = "Medium"
            recommendation = "Schedule maintenance soon."

        else:
            risk_level = "Low"
            recommendation = "Continue normal operation."

        results.append({
            "failure_prediction": int(pred),
            "failure_probability": float(prob),
            "risk_level": risk_level,
            "maintenance_recommendation": recommendation
        })

    return results