from __future__ import annotations

import platform
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .data import load_price_data
from .features import build_feature_frame, make_sequences
from .metrics import regression_metrics
from .models import NumpyLSTMRegressor, NumpyRNNRegressor
from .report import write_json, write_prediction_chart, write_predictions, write_run_log


@dataclass(frozen=True)
class ExperimentResult:
    output_dir: Path
    metrics: dict
    predictions: pd.DataFrame
    run_log: str


def _split_index(total_rows: int, train_ratio: float) -> int:
    split = int(total_rows * train_ratio)
    split = max(split, 20)
    split = min(split, total_rows - 8)
    if split <= 0:
        raise ValueError("not enough sequences for train/test split")
    return split


def run_experiment(
    symbol: str = "AAPL",
    output_dir: str | Path = "outputs",
    prefer_yahoo: bool = False,
    window: int = 30,
    horizon: int = 1,
    days: int = 620,
    train_ratio: float = 0.8,
) -> ExperimentResult:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    price_data = load_price_data(symbol=symbol, prefer_yahoo=prefer_yahoo, days=days)
    features = build_feature_frame(price_data.frame)
    sequences = make_sequences(features, window=window, horizon=horizon)
    split = _split_index(len(sequences.x), train_ratio)

    x_train, x_test = sequences.x[:split], sequences.x[split:]
    y_train, y_test = sequences.y[:split], sequences.y[split:]
    test_dates = sequences.dates[split:]

    rnn = NumpyRNNRegressor(hidden_units=18, seed=27).fit(x_train, y_train)
    lstm = NumpyLSTMRegressor(hidden_units=22, seed=2701).fit(x_train, y_train)

    rnn_scaled = rnn.predict(x_test)
    lstm_scaled = lstm.predict(x_test)

    actual_close = sequences.scaler.inverse_column(y_test, "Close")
    rnn_close = sequences.scaler.inverse_column(rnn_scaled, "Close")
    lstm_close = sequences.scaler.inverse_column(lstm_scaled, "Close")

    predictions = pd.DataFrame(
        {
            "date": test_dates.strftime("%Y-%m-%d"),
            "actual_close": actual_close,
            "rnn_prediction": rnn_close,
            "lstm_prediction": lstm_close,
        }
    )

    model_metrics = {
        "rnn": regression_metrics(actual_close, rnn_close),
        "lstm": regression_metrics(actual_close, lstm_close),
    }
    latest = predictions.iloc[-1].to_dict()
    latest["lstm_gap"] = round(float(latest["lstm_prediction"] - latest["actual_close"]), 4)
    latest["rnn_gap"] = round(float(latest["rnn_prediction"] - latest["actual_close"]), 4)

    metrics = {
        "symbol": symbol.upper(),
        "source": price_data.source,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rows": int(len(price_data.frame)),
        "window": window,
        "horizon": horizon,
        "feature_columns": list(sequences.feature_columns),
        "train_sequences": int(len(x_train)),
        "test_sequences": int(len(x_test)),
        "models": model_metrics,
        "latest": latest,
    }

    write_json(output_path / "metrics.json", metrics)
    write_predictions(output_path / "predictions.csv", predictions)
    write_prediction_chart(output_path / "prediction_plot.png", predictions, model_key="lstm")

    log_lines = [
        "Stock Price Prediction using LSTM and RNN",
        f"Symbol: {symbol.upper()}",
        f"Source: {price_data.source}",
        f"Python: {platform.python_version()}",
        f"Rows: {len(price_data.frame)}",
        f"Window: {window}",
        f"Train sequences: {len(x_train)}",
        f"Test sequences: {len(x_test)}",
        "",
        "RNN metrics:",
        f"  RMSE: {model_metrics['rnn']['rmse']}",
        f"  MAE: {model_metrics['rnn']['mae']}",
        f"  MAPE: {model_metrics['rnn']['mape']}%",
        f"  Direction accuracy: {model_metrics['rnn']['direction_accuracy']}%",
        "",
        "LSTM metrics:",
        f"  RMSE: {model_metrics['lstm']['rmse']}",
        f"  MAE: {model_metrics['lstm']['mae']}",
        f"  MAPE: {model_metrics['lstm']['mape']}%",
        f"  Direction accuracy: {model_metrics['lstm']['direction_accuracy']}%",
        "",
        f"Latest actual close: {latest['actual_close']:.2f}",
        f"Latest RNN prediction: {latest['rnn_prediction']:.2f}",
        f"Latest LSTM prediction: {latest['lstm_prediction']:.2f}",
        "",
        "Generated files:",
        "  outputs/metrics.json",
        "  outputs/predictions.csv",
        "  outputs/prediction_plot.png",
    ]
    run_log = "\n".join(log_lines)
    write_run_log(output_path / "run_log.txt", log_lines)

    return ExperimentResult(output_path, metrics, predictions, run_log)
