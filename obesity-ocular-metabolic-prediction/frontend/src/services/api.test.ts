import { describe, expect, it } from "vitest";
import { defaultPatientInput } from "./api";

describe("default patient input", () => {
  it("keeps a clinically plausible BMI profile", () => {
    expect(defaultPatientInput.bmi).toBeGreaterThan(25);
    expect(defaultPatientInput.ocular_risk_score).toBeGreaterThan(0);
    expect(defaultPatientInput.gender).toBe("Female");
  });
});
