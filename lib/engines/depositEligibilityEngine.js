import { Recommendation } from "../types/scanTypes.js";
export function getDepositEligibility(scan, recommendation, confidence, riskFlags, missingInfo) {
  const reasons = [];
  for (const m of missingInfo) reasons.push(m.replace("business name","business name"));
  if (recommendation.recommended_system === Recommendation.MANUAL) reasons.push("Manual review required");
  if (confidence.confidence_level === "Low" || confidence.confidence_level === "Manual Review") reasons.push("Low confidence recommendation");
  if (!recommendation.recommended_system) reasons.push("First Fix scope not generated");
  if (riskFlags.length) reasons.push("Red flag detected");
  const deposit_allowed = reasons.length === 0;
  return { deposit_allowed, deposit_block_reasons: [...new Set(reasons)] };
}
