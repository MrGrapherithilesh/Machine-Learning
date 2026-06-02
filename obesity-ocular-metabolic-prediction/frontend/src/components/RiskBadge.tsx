import { RiskCategory } from "../types/api";

const riskClass: Record<RiskCategory, string> = {
  Low: "risk-low",
  Moderate: "risk-moderate",
  High: "risk-high"
};

export function RiskBadge({ risk }: { risk: RiskCategory }) {
  return <span className={`risk-badge ${riskClass[risk]}`}>{risk}</span>;
}
