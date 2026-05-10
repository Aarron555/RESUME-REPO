const banned = ["AI agency","AI for boring work","guaranteed revenue","guaranteed bookings","unlimited support","unlimited lifetime","trusted by 10,000","double your sales","never miss another lead ever again","fully automate your business","no work required","passive income"];
export function runCopyGuard(text) {
  const found = banned.filter((p) => text.toLowerCase().includes(p.toLowerCase()));
  return { pass: found.length === 0, found };
}
