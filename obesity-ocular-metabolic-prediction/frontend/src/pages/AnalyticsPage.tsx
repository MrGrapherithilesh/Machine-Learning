import { useEffect, useState } from "react";
import { Fragment } from "react";
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { SectionHeader } from "../components/SectionHeader";
import { getAnalytics } from "../services/api";
import { AnalyticsPayload } from "../types/api";

export function AnalyticsPage() {
  const [analytics, setAnalytics] = useState<AnalyticsPayload | null>(null);

  useEffect(() => {
    getAnalytics().then(setAnalytics);
  }, []);

  if (!analytics) {
    return <div className="loading-panel">Loading analytics...</div>;
  }

  const featureData = analytics.feature_importance.map((item) => ({
    feature: item.feature.replaceAll("_", " "),
    importance: Number((item.importance * 100).toFixed(2))
  }));
  const matrixColumns = Object.keys(analytics.correlation_matrix[0] ?? {}).filter((key) => key !== "feature");

  return (
    <div className="page-stack">
      <SectionHeader
        eyebrow="Analytics"
        title="Feature Importance and Biomarker Patterns"
        subtitle="Model explainability and cohort-level biomarker relationships."
      />

      <section className="dashboard-grid">
        <article className="panel">
          <h3>Feature Ranking</h3>
          <ResponsiveContainer width="100%" height={340}>
            <BarChart data={featureData} layout="vertical" margin={{ left: 90 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" />
              <YAxis dataKey="feature" type="category" width={130} />
              <Tooltip />
              <Bar dataKey="importance" fill="#0F4C81" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </article>

        <article className="panel">
          <h3>Risk Group Distributions</h3>
          <ResponsiveContainer width="100%" height={340}>
            <BarChart data={analytics.distributions}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="feature" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="Low" fill="#2E7D32" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Moderate" fill="#C47F00" radius={[4, 4, 0, 0]} />
              <Bar dataKey="High" fill="#D32F2F" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </article>
      </section>

      <article className="panel">
        <h3>Correlation Matrix</h3>
        <div className="correlation-grid" style={{ gridTemplateColumns: `180px repeat(${matrixColumns.length}, minmax(92px, 1fr))` }}>
          <strong>Feature</strong>
          {matrixColumns.map((column) => <strong key={column}>{column.replaceAll("_", " ")}</strong>)}
          {analytics.correlation_matrix.map((row) => (
            <Fragment key={String(row.feature)}>
              <span key={`${row.feature}-label`}>{String(row.feature).replaceAll("_", " ")}</span>
              {matrixColumns.map((column) => {
                const value = Number(row[column]);
                const alpha = Math.min(Math.abs(value), 1);
                return (
                  <span
                    key={`${row.feature}-${column}`}
                    className="correlation-cell"
                    style={{ backgroundColor: `rgba(15, 76, 129, ${0.08 + alpha * 0.45})` }}
                  >
                    {value.toFixed(2)}
                  </span>
                );
              })}
            </Fragment>
          ))}
        </div>
      </article>
    </div>
  );
}
