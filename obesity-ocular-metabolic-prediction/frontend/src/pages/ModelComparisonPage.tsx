import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { SectionHeader } from "../components/SectionHeader";
import { getModels } from "../services/api";
import { ModelMetric } from "../types/api";

export function ModelComparisonPage() {
  const [models, setModels] = useState<ModelMetric[]>([]);

  useEffect(() => {
    getModels().then(setModels);
  }, []);

  return (
    <div className="page-stack">
      <SectionHeader
        eyebrow="Model Comparison"
        title="Classifier Evaluation"
        subtitle="Accuracy, precision, recall, F1 score, and ROC AUC across candidate models."
      />

      <article className="panel">
        <h3>Evaluation Metrics</h3>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={models}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="model_name" />
            <YAxis domain={[0, 1]} />
            <Tooltip />
            <Legend />
            <Bar dataKey="accuracy" fill="#0F4C81" radius={[4, 4, 0, 0]} />
            <Bar dataKey="precision" fill="#546E7A" radius={[4, 4, 0, 0]} />
            <Bar dataKey="recall" fill="#2E7D32" radius={[4, 4, 0, 0]} />
            <Bar dataKey="f1" fill="#C47F00" radius={[4, 4, 0, 0]} />
            <Bar dataKey="roc_auc" fill="#D32F2F" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </article>

      <article className="panel">
        <h3>Metrics Table</h3>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Model</th>
                <th>Accuracy</th>
                <th>Precision</th>
                <th>Recall</th>
                <th>F1</th>
                <th>ROC AUC</th>
              </tr>
            </thead>
            <tbody>
              {models.map((model) => (
                <tr key={model.model_name}>
                  <td>{model.model_name}</td>
                  <td>{model.accuracy}</td>
                  <td>{model.precision}</td>
                  <td>{model.recall}</td>
                  <td>{model.f1}</td>
                  <td>{model.roc_auc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </article>
    </div>
  );
}
