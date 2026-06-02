# Future Scope

## Real Dataset Integration

The most important improvement is replacing the generated dataset with a real clinical or public-health dataset. This would require clear dataset documentation, privacy checks, and ethical approval if patient data is used.

## Retinal Image Feature Extraction

The next version can add computer vision preprocessing for fundus images:

- vessel segmentation,
- arteriole and venule diameter estimation,
- optic cup-disc ratio extraction,
- macular region measurements,
- retinal texture embeddings.

## Model Improvements

- Add probability calibration.
- Compare CatBoost and LightGBM.
- Use nested cross-validation.
- Add fairness analysis across age and gender groups.
- Add confidence intervals for metrics.

## Explainability Improvements

- Add per-patient SHAP waterfall plots.
- Add model decision cards for each prediction.
- Explain how ocular and metabolic features interact for high-risk predictions.

## Product Improvements

- Add authentication for clinical users.
- Add CSV upload for batch prediction.
- Add PDF report generation for academic demo submissions.
- Store model version and dataset version with every prediction.
