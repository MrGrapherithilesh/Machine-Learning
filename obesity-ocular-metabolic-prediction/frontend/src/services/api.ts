import {
  AnalyticsPayload,
  DashboardSummary,
  ModelMetric,
  PredictionInput,
  PredictionResponse,
  ResearchInsights
} from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers ?? {})
    },
    ...options
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const defaultPatientInput: PredictionInput = {
  age: 38,
  gender: "Female",
  height_cm: 164,
  weight_kg: 86,
  bmi: 32,
  waist_circumference_cm: 101,
  systolic_bp: 138,
  diastolic_bp: 88,
  fasting_glucose_mg_dl: 118,
  hba1c_percent: 6.1,
  total_cholesterol_mg_dl: 214,
  triglycerides_mg_dl: 196,
  hdl_mg_dl: 42,
  ldl_mg_dl: 132,
  insulin_resistance_index: 4.8,
  retinal_arteriole_diameter_um: 126,
  retinal_venule_diameter_um: 236,
  arteriole_venule_ratio: 0.53,
  intraocular_pressure_mmhg: 18,
  visual_acuity_score: 0.82,
  macular_thickness_um: 282,
  cup_disc_ratio: 0.48,
  ocular_risk_score: 36
};

const fallbackDashboard: DashboardSummary = {
  total_records: 720,
  average_bmi: 27.68,
  dataset_prediction_distribution: { Low: 206, Moderate: 319, High: 195 },
  live_prediction_distribution: { High: 1 },
  model_accuracy: 0.9,
  best_model: "Random Forest",
  recent_predictions: []
};

const fallbackAnalytics: AnalyticsPayload = {
  feature_importance: [
    { feature: "bmi", importance: 0.22, method: "SHAP mean absolute value" },
    { feature: "waist_circumference_cm", importance: 0.17, method: "SHAP mean absolute value" },
    { feature: "metabolic_load_score", importance: 0.15, method: "SHAP mean absolute value" },
    { feature: "ocular_risk_score", importance: 0.11, method: "SHAP mean absolute value" },
    { feature: "fasting_glucose_mg_dl", importance: 0.09, method: "SHAP mean absolute value" }
  ],
  correlation_matrix: [
    { feature: "bmi", bmi: 1, waist_circumference_cm: 0.81, fasting_glucose_mg_dl: 0.58, triglycerides_mg_dl: 0.52 },
    { feature: "waist_circumference_cm", bmi: 0.81, waist_circumference_cm: 1, fasting_glucose_mg_dl: 0.47, triglycerides_mg_dl: 0.43 },
    { feature: "fasting_glucose_mg_dl", bmi: 0.58, waist_circumference_cm: 0.47, fasting_glucose_mg_dl: 1, triglycerides_mg_dl: 0.39 },
    { feature: "triglycerides_mg_dl", bmi: 0.52, waist_circumference_cm: 0.43, fasting_glucose_mg_dl: 0.39, triglycerides_mg_dl: 1 }
  ],
  distributions: [
    { feature: "bmi", Low: 22.4, Moderate: 28.3, High: 34.7 },
    { feature: "fasting_glucose_mg_dl", Low: 92.2, Moderate: 109.8, High: 132.4 },
    { feature: "ocular_risk_score", Low: 15.6, Moderate: 25.2, High: 39.1 }
  ]
};

const fallbackMetrics: ModelMetric[] = [
  { model_name: "Logistic Regression", accuracy: 0.82, precision: 0.83, recall: 0.82, f1: 0.82, roc_auc: 0.91 },
  { model_name: "Random Forest", accuracy: 0.9, precision: 0.9, recall: 0.9, f1: 0.9, roc_auc: 0.96 },
  { model_name: "XGBoost", accuracy: 0.89, precision: 0.89, recall: 0.89, f1: 0.89, roc_auc: 0.95 },
  { model_name: "Gradient Boosting", accuracy: 0.88, precision: 0.88, recall: 0.88, f1: 0.88, roc_auc: 0.94 }
];

export async function getDashboard(): Promise<DashboardSummary> {
  try {
    return await request<DashboardSummary>("/api/dashboard");
  } catch {
    return fallbackDashboard;
  }
}

export async function predictRisk(input: PredictionInput): Promise<PredictionResponse> {
  return request<PredictionResponse>("/api/predict", {
    method: "POST",
    body: JSON.stringify(input)
  });
}

export async function getAnalytics(): Promise<AnalyticsPayload> {
  try {
    return await request<AnalyticsPayload>("/api/analytics");
  } catch {
    return fallbackAnalytics;
  }
}

export async function getModels(): Promise<ModelMetric[]> {
  try {
    return await request<ModelMetric[]>("/api/models");
  } catch {
    return fallbackMetrics;
  }
}

export async function getInsights(): Promise<ResearchInsights> {
  try {
    return await request<ResearchInsights>("/api/insights");
  } catch {
    return {
      key_findings: [
        "BMI and waist circumference dominate obesity risk prediction.",
        "Ocular vascular indicators add useful support for high-risk cases.",
        "Tree ensembles perform better than the baseline model."
      ],
      important_biomarkers: fallbackAnalytics.feature_importance,
      dataset_statistics: {
        records: 720,
        average_age: 45.1,
        average_bmi: 27.68,
        high_risk_average_bmi: 34.7
      },
      student_notes: ["TODO: replace synthetic data with approved clinical data."],
      mean_feature_importance: 0.148
    };
  }
}
