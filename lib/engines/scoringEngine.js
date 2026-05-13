const urgencyMap = {"Not a big deal":4,"Annoying":8,"Could cost us a job":15,"Happens often and hurts":20};
const valueMap = {"Under $100":5,"$100–$250":10,"$250–$500":15,"$500+":20,"Not sure":8};

export function scoreScan(scanAnswers) {
  const reasons = {};
  const urgency_score = urgencyMap[scanAnswers.urgency_answer] || 0;
  reasons.urgency_score = `Urgency '${scanAnswers.urgency_answer || "not provided"}' mapped to ${urgency_score}.`;
  const ticket_value_score = valueMap[scanAnswers.average_job_value_answer] || 0;
  reasons.ticket_value_score = `Average job value '${scanAnswers.average_job_value_answer || "not provided"}' mapped to ${ticket_value_score}.`;
  const sourceCount = scanAnswers.lead_sources?.length || 0;
  const lead_chaos_score = sourceCount >= 4 ? 20 : sourceCount === 3 ? 15 : sourceCount === 2 ? 10 : sourceCount === 1 ? 5 : 0;
  reasons.lead_chaos_score = `${sourceCount} lead sources indicates coordination complexity of ${lead_chaos_score}.`;
  const painCount = scanAnswers.pain_points?.length || 0;
  let owner_pain_score = painCount >= 4 ? 20 : painCount === 3 ? 15 : painCount === 2 ? 12 : painCount === 1 ? 8 : 0;
  const painBoost = ["Missed calls","Slow replies","DMs pile up","We forget to follow up","Staff forgets to respond","I do too much manually"];
  if ((scanAnswers.pain_points || []).some((p) => painBoost.includes(p))) owner_pain_score += 2;
  reasons.owner_pain_score = `${painCount} pains with high-leak indicators gives ${owner_pain_score}.`;
  const tools = scanAnswers.current_tools || [];
  let implementation_simplicity_score = tools.includes("Not sure") ? 10 : 14;
  if (tools.some((t)=>["Mostly phone/text","Google Sheets","Gmail","Calendly"].includes(t))) implementation_simplicity_score = 19;
  if (tools.some((t)=>["Square","Stripe","Jobber","Housecall Pro","GoHighLevel"].includes(t))) implementation_simplicity_score = 14;
  reasons.implementation_simplicity_score = `Current tools suggest implementation simplicity score of ${implementation_simplicity_score}.`;
  const total_score = urgency_score + ticket_value_score + lead_chaos_score + owner_pain_score + implementation_simplicity_score;
  const tier = total_score >= 80 ? "Hot" : total_score >= 60 ? "Warm" : total_score >= 40 ? "Cold" : "Manual Review / Not Fit";
  return { urgency_score,ticket_value_score,lead_chaos_score,owner_pain_score,implementation_simplicity_score,total_score,tier,reasons };
}
