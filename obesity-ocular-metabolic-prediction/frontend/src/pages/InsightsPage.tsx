import { Microscope } from "lucide-react";
import { useEffect, useState } from "react";
import { SectionHeader } from "../components/SectionHeader";
import { getInsights } from "../services/api";
import { ResearchInsights } from "../types/api";

export function InsightsPage() {
  const [insights, setInsights] = useState<ResearchInsights | null>(null);

  useEffect(() => {
    getInsights().then(setInsights);
  }, []);

  if (!insights) {
    return <div className="loading-panel">Loading research insights...</div>;
  }

  return (
    <div className="page-stack">
      <SectionHeader
        eyebrow="Research Insights"
        title="Key Findings"
        subtitle="Interpretation notes prepared for academic presentation."
      />

      <section className="insight-grid">
        <article className="panel">
          <h3><Microscope size={20} /> Findings</h3>
          <ul className="finding-list">
            {insights.key_findings.map((finding) => (
              <li key={finding}>{finding}</li>
            ))}
          </ul>
        </article>

        <article className="panel">
          <h3>Important Biomarkers</h3>
          <div className="contributor-list">
            {insights.important_biomarkers.map((item) => (
              <div key={item.feature} className="contributor-row">
                <span>{item.feature.replaceAll("_", " ")}</span>
                <strong>{Math.round(item.importance * 100)}%</strong>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="dashboard-grid">
        <article className="panel">
          <h3>Dataset Statistics</h3>
          <div className="stat-list">
            {Object.entries(insights.dataset_statistics).map(([key, value]) => (
              <div key={key}>
                <span>{key.replaceAll("_", " ")}</span>
                <strong>{typeof value === "object" ? JSON.stringify(value) : value}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <h3>Student Research Notes</h3>
          <ul className="finding-list">
            {insights.student_notes.map((note) => (
              <li key={note}>{note}</li>
            ))}
          </ul>
        </article>
      </section>
    </div>
  );
}
