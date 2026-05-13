const flaggedPhrases = ["guaranteed revenue","guaranteed bookings","custom software","unlimited support","employee replacement","chatbot","legal","medical","financial","sensitive customer data","cold texting","everything automated","full custom automation","regulated","replacing staff","without approval"];

export function detectRiskFlags(scanAnswers) {
  const text = `${scanAnswers.fit_check_answer || ""} ${scanAnswers.free_text_pain || ""}`.toLowerCase();
  const flags = flaggedPhrases.filter((p) => text.includes(p));
  if (scanAnswers.fit_check_answer === "I need help with legal/medical/financial intake") flags.push("sensitive intake");
  if (scanAnswers.fit_check_answer === "I want guaranteed sales") flags.push("guaranteed sales expectation");
  if (scanAnswers.fit_check_answer === "I want custom software") flags.push("custom software request");
  if (scanAnswers.fit_check_answer === "I want a chatbot to replace staff") flags.push("chatbot replacing staff");
  return [...new Set(flags)];
}
