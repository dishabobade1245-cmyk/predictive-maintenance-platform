import pandas as pd


def create_features(data):
    """
    Create model-ready features from raw equipment data.
    """

    X = data[
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
    X["Temperature Difference"] = (
        X["Process temperature [K]"]
        - X["Air temperature [K]"]
    )

    # Mechanical load
    X["Mechanical Load"] = (
        X["Rotational speed [rpm]"]
        * X["Torque [Nm]"]
    )

    # Wear-load interaction
    X["Wear Load"] = (
        X["Tool wear [min]"]
        * X["Torque [Nm]"]
    )

    # One-hot encode machine type
    X = pd.get_dummies(
        X,
        columns=["Type"],
        dtype=int
    )

    # Ensure the same feature columns used during model training
    required_columns = [
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]",
        "Temperature Difference",
        "Mechanical Load",
        "Wear Load",
        "Type_H",
        "Type_L",
        "Type_M"
    ]

    X = X.reindex(
        columns=required_columns,
        fill_value=0
    )

    return X