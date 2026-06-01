from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


def ema(series: pd.Series, span: int) -> pd.Series:
    if span < 2:
        raise ValueError("EMA span must be at least 2")
    return series.astype(float).ewm(span=span, adjust=False).mean()


def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    if window < 2:
        raise ValueError("RSI window must be at least 2")

    delta = series.astype(float).diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    average_gain = gain.rolling(window=window, min_periods=window).mean()
    average_loss = loss.rolling(window=window, min_periods=window).mean()
    relative_strength = average_gain / average_loss.replace(0, np.nan)
    value = 100 - (100 / (1 + relative_strength))
    return value.fillna(50).clip(0, 100)


def build_feature_frame(price_frame: pd.DataFrame) -> pd.DataFrame:
    close = price_frame["Close"].astype(float)
    volume = price_frame["Volume"].astype(float)

    frame = pd.DataFrame(index=price_frame.index)
    frame["Close"] = close
    frame["Return"] = close.pct_change().replace([np.inf, -np.inf], 0)
    frame["RSI"] = rsi(close)
    frame["EMA_12"] = ema(close, 12)
    frame["EMA_26"] = ema(close, 26)
    frame["Volume_Change"] = volume.pct_change().replace([np.inf, -np.inf], 0)

    return frame.dropna().copy()


@dataclass(frozen=True)
class MinMaxScaler:
    minimum: np.ndarray
    maximum: np.ndarray
    columns: tuple[str, ...]

    @classmethod
    def fit(cls, frame: pd.DataFrame) -> "MinMaxScaler":
        return cls(
            minimum=frame.min(axis=0).to_numpy(dtype=float),
            maximum=frame.max(axis=0).to_numpy(dtype=float),
            columns=tuple(frame.columns),
        )

    @property
    def scale(self) -> np.ndarray:
        scale = self.maximum - self.minimum
        scale[scale == 0] = 1
        return scale

    def transform_frame(self, frame: pd.DataFrame) -> pd.DataFrame:
        values = (frame.loc[:, self.columns].to_numpy(dtype=float) - self.minimum) / self.scale
        return pd.DataFrame(values, index=frame.index, columns=self.columns)

    def inverse_column(self, values: np.ndarray, column: str) -> np.ndarray:
        column_index = self.columns.index(column)
        return values * self.scale[column_index] + self.minimum[column_index]


@dataclass(frozen=True)
class SequenceDataset:
    x: np.ndarray
    y: np.ndarray
    dates: pd.DatetimeIndex
    scaler: MinMaxScaler
    feature_columns: tuple[str, ...]


def make_sequences(
    feature_frame: pd.DataFrame,
    window: int = 30,
    horizon: int = 1,
    target_column: str = "Close",
) -> SequenceDataset:
    if window < 3:
        raise ValueError("window must be at least 3")
    if horizon < 1:
        raise ValueError("horizon must be at least 1")
    if target_column not in feature_frame.columns:
        raise ValueError(f"{target_column} is not in feature frame")
    if len(feature_frame) <= window + horizon:
        raise ValueError("not enough rows to build time windows")

    scaler = MinMaxScaler.fit(feature_frame)
    scaled = scaler.transform_frame(feature_frame)
    values = scaled.to_numpy(dtype=float)
    target_index = scaled.columns.get_loc(target_column)

    x_rows: list[np.ndarray] = []
    y_rows: list[float] = []
    y_dates: list[pd.Timestamp] = []
    last_start = len(values) - window - horizon + 1

    for start in range(last_start):
        target_position = start + window + horizon - 1
        x_rows.append(values[start : start + window])
        y_rows.append(float(values[target_position, target_index]))
        y_dates.append(feature_frame.index[target_position])

    return SequenceDataset(
        x=np.asarray(x_rows, dtype=float),
        y=np.asarray(y_rows, dtype=float),
        dates=pd.DatetimeIndex(y_dates),
        scaler=scaler,
        feature_columns=tuple(scaled.columns),
    )
