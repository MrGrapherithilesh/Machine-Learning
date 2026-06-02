export type RiskCategory = "Low" | "Moderate" | "High";

export interface DashboardSummary {
  total_records: number;
  average_bmi: number;
  dataset_prediction_distribution: Record<RiskCategory, number>;
  live_prediction_distribution: Partial<Record<RiskCategory, number>>;
  model_accuracy: number;
  best_model: string;
  recent_predictions: RecentPrediction[];
}

export interface RecentPrediction {
  created_at: string;
  risk_category: RiskCategory;
  obesity_risk_percentage: number;
  confidence_score: number;
  model_used: string;
}

export interface PredictionInput {
  age: number;
  gender: "Male" | "Female" | "Other";
  height_cm: number;
  weight_kg: number;
  bmi: number;
  waist_circumference_cm: number;
  systolic_bp: number;
  diastolic_bp: number;
  fasting_glucose_mg_dl: number;
  hba1c_percent: number;
  total_cholesterol_mg_dl: number;
  triglycerides_mg_dl: number;
  hdl_mg_dl: number;
  ldl_mg_dl: number;
  insulin_resistance_index: number;
  retinal_arteriole_diameter_um: number;
  retinal_venule_diameter_um: number;
  arteriole_venule_ratio: number;
  intraocular_pressure_mmhg: number;
  visual_acuity_score: number;
  macular_thickness_um: number;
  cup_disc_ratio: number;
  ocular_risk_score: number;
}

export interface PredictionResponse {
  risk_category: RiskCategory;
  obesity_risk_percentage: number;
  confidence_score: number;
  model_used: string;
  probabilities: Array<{ category: RiskCategory; probability: number }>;
  top_contributors: FeatureImportance[];
}

export interface FeatureImportance {
  feature: string;
  importance: number;
  method: string;
}

export interface AnalyticsPayload {
  feature_importance: FeatureImportance[];
  correlation_matrix: Array<Record<string, number | string>>;
  distributions: Array<Record<string, number | string>>;
}

export interface ModelMetric {
  model_name: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
  roc_auc: number;
}

export interface ResearchInsights {
  key_findings: string[];
  important_biomarkers: FeatureImportance[];
  dataset_statistics: Record<string, number | string | Record<string, number>>;
  student_notes: string[];
  mean_feature_importance: number;
}
