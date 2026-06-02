import { Activity, BarChart3, Brain, ClipboardPlus, LayoutDashboard } from "lucide-react";
import { ReactNode } from "react";
import { useMemo, useState } from "react";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import { DashboardPage } from "./pages/DashboardPage";
import { InsightsPage } from "./pages/InsightsPage";
import { ModelComparisonPage } from "./pages/ModelComparisonPage";
import { PredictionPage } from "./pages/PredictionPage";

type ViewKey = "dashboard" | "prediction" | "analytics" | "models" | "insights";

const views: Array<{ key: ViewKey; label: string; icon: ReactNode }> = [
  { key: "dashboard", label: "Dashboard", icon: <LayoutDashboard size={18} /> },
  { key: "prediction", label: "Prediction", icon: <ClipboardPlus size={18} /> },
  { key: "analytics", label: "Analytics", icon: <BarChart3 size={18} /> },
  { key: "models", label: "Models", icon: <Activity size={18} /> },
  { key: "insights", label: "Insights", icon: <Brain size={18} /> }
];

export default function App() {
  const [activeView, setActiveView] = useState<ViewKey>("dashboard");

  const content = useMemo(() => {
    switch (activeView) {
      case "prediction":
        return <PredictionPage />;
      case "analytics":
        return <AnalyticsPage />;
      case "models":
        return <ModelComparisonPage />;
      case "insights":
        return <InsightsPage />;
      default:
        return <DashboardPage />;
    }
  }, [activeView]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-mark">
          <span>OM</span>
          <div>
            <strong>Obesity Model</strong>
            <small>Ocular + Metabolic AI</small>
          </div>
        </div>
        <nav>
          {views.map((view) => (
            <button
              key={view.key}
              className={activeView === view.key ? "active" : ""}
              onClick={() => setActiveView(view.key)}
              title={view.label}
            >
              {view.icon}
              <span>{view.label}</span>
            </button>
          ))}
        </nav>
      </aside>

      <main className="content-area">
        <header className="top-bar">
          <div>
            <h1>Predictive Modeling of Obesity Prevalence</h1>
            <p>Academic healthcare analytics system using ocular and metabolic biomarkers.</p>
          </div>
          <span className="status-pill">Research Prototype</span>
        </header>
        {content}
      </main>
    </div>
  );
}
