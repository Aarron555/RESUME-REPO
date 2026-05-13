export const requiredBusinessFields = ["business_name", "contact_name", "industry", "service_area"];

export function createScanSubmission(input = {}) {
  const now = new Date().toISOString();
  return {
    id: input.id || `scan_${Math.random().toString(36).slice(2, 10)}`,
    business_name: input.business_name || "",
    contact_name: input.contact_name || "",
    phone: input.phone || "",
    email: input.email || "",
    industry: input.industry || "",
    service_area: input.service_area || "",
    website_or_social: input.website_or_social || "",
    preferred_contact_method: input.preferred_contact_method,
    lead_sources: input.lead_sources || [],
    pain_points: input.pain_points || [],
    urgency_answer: input.urgency_answer || "",
    average_job_value_answer: input.average_job_value_answer || "",
    current_tools: input.current_tools || [],
    fit_check_answer: input.fit_check_answer || "",
    free_text_pain: input.free_text_pain || "",
    urgency_score: 0, ticket_value_score: 0, lead_chaos_score: 0, owner_pain_score: 0, implementation_simplicity_score: 0,
    total_score: 0, tier: "", recommended_system: "", confidence_level: "", plain_language_reason: "", score_reasons: {},
    risk_flags: [], missing_info: [], deposit_allowed: false, deposit_block_reasons: [], next_best_action: "",
    customer_recommendation_message: "", internal_build_brief: "", status: "new_scan", admin_notes: "",
    created_at: now, updated_at: now, submitted_at: now
  };
}
