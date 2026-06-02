from __future__ import annotations

import numpy as np


def confusion_matrix(actual: np.ndarray, predicted: np.ndarray, class_count: int) -> np.ndarray:
    matrix = np.zeros((class_count, class_count), dtype=int)
    for truth, guess in zip(actual.astype(int), predicted.astype(int)):
        matrix[truth, guess] += 1
    return matrix


def classification_report(actual: np.ndarray, predicted: np.ndarray, label_names: tuple[str, ...]) -> dict:
    matrix = confusion_matrix(actual, predicted, len(label_names))
    report = {}
    for index, name in enumerate(label_names):
        true_positive = matrix[index, index]
        precision_denominator = matrix[:, index].sum()
        recall_denominator = matrix[index, :].sum()
        precision = true_positive / precision_denominator if precision_denominator else 0.0
        recall = true_positive / recall_denominator if recall_denominator else 0.0
        report[name] = {
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "support": int(recall_denominator),
        }

    return {
        "accuracy": round(float(np.mean(actual == predicted)), 4),
        "confusion_matrix": matrix.tolist(),
        "per_class": report,
    }
