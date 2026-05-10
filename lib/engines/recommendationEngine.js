import { Recommendation } from "../types/scanTypes.js";
export function recommendSystem(scanAnswers, scores, riskFlags) {
  if (riskFlags.length) return { recommended_system: Recommendation.MANUAL, reason: "Red flag detected; manual review required." };
  const pains = scanAnswers.pain_points || [];
  const hasMissedLead = pains.some((p) => ["Missed calls","Slow replies","DMs pile up","Staff forgets to respond"].includes(p)) || (scanAnswers.lead_sources?.length || 0) >= 3;
  const hasQuote = pains.some((p) => ["Quotes get lost","We forget to follow up"].includes(p));
  const hasReview = pains.some((p) => ["Reviews do not get requested","Old customers are not re-contacted"].includes(p));
  if (hasMissedLead) return { recommended_system: Recommendation.MISSED_LEAD, reason: "Highest-urgency lead response leaks detected." };
  if (hasQuote) return { recommended_system: Recommendation.QUOTE, reason: "Quote follow-up leak detected." };
  if (hasReview) return { recommended_system: Recommendation.REVIEW, reason: "Review/reactivation leak detected." };
  if (scores.total_score < 40) return { recommended_system: Recommendation.MANUAL, reason: "Low urgency/value and unclear workflow." };
  return { recommended_system: Recommendation.MANUAL, reason: "Signals were too broad for a safe one-system First Fix." };
}
