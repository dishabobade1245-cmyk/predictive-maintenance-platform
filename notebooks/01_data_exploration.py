import pandas as pd
df = pd.read_csv("data/ai4i2020.csv")
print(df.head())
print(df.columns)
print(df.info())
print(df["Machine failure"].value_counts())
print(df.describe())
print(df["Type"].value_counts())
print(pd.crosstab(df["Type"] , df["Machine failure"]))
print(df.duplicated().sum())
# Features (input)
X = df[
    [
        "Type",
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]"
    ]
]

# Target (what we want to predict)
y = df["Machine failure"]

print("X shape:", X.shape)
print("y shape:", y.shape)
# Convert the Type column into numerical columns
X = pd.get_dummies(X, columns=["Type"], dtype=int)

print(X.head())
print("New X shape:", X.shape)
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Scaled training data:", X_train_scaled.shape)
print("Scaled testing data:", X_test_scaled.shape)
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(
    class_weight="balanced",
    random_state=42,
    max_iter=1000
)

model.fit(X_train_scaled, y_train)

print("Model training completed!")
# Make predictions on unseen test data
y_pred = model.predict(X_test_scaled)

# Get failure probabilities
y_prob = model.predict_proba(X_test_scaled)[:, 1]

print("Predictions:", y_pred[:10])
print("Failure probabilities:", y_prob[:10])
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)

print("Confusion Matrix:")
print(cm)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)
from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42
)

rf_model.fit(X_train, y_train)

print("Random Forest training completed!")

# Random Forest predictions
rf_pred = rf_model.predict(X_test)

print("Random Forest Predictions:", rf_pred[:10])

# Evaluate Random Forest
rf_cm = confusion_matrix(y_test, rf_pred)

rf_accuracy = accuracy_score(y_test, rf_pred)
rf_precision = precision_score(y_test, rf_pred)
rf_recall = recall_score(y_test, rf_pred)
rf_f1 = f1_score(y_test, rf_pred)

print("Random Forest Confusion Matrix:")
print(rf_cm)

print("Random Forest Accuracy:", rf_accuracy)
print("Random Forest Precision:", rf_precision)
print("Random Forest Recall:", rf_recall)
print("Random Forest F1-score:", rf_f1)

# Random Forest failure probabilities
rf_prob = rf_model.predict_proba(X_test)[:, 1]

print("Random Forest Failure Probabilities:", rf_prob[:10])

# Create a validation set from the training data
X_train_model, X_val, y_train_model, y_val = train_test_split(
    X_train,
    y_train,
    test_size=0.2,
    random_state=42,
    stratify=y_train
)

# Train Random Forest on the smaller training portion
rf_tuning_model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42
)

rf_tuning_model.fit(X_train_model, y_train_model)

# Get failure probabilities on validation data
val_prob = rf_tuning_model.predict_proba(X_val)[:, 1]

print("Validation data:", X_val.shape)
print("Validation probabilities:", val_prob[:10])

import numpy as np

thresholds = np.arange(0.1, 0.91, 0.05)

best_threshold = 0.5
best_f1 = 0

for threshold in thresholds:
    val_pred = (val_prob >= threshold).astype(int)

    precision = precision_score(y_val, val_pred)
    recall = recall_score(y_val, val_pred)
    f1 = f1_score(y_val, val_pred)

    print(
        f"Threshold: {threshold:.2f} | "
        f"Precision: {precision:.3f} | "
        f"Recall: {recall:.3f} | "
        f"F1: {f1:.3f}"
    )

    if f1 > best_f1:
        best_f1 = f1
        best_threshold = threshold

print("\nBest threshold:", best_threshold)
print("Best validation F1-score:", best_f1)

# Use the selected threshold on the final test data
final_threshold = best_threshold

rf_final_pred = (rf_prob >= final_threshold).astype(int)

# Final evaluation
final_cm = confusion_matrix(y_test, rf_final_pred)

final_accuracy = accuracy_score(y_test, rf_final_pred)
final_precision = precision_score(y_test, rf_final_pred)
final_recall = recall_score(y_test, rf_final_pred)
final_f1 = f1_score(y_test, rf_final_pred)

print("\nFinal Random Forest Results:")
print("Threshold:", final_threshold)
print("Confusion Matrix:")
print(final_cm)
print("Accuracy:", final_accuracy)
print("Precision:", final_precision)
print("Recall:", final_recall)
print("F1-score:", final_f1)
import tensorflow as tf

