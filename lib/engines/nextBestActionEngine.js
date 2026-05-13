import { Status } from "../types/scanTypes.js";
export function getNextBestAction(scanState) {
  if (scanState.risk_flags?.length) return { label: "Manual Review Required", why: "Red flags detected.", blocked: false };
  if (scanState.missing_info?.length) return { label: "Request Missing Info", why: "Critical details are missing.", blocked: false };
  if (scanState.confidence_level === "Low") return { label: "Book Review Call", why: "Low confidence recommendation needs clarification.", blocked: false };
  const map = {
    [Status.NEW_SCAN]: "Send Recommendation",
    [Status.RECOMMENDATION_SENT]: "Send Deposit Link",
    [Status.DEPOSIT_REQUESTED]: "Follow Up On Deposit",
    [Status.DEPOSIT_PAID]: "Schedule Activation Call",
    [Status.ACTIVATION_SCHEDULED]: "Send Onboarding",
    [Status.ONBOARDING_COMPLETE]: "Move To Build Ready",
    [Status.BUILD_READY]: "Start Build",
    [Status.IN_BUILD]: "Continue Build / QA",
    [Status.QA_TESTING]: "Request Final Payment",
    [Status.HANDOFF_SENT]: "Offer Care",
    [Status.CARE_OFFERED]: "Ask For Referral / Case Study"
  };
  return { label: map[scanState.status] || "Send Recommendation", why: "Next stage action based on current pipeline status.", blocked: false };
}
