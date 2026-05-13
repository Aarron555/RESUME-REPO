const checklists = {
  'Missed Lead Fix':['lead source to connect','staff alert contact','customer reply tone','business hours','booking/callback link','owner approval contact','follow-up timing preference'],
  'Quote Follow-Up Fix':['quote source','quote tracker fields','follow-up timing','staff reminder contact','won/lost status options','message tone','owner approval contact'],
  'Review + Reactivation Fix':['completed job trigger','review link','customer list source','reactivation message approval','referral prompt approval','owner approval contact']
};
export function evaluateBuildReady(recommendedSystem, provided = {}, overrideReason=''){
  const required = checklists[recommendedSystem] || [];
  const missing = required.filter((k)=>!provided[k]);
  const blocked = missing.length>0 && !overrideReason;
  return { required, missing, blocked, override_used: !!overrideReason };
}
