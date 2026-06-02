# Methodology

## 1. Data Collection and Preparation

This mini-project uses a generated academic dataset because no real clinical dataset was provided. The generator creates clinically plausible ocular and metabolic biomarkers and intentionally inserts a small amount of missing data and outliers so the preprocessing pipeline can demonstrate realistic handling.

Input groups:

- Demographic: age, gender.
- Anthropometric: height, weight, BMI, waist circumference.
- Metabolic: glucose, HbA1c, cholesterol, triglycerides, HDL, LDL, blood pressure, insulin resistance.
- Ocular: retinal arteriole diameter, retinal venule diameter, arteriole-venule ratio, intraocular pressure, visual acuity, macular thickness, cup-disc ratio, ocular risk score.

## 2. Preprocessing

The preprocessing pipeline includes:

- Missing value handling using median imputation for numeric fields.
- Most-frequent imputation for categorical gender values.
- IQR-based clipping for numeric outliers.
- Standard scaling for numeric features.
- One-hot encoding for gender.

## 3. Feature Engineering

Additional features are created to capture clinically meaningful relationships:

- Pulse pressure = systolic BP - diastolic BP.
- Cholesterol ratio = total cholesterol / HDL.
- Waist-height ratio = waist circumference / height.
- Metabolic load score from BMI, glucose, triglycerides, and insulin resistance.
- Ocular vascular index from arteriole-venule ratio, ocular risk score, and intraocular pressure.

## 4. Model Training

Four classifiers are trained:

1. Logistic Regression.
2. Random Forest.
3. XGBoost.
4. Gradient Boosting.

The target is a three-class obesity risk label: Low, Moderate, and High. The data is split into train and test sets using stratified sampling to keep class proportions stable.

## 5. Evaluation

The project reports:

- Accuracy.
- Weighted precision.
- Weighted recall.
- Weighted F1 score.
- Weighted multiclass ROC AUC.

The best model is selected by weighted F1 score, with ROC AUC used as a secondary signal.

## 6. Explainability

The system attempts SHAP-based feature importance for the selected model. If the local runtime cannot compute SHAP for a specific estimator, the code falls back to model-derived feature importance. This keeps the demonstration reliable while still showing the intended explainability workflow.

## 7. Deployment Flow

The trained model is saved using Joblib. FastAPI loads the model artifact at startup, exposes prediction and analytics endpoints, and stores live predictions in SQLite. The React frontend consumes the API and displays the project as a clinical research dashboard.
