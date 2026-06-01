from __future__ import annotations

import numpy as np


def regression_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    error = predicted - actual

    rmse = float(np.sqrt(np.mean(error**2)))
    mae = float(np.mean(np.abs(error)))
    denominator = np.where(np.abs(actual) < 1e-9, 1, np.abs(actual))
    mape = float(np.mean(np.abs(error / denominator)) * 100)

    if len(actual) > 1:
        actual_direction = np.sign(np.diff(actual))
        predicted_direction = np.sign(np.diff(predicted))
        direction_accuracy = float(np.mean(actual_direction == predicted_direction) * 100)
    else:
        direction_accuracy = 0.0

    return {
        "rmse": round(rmse, 4),
        "mae": round(mae, 4),
        "mape": round(mape, 4),
        "direction_accuracy": round(direction_accuracy, 2),
    }
