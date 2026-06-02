from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Iterator

from app.core.config import DATABASE_PATH


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                risk_category TEXT NOT NULL,
                obesity_risk_percentage REAL NOT NULL,
                confidence_score REAL NOT NULL,
                model_used TEXT NOT NULL,
                request_json TEXT NOT NULL,
                probabilities_json TEXT NOT NULL
            )
            """
        )


def save_prediction(
    request_payload: dict[str, object],
    risk_category: str,
    obesity_risk_percentage: float,
    confidence_score: float,
    model_used: str,
    probabilities: list[dict[str, float | str]],
) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO predictions (
                created_at,
                risk_category,
                obesity_risk_percentage,
                confidence_score,
                model_used,
                request_json,
                probabilities_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                risk_category,
                obesity_risk_percentage,
                confidence_score,
                model_used,
                json.dumps(request_payload),
                json.dumps(probabilities),
            ),
        )


def prediction_distribution() -> dict[str, int]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT risk_category, COUNT(*) AS count FROM predictions GROUP BY risk_category"
        ).fetchall()
    return {row["risk_category"]: int(row["count"]) for row in rows}


def recent_predictions(limit: int = 8) -> list[dict[str, object]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT created_at, risk_category, obesity_risk_percentage, confidence_score, model_used
            FROM predictions
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]
