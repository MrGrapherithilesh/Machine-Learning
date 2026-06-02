from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = PROJECT_ROOT / "backend"
DATA_DIR = PROJECT_ROOT / "data"
DATA_PATH = DATA_DIR / "biomarker_dataset.csv"
ARTIFACT_DIR = BACKEND_ROOT / "artifacts"
MODEL_ARTIFACT_PATH = ARTIFACT_DIR / "obesity_model_artifact.joblib"
METRICS_PATH = ARTIFACT_DIR / "model_metrics.json"
FEATURE_IMPORTANCE_PATH = ARTIFACT_DIR / "feature_importance.json"
DATABASE_PATH = BACKEND_ROOT / "obesity_predictions.db"

TARGET_COLUMN = "obesity_risk_level"

BASE_FEATURES = [
    "age",
    "gender",
    "height_cm",
    "weight_kg",
    "bmi",
    "waist_circumference_cm",
    "systolic_bp",
    "diastolic_bp",
    "fasting_glucose_mg_dl",
    "hba1c_percent",
    "total_cholesterol_mg_dl",
    "triglycerides_mg_dl",
    "hdl_mg_dl",
    "ldl_mg_dl",
    "insulin_resistance_index",
    "retinal_arteriole_diameter_um",
    "retinal_venule_diameter_um",
    "arteriole_venule_ratio",
    "intraocular_pressure_mmhg",
    "visual_acuity_score",
    "macular_thickness_um",
    "cup_disc_ratio",
    "ocular_risk_score",
]

ENGINEERED_FEATURES = [
    "pulse_pressure",
    "cholesterol_ratio",
    "waist_height_ratio",
    "metabolic_load_score",
    "ocular_vascular_index",
]

NUMERIC_FEATURES = [feature for feature in BASE_FEATURES if feature != "gender"] + ENGINEERED_FEATURES
CATEGORICAL_FEATURES = ["gender"]

RISK_ORDER = ["Low", "Moderate", "High"]
