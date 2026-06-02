from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    age: int = Field(..., ge=18, le=90)
    gender: Literal["Male", "Female", "Other"]
    height_cm: float = Field(..., ge=120, le=220)
    weight_kg: float = Field(..., ge=35, le=180)
    bmi: float = Field(..., ge=12, le=60)
    waist_circumference_cm: float = Field(..., ge=45, le=170)
    systolic_bp: float = Field(..., ge=70, le=230)
    diastolic_bp: float = Field(..., ge=40, le=140)
    fasting_glucose_mg_dl: float = Field(..., ge=50, le=300)
    hba1c_percent: float = Field(..., ge=3.5, le=14)
    total_cholesterol_mg_dl: float = Field(..., ge=80, le=420)
    triglycerides_mg_dl: float = Field(..., ge=30, le=650)
    hdl_mg_dl: float = Field(..., ge=15, le=120)
    ldl_mg_dl: float = Field(..., ge=30, le=300)
    insulin_resistance_index: float = Field(..., ge=0.2, le=12)
    retinal_arteriole_diameter_um: float = Field(..., ge=70, le=220)
    retinal_venule_diameter_um: float = Field(..., ge=130, le=320)
    arteriole_venule_ratio: float = Field(..., ge=0.3, le=1.2)
    intraocular_pressure_mmhg: float = Field(..., ge=5, le=40)
    visual_acuity_score: float = Field(..., ge=0.1, le=1.5)
    macular_thickness_um: float = Field(..., ge=180, le=380)
    cup_disc_ratio: float = Field(..., ge=0.1, le=0.95)
    ocular_risk_score: float = Field(..., ge=0, le=100)


class ProbabilityItem(BaseModel):
    category: str
    probability: float


class PredictionResponse(BaseModel):
    risk_category: str
    obesity_risk_percentage: float
    confidence_score: float
    model_used: str
    probabilities: list[ProbabilityItem]
    top_contributors: list[dict[str, float | str]]


class MetricResponse(BaseModel):
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
