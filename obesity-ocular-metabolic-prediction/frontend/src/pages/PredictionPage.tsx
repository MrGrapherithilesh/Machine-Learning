import { Calculator, Save } from "lucide-react";
import { FormEvent, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { RiskBadge } from "../components/RiskBadge";
import { SectionHeader } from "../components/SectionHeader";
import { defaultPatientInput, predictRisk } from "../services/api";
import { PredictionInput, PredictionResponse } from "../types/api";

type NumericFieldKey = Exclude<keyof PredictionInput, "gender">;

const numericFields: Array<{ key: NumericFieldKey; label: string; step?: number }> = [
  { key: "age", label: "Age" },
  { key: "height_cm", label: "Height (cm)", step: 0.1 },
  { key: "weight_kg", label: "Weight (kg)", step: 0.1 },
  { key: "bmi", label: "BMI", step: 0.1 },
  { key: "waist_circumference_cm", label: "Waist Circumference (cm)", step: 0.1 },
  { key: "systolic_bp", label: "Systolic BP" },
  { key: "diastolic_bp", label: "Diastolic BP" },
  { key: "fasting_glucose_mg_dl", label: "Glucose (mg/dL)", step: 0.1 },
  { key: "hba1c_percent", label: "HbA1c (%)", step: 0.1 },
  { key: "total_cholesterol_mg_dl", label: "Total Cholesterol", step: 0.1 },
  { key: "triglycerides_mg_dl", label: "Triglycerides", step: 0.1 },
  { key: "hdl_mg_dl", label: "HDL", step: 0.1 },
  { key: "ldl_mg_dl", label: "LDL", step: 0.1 },
  { key: "insulin_resistance_index", label: "Insulin Resistance", step: 0.1 },
  { key: "retinal_arteriole_diameter_um", label: "Retinal Arteriole (um)", step: 0.1 },
  { key: "retinal_venule_diameter_um", label: "Retinal Venule (um)", step: 0.1 },
  { key: "arteriole_venule_ratio", label: "AV Ratio", step: 0.01 },
  { key: "intraocular_pressure_mmhg", label: "Intraocular Pressure", step: 0.1 },
  { key: "visual_acuity_score", label: "Visual Acuity", step: 0.01 },
  { key: "macular_thickness_um", label: "Macular Thickness (um)", step: 0.1 },
  { key: "cup_disc_ratio", label: "Cup-Disc Ratio", step: 0.01 },
  { key: "ocular_risk_score", label: "Ocular Risk Score", step: 0.1 }
];

export function PredictionPage() {
  const [form, setForm] = useState<PredictionInput>(defaultPatientInput);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  function updateNumber(key: NumericFieldKey, value: string) {
    setForm((current) => ({ ...current, [key]: Number(value) }));
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setIsSubmitting(true);
    setError(null);
    try {
      const prediction = await predictRisk(form);
      setResult(prediction);
    } catch {
      setError("Prediction API is not available. Start the FastAPI backend on port 8000.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="page-stack">
      <SectionHeader
        eyebrow="Patient Prediction"
        title="Biomarker Risk Assessment"
        subtitle="Enter ocular and metabolic measurements to estimate obesity risk."
      />

      <section className="prediction-layout">
        <form className="panel prediction-form" onSubmit={handleSubmit}>
          <h3>Patient Biomarkers</h3>
          <label className="field">
            <span>Gender</span>
            <select value={form.gender} onChange={(event) => setForm((current) => ({ ...current, gender: event.target.value as PredictionInput["gender"] }))}>
              <option>Female</option>
              <option>Male</option>
              <option>Other</option>
            </select>
          </label>
          <div className="input-grid">
            {numericFields.map((field) => (
              <label className="field" key={field.key}>
                <span>{field.label}</span>
                <input
                  type="number"
                  value={form[field.key]}
                  step={field.step ?? 1}
                  onChange={(event) => updateNumber(field.key, event.target.value)}
                />
              </label>
            ))}
          </div>
          <button className="primary-button" type="submit" disabled={isSubmitting}>
            {isSubmitting ? <Calculator size={18} /> : <Save size={18} />}
            {isSubmitting ? "Analyzing" : "Predict Risk"}
          </button>
          {error ? <p className="error-text">{error}</p> : null}
        </form>

        <aside className="panel result-panel">
          <h3>Prediction Output</h3>
          {result ? (
            <>
              <div className="risk-summary">
                <RiskBadge risk={result.risk_category} />
                <strong>{result.obesity_risk_percentage}%</strong>
                <span>Confidence {result.confidence_score}% with {result.model_used}</span>
              </div>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={result.probabilities}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="category" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Bar dataKey="probability" fill="#0F4C81" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
              <div className="contributor-list">
                <h4>Top Biomarker Contributors</h4>
                {result.top_contributors.map((item) => (
                  <div key={item.feature} className="contributor-row">
                    <span>{item.feature}</span>
                    <strong>{Math.round(item.importance * 100)}%</strong>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <p className="muted">Submit a patient profile to view risk percentage, category, confidence, and biomarker contributors.</p>
          )}
        </aside>
      </section>
    </div>
  );
}
