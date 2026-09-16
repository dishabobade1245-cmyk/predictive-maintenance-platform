import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset


def generate_drift_report(reference_data, current_data):
    """
    Compare reference and current equipment data
    to detect changes in sensor data distribution.
    """

    report = Report(
        metrics=[
            DataDriftPreset()
        ]
    )

    result = report.run(
        reference_data=reference_data,
        current_data=current_data
    )

    return result