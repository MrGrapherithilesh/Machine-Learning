from __future__ import annotations

import pandas as pd

from app.core.config import BASE_FEATURES


def input_to_frame(payload: dict[str, object]) -> pd.DataFrame:
    """Convert an API payload into the exact feature frame expected by the model."""

    return pd.DataFrame([{feature: payload[feature] for feature in BASE_FEATURES}])
