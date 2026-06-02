from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from app.core.config import DATA_PATH, TARGET_COLUMN


def _risk_category(score: float) -> str:
    if score >= 1.35:
        return "High"
    if score >= 0.45:
        return "Moderate"
    return "Low"


def generate_synthetic_biomarker_dataset(
    path: Path = DATA_PATH,
    n_samples: int = 720,
    random_state: int = 42,
) -> pd.DataFrame:
    """Generate a reproducible academic demo dataset.

    The values are clinically plausible enough for a mini-project demo, but
    this is not a real diagnostic dataset.
    """

    rng = np.random.default_rng(random_state)

    age = rng.integers(18, 74, size=n_samples)
    gender = rng.choice(["Male", "Female", "Other"], size=n_samples, p=[0.48, 0.49, 0.03])
    height_cm = rng.normal(166, 9, size=n_samples).clip(145, 192)
    bmi = rng.normal(27.5, 5.9, size=n_samples).clip(16.8, 45.0)
    weight_kg = bmi * (height_cm / 100) ** 2

    waist_circumference_cm = (bmi * 2.35 + rng.normal(27, 7, size=n_samples)).clip(60, 136)
    systolic_bp = (108 + bmi * 1.2 + age * 0.18 + rng.normal(0, 9, size=n_samples)).clip(88, 188)
    diastolic_bp = (66 + bmi * 0.55 + rng.normal(0, 7, size=n_samples)).clip(52, 118)
    fasting_glucose = (78 + bmi * 1.15 + age * 0.12 + rng.normal(0, 10, size=n_samples)).clip(68, 210)
    hba1c = (4.6 + fasting_glucose / 140 + rng.normal(0, 0.25, size=n_samples)).clip(4.5, 9.8)
    triglycerides = (78 + bmi * 4.2 + rng.normal(0, 32, size=n_samples)).clip(50, 410)
    hdl = (61 - bmi * 0.62 + rng.normal(0, 7, size=n_samples)).clip(24, 82)
    ldl = (82 + bmi * 2.4 + rng.normal(0, 22, size=n_samples)).clip(55, 225)
    total_cholesterol = (ldl + hdl + triglycerides / 5 + rng.normal(0, 8, size=n_samples)).clip(130, 310)
    insulin_resistance = (1.2 + bmi * 0.11 + fasting_glucose * 0.012 + rng.normal(0, 0.55, size=n_samples)).clip(0.8, 8.2)

    retinal_arteriole = (158 - bmi * 0.9 - systolic_bp * 0.06 + rng.normal(0, 8, size=n_samples)).clip(92, 178)
    retinal_venule = (205 + bmi * 0.85 + triglycerides * 0.04 + rng.normal(0, 12, size=n_samples)).clip(165, 270)
    avr = (retinal_arteriole / retinal_venule).clip(0.42, 0.95)
    intraocular_pressure = (13.6 + bmi * 0.13 + rng.normal(0, 2.0, size=n_samples)).clip(9, 28)
    visual_acuity = (1.05 - age * 0.003 - bmi * 0.004 + rng.normal(0, 0.08, size=n_samples)).clip(0.35, 1.25)
    macular_thickness = (255 + fasting_glucose * 0.12 + rng.normal(0, 11, size=n_samples)).clip(220, 320)
    cup_disc_ratio = (0.31 + intraocular_pressure * 0.008 + rng.normal(0, 0.05, size=n_samples)).clip(0.18, 0.78)
    ocular_risk = (
        (1 - avr) * 42
        + (intraocular_pressure - 14) * 1.1
        + (1.0 - visual_acuity) * 12
        + rng.normal(0, 4, size=n_samples)
    ).clip(0, 60)

    risk_score = (
        (bmi - 25) * 0.14
        + (waist_circumference_cm - 88) * 0.025
        + (fasting_glucose - 100) * 0.012
        + (triglycerides - 150) * 0.004
        + (systolic_bp - 120) * 0.01
        + (insulin_resistance - 3.2) * 0.18
        + (ocular_risk - 20) * 0.025
        + rng.normal(0, 0.45, size=n_samples)
    )
    target = np.array([_risk_category(score) for score in risk_score])

    df = pd.DataFrame(
        {
            "patient_id": [f"P{index:04d}" for index in range(1, n_samples + 1)],
            "age": age,
            "gender": gender,
            "height_cm": height_cm.round(1),
            "weight_kg": weight_kg.round(1),
            "bmi": bmi.round(1),
            "waist_circumference_cm": waist_circumference_cm.round(1),
            "systolic_bp": systolic_bp.round(0),
            "diastolic_bp": diastolic_bp.round(0),
            "fasting_glucose_mg_dl": fasting_glucose.round(1),
            "hba1c_percent": hba1c.round(2),
            "total_cholesterol_mg_dl": total_cholesterol.round(1),
            "triglycerides_mg_dl": triglycerides.round(1),
            "hdl_mg_dl": hdl.round(1),
            "ldl_mg_dl": ldl.round(1),
            "insulin_resistance_index": insulin_resistance.round(2),
            "retinal_arteriole_diameter_um": retinal_arteriole.round(1),
            "retinal_venule_diameter_um": retinal_venule.round(1),
            "arteriole_venule_ratio": avr.round(3),
            "intraocular_pressure_mmhg": intraocular_pressure.round(1),
            "visual_acuity_score": visual_acuity.round(2),
            "macular_thickness_um": macular_thickness.round(1),
            "cup_disc_ratio": cup_disc_ratio.round(2),
            "ocular_risk_score": ocular_risk.round(1),
            TARGET_COLUMN: target,
        }
    )

    # A few realistic imperfections for the preprocessing pipeline to fix.
    missing_columns = [
        "bmi",
        "fasting_glucose_mg_dl",
        "total_cholesterol_mg_dl",
        "retinal_arteriole_diameter_um",
        "ocular_risk_score",
    ]
    for column in missing_columns:
        missing_index = rng.choice(df.index, size=max(4, n_samples // 55), replace=False)
        df.loc[missing_index, column] = np.nan

    outlier_index = rng.choice(df.index, size=max(3, n_samples // 90), replace=False)
    df.loc[outlier_index, "triglycerides_mg_dl"] *= 1.7
    df.loc[outlier_index, "systolic_bp"] += 28

    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def load_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the biomarker dataset, generating it when missing."""

    if not path.exists():
        return generate_synthetic_biomarker_dataset(path=path)
    return pd.read_csv(path)


if __name__ == "__main__":
    generated = generate_synthetic_biomarker_dataset()
    print(f"Generated {len(generated)} biomarker records at {DATA_PATH}")
