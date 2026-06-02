import { Activity, Database, Gauge, Stethoscope } from "lucide-react";
import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { RiskBadge } from "../components/RiskBadge";
import { SectionHeader } from "../components/SectionHeader";
import { StatCard } from "../components/StatCard";
import { getDashboard } from "../services/api";
import { DashboardSummary, RiskCategory } from "../types/api";

const riskColors: Record<RiskCategory, string> = {
  Low: "#2E7D32",
  Moderate: "#C47F00",
  High: "#D32F2F"
};

export function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);

  useEffect(() => {
    getDashboard().then(setSummary);
  }, []);

  if (!summary) {
    return <div className="loading-panel">Loading dashboard metrics...</div>;
  }

  const distributionData = Object.entries(summary.dataset_prediction_distribution).map(([category, count]) => ({
    category,
    count
  }));
  const totalDistribution = distributionData.reduce((total, item) => total + item.count, 0);
  const lowCount = summary.dataset_prediction_distribution.Low ?? 0;
  const moderateCount = summary.dataset_prediction_distribution.Moderate ?? 0;
  const highCount = summary.dataset_prediction_distribution.High ?? 0;
  const lowEnd = (lowCount / totalDistribution) * 100;
  const moderateEnd = lowEnd + (moderateCount / totalDistribution) * 100;
  const donutStyle = {
    background: `conic-gradient(${riskColors.Low} 0 ${lowEnd}%, ${riskColors.Moderate} ${lowEnd}% ${moderateEnd}%, ${riskColors.High} ${moderateEnd}% 100%)`
  };

  return (
    <div className="page-stack">
      <SectionHeader
        eyebrow="Clinical Research Dashboard"
        title="Obesity Biomarker Risk Overview"
        subtitle="Ocular and metabolic biomarker modeling summary for academic review."
      />

      <section className="stat-grid">
        <StatCard label="Dataset Records" value={summary.total_records} detail="Synthetic academic cohort" icon={<Database size={22} />} />
        <StatCard label="Average BMI" value={summary.average_bmi} detail="kg/m2" icon={<Gauge size={22} />} />
        <StatCard label="Best Model" value={summary.best_model} detail="Selected by F1 and ROC AUC" icon={<Activity size={22} />} />
        <StatCard label="Model Accuracy" value={`${Math.round(summary.model_accuracy * 100)}%`} detail="Holdout evaluation" icon={<Stethoscope size={22} />} />
      </section>

      <section className="dashboard-grid">
        <article className="panel">
          <h3>Prediction Distribution</h3>
          <div className="donut-wrap">
            <div className="donut-chart" style={donutStyle}>
              <div className="donut-center">
                <strong>{totalDistribution}</strong>
                <span>records</span>
              </div>
            </div>
          </div>
          <div className="legend-row">
            {distributionData.map((item) => (
              <span key={item.category}>
                <i style={{ background: riskColors[item.category as RiskCategory] }} />
                {item.category}: {item.count}
              </span>
            ))}
          </div>
        </article>

        <article className="panel">
          <h3>Risk Counts</h3>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={distributionData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="category" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                {distributionData.map((entry) => (
                  <Cell key={entry.category} fill={riskColors[entry.category as RiskCategory]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </article>
      </section>

      <article className="panel">
        <h3>Recent Prediction Log</h3>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>Risk</th>
                <th>Risk %</th>
                <th>Confidence</th>
                <th>Model</th>
              </tr>
            </thead>
            <tbody>
              {summary.recent_predictions.length === 0 ? (
                <tr>
                  <td colSpan={5}>No live predictions recorded yet.</td>
                </tr>
              ) : (
                summary.recent_predictions.map((row) => (
                  <tr key={`${row.created_at}-${row.obesity_risk_percentage}`}>
                    <td>{new Date(row.created_at).toLocaleString()}</td>
                    <td><RiskBadge risk={row.risk_category} /></td>
                    <td>{row.obesity_risk_percentage}%</td>
                    <td>{row.confidence_score}%</td>
                    <td>{row.model_used}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </article>
    </div>
  );
}
