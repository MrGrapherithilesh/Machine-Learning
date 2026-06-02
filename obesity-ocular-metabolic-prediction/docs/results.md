# Results

The exact values are generated when the training script runs on the local dataset. The model metrics are saved to:

- `backend/artifacts/model_metrics.json`
- `backend/artifacts/feature_importance.json`

## Expected Output Format

| Model | Accuracy | Precision | Recall | F1 Score | ROC AUC |
| --- | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | generated | generated | generated | generated | generated |
| Random Forest | generated | generated | generated | generated | generated |
| XGBoost | generated | generated | generated | generated | generated |
| Gradient Boosting | generated | generated | generated | generated | generated |

## Interpretation Pattern

During testing, tree-based models usually perform better because the dataset contains non-linear relationships between BMI, glucose, triglycerides, ocular risk score, and retinal vessel indicators.

Commonly important biomarkers include:

- BMI.
- Waist circumference.
- Metabolic load score.
- Fasting glucose.
- Triglycerides.
- Ocular risk score.
- Arteriole-venule ratio.

## Screenshot Evidence

Final screenshots are saved in `screenshots/` after the app and tests are run:

- `dashboard.png`
- `prediction.png`
- `analytics.png`
- `model-comparison.png`
- `testing-phase.png`

## Limitations

- The dataset is synthetic.
- Ocular imaging is represented through extracted numeric biomarkers, not raw image processing.
- SHAP explanations depend on local package availability and model compatibility.
- The system is not intended for clinical diagnosis.
