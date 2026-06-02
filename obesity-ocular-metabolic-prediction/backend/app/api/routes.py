from __future__ import annotations

from fastapi import APIRouter

from app.models.schemas import PredictionInput, PredictionResponse
from app.services.analytics_service import analytics_payload, dashboard_summary, model_metrics, research_insights
from app.services.model_service import model_service

router = APIRouter(prefix="/api")


@router.get("/dashboard")
def get_dashboard() -> dict[str, object]:
    return dashboard_summary()


@router.post("/predict", response_model=PredictionResponse)
def predict_obesity_risk(payload: PredictionInput) -> PredictionResponse:
    return model_service.predict(payload)


@router.get("/analytics")
def get_analytics() -> dict[str, object]:
    return analytics_payload()


@router.get("/models")
def get_models() -> list[dict[str, object]]:
    return model_metrics()


@router.get("/insights")
def get_research_insights() -> dict[str, object]:
    return research_insights()
