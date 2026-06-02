from __future__ import annotations

import joblib
import numpy as np

from app.core.config import MODEL_ARTIFACT_PATH
from app.db.database import save_prediction
from app.ml.prediction import input_to_frame
from app.ml.training import train_all_models
from app.models.schemas import PredictionInput, PredictionResponse


class ModelService:
    """Loads trained artifacts and serves model predictions."""

    def __init__(self) -> None:
        self._artifact: dict[str, object] | None = None

    @property
    def artifact(self) -> dict[str, object]:
        if self._artifact is None:
            if not MODEL_ARTIFACT_PATH.exists():
                self._artifact = train_all_models()
            else:
                self._artifact = joblib.load(MODEL_ARTIFACT_PATH)
        return self._artifact

    def reload(self) -> None:
        self._artifact = joblib.load(MODEL_ARTIFACT_PATH)

    def predict(self, payload: PredictionInput) -> PredictionResponse:
        artifact = self.artifact
        model = artifact["model"]
        classes = list(artifact["classes"])
        request_payload = payload.model_dump()
        feature_frame = input_to_frame(request_payload)

        probabilities = np.asarray(model.predict_proba(feature_frame)[0], dtype=float)
        predicted_index = int(np.argmax(probabilities))
        risk_category = str(classes[predicted_index])
        high_index = classes.index("High") if "High" in classes else predicted_index
        risk_percentage = round(float(probabilities[high_index] * 100), 2)
        confidence = round(float(probabilities[predicted_index] * 100), 2)
        probability_items = [
            {"category": str(category), "probability": round(float(probability * 100), 2)}
            for category, probability in zip(classes, probabilities, strict=False)
        ]

        top_contributors = artifact.get("feature_importance", [])[:6]

        save_prediction(
            request_payload=request_payload,
            risk_category=risk_category,
            obesity_risk_percentage=risk_percentage,
            confidence_score=confidence,
            model_used=str(artifact["best_model_name"]),
            probabilities=probability_items,
        )

        return PredictionResponse(
            risk_category=risk_category,
            obesity_risk_percentage=risk_percentage,
            confidence_score=confidence,
            model_used=str(artifact["best_model_name"]),
            probabilities=probability_items,
            top_contributors=top_contributors,
        )


model_service = ModelService()
