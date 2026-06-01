from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


@dataclass(frozen=True)
class PriceData:
    frame: pd.DataFrame
    source: str


def _normalise_columns(frame: pd.DataFrame) -> pd.DataFrame:
    if isinstance(frame.columns, pd.MultiIndex):
        frame = frame.copy()
        frame.columns = [column[0] for column in frame.columns]

    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"price data is missing required columns: {missing}")

    cleaned = frame[REQUIRED_COLUMNS].copy()
    cleaned.index = pd.to_datetime(cleaned.index)
    cleaned = cleaned.sort_index()
    cleaned = cleaned.dropna()
    return cleaned


def load_yahoo_finance(
    symbol: str = "AAPL",
    start: str = "2018-01-01",
    end: Optional[str] = None,
) -> PriceData:
    """Download historical data from Yahoo Finance through yfinance."""

    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError("yfinance is not installed") from exc

    downloaded = yf.download(
        symbol,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
        threads=False,
    )
    if downloaded.empty:
        raise RuntimeError(f"Yahoo Finance returned no rows for {symbol}")

    return PriceData(_normalise_columns(downloaded), f"Yahoo Finance API ({symbol})")


def make_demo_aapl_like_data(days: int = 620, end_date: str | date = "2026-05-29") -> PriceData:
    """Create stable AAPL-like data so tests and demos run offline."""

    rng = np.random.default_rng(27)
    dates = pd.bdate_range(end=pd.Timestamp(end_date), periods=days)

    trend = np.linspace(0, 68, len(dates))
    market_cycles = 10 * np.sin(np.linspace(0, 9.5 * np.pi, len(dates)))
    shock = rng.normal(0, 1.9, len(dates)).cumsum()
    close = 148 + trend + market_cycles + shock
    close = np.maximum(close, 82)

    open_price = close + rng.normal(0, 1.25, len(dates))
    spread = np.abs(rng.normal(2.2, 0.8, len(dates)))
    high = np.maximum(open_price, close) + spread
    low = np.minimum(open_price, close) - spread
    volume_wave = 1 + 0.16 * np.sin(np.linspace(0, 7 * np.pi, len(dates)))
    volume = (78_000_000 * volume_wave + rng.normal(0, 4_500_000, len(dates))).astype(int)
    volume = np.maximum(volume, 24_000_000)

    frame = pd.DataFrame(
        {
            "Open": open_price,
            "High": high,
            "Low": low,
            "Close": close,
            "Volume": volume,
        },
        index=dates,
    )
    return PriceData(_normalise_columns(frame), "deterministic offline AAPL-like demo data")


def load_price_data(
    symbol: str = "AAPL",
    prefer_yahoo: bool = False,
    days: int = 620,
    start: str = "2018-01-01",
    end: Optional[str] = None,
) -> PriceData:
    if prefer_yahoo:
        try:
            return load_yahoo_finance(symbol=symbol, start=start, end=end)
        except Exception as exc:
            demo = make_demo_aapl_like_data(days=days)
            return PriceData(demo.frame, f"{demo.source} (Yahoo fallback: {exc})")

    return make_demo_aapl_like_data(days=days)
