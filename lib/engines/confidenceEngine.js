import { Recommendation } from "../types/scanTypes.js";
export function getConfidence(scanAnswers, scores, recommendation, riskFlags) {
  if (riskFlags.length || recommendation.recommended_system === Recommendation.MANUAL) return { confidence_level: "Manual Review", reason: "Risk or fit boundaries require human review." };
  const missing = ["business_name","contact_name","industry","service_area"].filter((k)=>!scanAnswers[k]).length + (!scanAnswers.phone && !scanAnswers.email ? 1 : 0);
  if (scores.total_score < 50 || missing > 2) return { confidence_level: "Low", reason: "Low score or incomplete answers reduce confidence." };
  if (missing > 0) return { confidence_level: "Medium", reason: "Core pain is clear; confirm missing details on Activation Call." };
  return { confidence_level: "High", reason: "Clear pain, clear fit, and complete info with no red flags." };
}