nn_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(8,)),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

nn_model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

print(nn_model.summary())
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

classes = np.unique(y_train)

weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=y_train
)

class_weights = dict(zip(classes, weights))

history = nn_model.fit(
    X_train_scaled,
    y_train,
    validation_split=0.2,
    epochs=30,
    batch_size=32,
    class_weight=class_weights,
    verbose=1
)

# Neural Network predictions
nn_prob = nn_model.predict(X_test_scaled, verbose=0).ravel()

# Convert probability into 0/1 prediction
nn_pred = (nn_prob >= 0.5).astype(int)

# Evaluation
nn_cm = confusion_matrix(y_test, nn_pred)

nn_accuracy = accuracy_score(y_test, nn_pred)
nn_precision = precision_score(y_test, nn_pred)
nn_recall = recall_score(y_test, nn_pred)
nn_f1 = f1_score(y_test, nn_pred)

print("\nNeural Network Results:")
print("Confusion Matrix:")
print(nn_cm)
print("Accuracy:", nn_accuracy)
print("Precision:", nn_precision)
print("Recall:", nn_recall)
print("F1-score:", nn_f1) 
# Recalculate Logistic Regression metrics
lr_accuracy = accuracy_score(y_test, y_pred)
lr_precision = precision_score(y_test, y_pred)
lr_recall = recall_score(y_test, y_pred)
lr_f1 = f1_score(y_test, y_pred)

# Model Comparison
comparison = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "Random Forest",
        "Neural Network"
    ],
    "Accuracy": [
        lr_accuracy,
        final_accuracy,
        nn_accuracy
    ],
    "Precision": [
        lr_precision,
        final_precision,
        nn_precision
    ],
    "Recall": [
        lr_recall,
        final_recall,
        nn_recall
    ],
    "F1-score": [
        lr_f1,
        final_f1,
        nn_f1
    ]
})

print("\nModel Comparison:")
print(comparison.to_string(index=False))
# Feature Engineering

X_engineered = df[
    [
        "Type",
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]"
    ]
].copy()

# Temperature difference
X_engineered["Temperature Difference"] = (
    X_engineered["Process temperature [K]"]
    - X_engineered["Air temperature [K]"]
)

# Mechanical load proxy
X_engineered["Mechanical Load"] = (
    X_engineered["Rotational speed [rpm]"]
    * X_engineered["Torque [Nm]"]
)

# Wear-load interaction
X_engineered["Wear Load"] = (
    X_engineered["Tool wear [min]"]
    * X_engineered["Torque [Nm]"]
)

# Encode machine type
X_engineered = pd.get_dummies(
    X_engineered,
    columns=["Type"],
    dtype=int
)

print("\nEngineered Features:")
print(X_engineered.head())
print("Engineered X shape:", X_engineered.shape)
# Train-test split for engineered features

X_eng_train, X_eng_test, y_eng_train, y_eng_test = train_test_split(
    X_engineered,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train Random Forest on engineered features

rf_engineered = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42
)

rf_engineered.fit(X_eng_train, y_eng_train)

# Predict probabilities
rf_eng_prob = rf_engineered.predict_proba(X_eng_test)[:, 1]

print("Engineered Random Forest training completed!")
print("Training data:", X_eng_train.shape)
print("Testing data:", X_eng_test.shape)
# Evaluate Engineered Random Forest

rf_eng_pred = (rf_eng_prob >= 0.45).astype(int)

rf_eng_cm = confusion_matrix(y_eng_test, rf_eng_pred)

rf_eng_accuracy = accuracy_score(y_eng_test, rf_eng_pred)
rf_eng_precision = precision_score(y_eng_test, rf_eng_pred)
rf_eng_recall = recall_score(y_eng_test, rf_eng_pred)
rf_eng_f1 = f1_score(y_eng_test, rf_eng_pred)

print("\nEngineered Random Forest Results:")
print("Confusion Matrix:")
print(rf_eng_cm)
print("Accuracy:", rf_eng_accuracy)
print("Precision:", rf_eng_precision)
print("Recall:", rf_eng_recall)
print("F1-score:", rf_eng_f1)
import joblib

# Save final model
joblib.dump(rf_engineered, "models/predictive_maintenance_model.pkl")

print("Final model saved successfully!")
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.feature_engineering import create_features
test_features = create_features(df)

print("\nReusable Feature Engineering Test:")
print(test_features.head())
print("Shape:", test_features.shape)
print("Columns:", test_features.columns.tolist())