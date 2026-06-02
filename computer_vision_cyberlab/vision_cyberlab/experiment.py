from __future__ import annotations

import platform
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from .dataset import VisionDataset, make_dataset, save_image_grid
from .features import FeatureScaler, extract_filter_bank_features
from .metrics import classification_report
from .model import TinyVisionNet
from .report import (
    write_confusion_image,
    write_csv,
    write_json,
    write_prediction_mosaic,
    write_terminal_html,
    write_training_curve,
)


@dataclass(frozen=True)
class ExperimentResult:
    output_dir: Path
    metrics: dict
    run_log: str


def _split(dataset: VisionDataset, train_ratio: float = 0.75) -> tuple[VisionDataset, VisionDataset]:
    split = int(len(dataset.images) * train_ratio)
    return (
        VisionDataset(dataset.images[:split], dataset.labels[:split], dataset.label_names),
        VisionDataset(dataset.images[split:], dataset.labels[split:], dataset.label_names),
    )


def run_experiment(
    output_dir: str | Path = "outputs",
    samples_per_class: int = 120,
    image_size: int = 40,
    epochs: int = 90,
    seed: int = 27,
) -> ExperimentResult:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    dataset = make_dataset(samples_per_class=samples_per_class, image_size=image_size, seed=seed)
    train, test = _split(dataset)
    train_features_raw = extract_filter_bank_features(train.images)
    test_features_raw = extract_filter_bank_features(test.images)
    scaler = FeatureScaler.fit(train_features_raw)
    train_features = scaler.transform(train_features_raw)
    test_features = scaler.transform(test_features_raw)

    model = TinyVisionNet(
        input_dim=train_features.shape[1],
        hidden_units=72,
        class_count=len(dataset.label_names),
        seed=seed,
        learning_rate=0.055,
    ).fit(train_features, train.labels, epochs=epochs)

    probabilities = model.predict_proba(test_features)
    predicted = np.argmax(probabilities, axis=1)
    report = classification_report(test.labels, predicted, dataset.label_names)

    prediction_rows = []
    for index, (truth, guess, confidence) in enumerate(zip(test.labels, predicted, probabilities.max(axis=1))):
        prediction_rows.append(
            {
                "sample_id": index,
                "actual_id": int(truth),
                "actual": dataset.label_names[int(truth)],
                "predicted_id": int(guess),
                "predicted": dataset.label_names[int(guess)],
                "confidence": round(float(confidence), 5),
                "correct": bool(truth == guess),
            }
        )

    metrics = {
        "project": "Deep Learning for Computer Vision using Python and MATLAB",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": platform.python_version(),
        "samples": int(len(dataset.images)),
        "train_samples": int(len(train.images)),
        "test_samples": int(len(test.images)),
        "image_size": [image_size, image_size, 3],
        "labels": list(dataset.label_names),
        "class_counts": dataset.class_counts(),
        "feature_count": int(train_features.shape[1]),
        "filters": ["edge_x", "edge_y", "laplace", "soft_blur", "diagonal"],
        "model": {
            "name": "TinyVisionNet",
            "hidden_units": 72,
            "epochs": epochs,
            "final_train_accuracy": model.history[-1]["accuracy"],
            "final_train_loss": model.history[-1]["loss"],
        },
        "test_report": report,
    }

    write_json(output / "metrics.json", metrics)
    write_csv(output / "predictions.csv", pd.DataFrame(prediction_rows))
    write_csv(output / "training_curve.csv", pd.DataFrame(model.history))
    save_image_grid(output / "sample_grid.png", dataset)
    write_confusion_image(output / "confusion_matrix.png", report["confusion_matrix"], dataset.label_names)
    write_training_curve(output / "training_curve.png", model.history)
    write_prediction_mosaic(output / "prediction_mosaic.png", test.images, prediction_rows, dataset.label_names)

    lines = [
        "Deep Learning for Computer Vision using Python and MATLAB",
        "Python native run",
        f"Python: {platform.python_version()}",
        f"Samples: {len(dataset.images)}",
        f"Train samples: {len(train.images)}",
        f"Test samples: {len(test.images)}",
        f"Image size: {image_size}x{image_size}x3",
        f"Feature count: {train_features.shape[1]}",
        f"Model: TinyVisionNet hidden=72 epochs={epochs}",
        "",
        f"Test accuracy: {report['accuracy']:.2%}",
        f"Final train accuracy: {model.history[-1]['accuracy']:.2%}",
        f"Final train loss: {model.history[-1]['loss']}",
        "",
        "Class report:",
    ]
    for name, row in report["per_class"].items():
        lines.append(
            f"  {name}: precision={row['precision']:.2f} recall={row['recall']:.2f} support={row['support']}"
        )
    lines.extend(
        [
            "",
            "Generated files:",
            "  outputs/metrics.json",
            "  outputs/predictions.csv",
            "  outputs/training_curve.csv",
            "  outputs/sample_grid.png",
            "  outputs/confusion_matrix.png",
            "  outputs/training_curve.png",
            "  outputs/prediction_mosaic.png",
        ]
    )

    run_log = "\n".join(lines)
    (output / "run_log.txt").write_text(run_log + "\n", encoding="utf-8")
    write_terminal_html(output / "cli-output.html", "vision model run", run_log)
    return ExperimentResult(output, metrics, run_log)
