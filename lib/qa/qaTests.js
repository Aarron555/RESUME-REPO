import { scoreScan } from "../engines/scoringEngine.js";
import { detectRiskFlags } from "../engines/redFlagEngine.js";
import { recommendSystem } from "../engines/recommendationEngine.js";
import { getConfidence } from "../engines/confidenceEngine.js";
import { getDepositEligibility } from "../engines/depositEligibilityEngine.js";
import { getNextBestAction } from "../engines/nextBestActionEngine.js";
import { runCopyGuard } from "../compliance/copyGuards.js";
import { demoProfiles } from "../demo/demoProfiles.js";
import { processScan } from "../services/scanOrchestrator.js";
import { evaluateBuildReady } from "../engines/buildReadyChecklistEngine.js";
import { getRuntimeConfig, canShowDepositCta, canShowBookingCta } from "../config/runtimeConfig.js";
import { paymentRepository, bookingRepository } from "../data/opsRepositories.js";
import { auditLogRepository } from "../data/auditLogRepository.js";

const results=[]; const ok=(n,c)=>results.push({n,c});
const s=scoreScan({urgency_answer:"Happens often and hurts",average_job_value_answer:"$500+",lead_sources:[1,2,3,4],pain_points:["Missed calls"],current_tools:["Gmail"]});
ok('urgency mapping',s.urgency_score===20); ok('ticket mapping',s.ticket_value_score===20); ok('lead chaos',s.lead_chaos_score===20); ok('owner pain',s.owner_pain_score>=10); ok('tool mapping',s.implementation_simplicity_score===19);
const rf=detectRiskFlags({fit_check_answer:'I want custom software and guaranteed revenue plus unlimited support'}); ok('red flag custom',rf.some(x=>x.includes('custom'))); ok('red flag guaranteed',rf.some(x=>x.includes('guaranteed'))); ok('red flag unlimited',rf.some(x=>x.includes('unlimited')));
const rec=recommendSystem({pain_points:['Quotes get lost'],lead_sources:['Phone']},{total_score:70},[]); ok('quote route',rec.recommended_system==='Quote Follow-Up Fix');
const conf=getConfidence({business_name:'x',contact_name:'y',phone:'1',industry:'z',service_area:'a'},{total_score:80},{recommended_system:'Missed Lead Fix'},[]); ok('high confidence',conf.confidence_level==='High');
const dep=getDepositEligibility({}, {recommended_system:'Manual Review / Not Fit Yet'},{confidence_level:'Manual Review'},['x'],['Missing phone or email']); ok('deposit block',dep.deposit_allowed===false);
ok('next action red flag',getNextBestAction({risk_flags:['x']}).label==='Manual Review Required');
ok('copy guard safe',runCopyGuard('systems for boring work').pass===true);
ok('copy guard banned',runCopyGuard('guaranteed bookings').pass===false);
const br=evaluateBuildReady('Missed Lead Fix', {'lead source to connect':1}); ok('build ready blocked missing checklist',br.blocked===true);
const cfg=getRuntimeConfig(); ok('config helper exists',Array.isArray(cfg.safeWarnings));
ok('deposit cta disabled when link missing or blocked',canShowDepositCta(false)===false);
ok('booking cta follows config',typeof canShowBookingCta()==='boolean');

for (const p of demoProfiles){ const out=processScan(p.input); if (p.expected.recommended_system) ok(`demo ${p.name} route`,out.recommended_system===p.expected.recommended_system); if (typeof p.expected.deposit_allowed==='boolean') ok(`demo ${p.name} deposit`,out.deposit_allowed===p.expected.deposit_allowed); if (p.expected.next_best_action) ok(`demo ${p.name} next action`, out.next_best_action===p.expected.next_best_action); }

const hot = processScan(demoProfiles[0].input);
const pay = paymentRepository.upsert(hot.id,{status:'requested'});
const pay2 = paymentRepository.upsert(hot.id,{status:'manual_confirmed',confirmation_note:'bank screenshot verified'});
auditLogRepository.add({actor:'admin',scan_id:hot.id,action:'payment_manual_confirmed',new_value:pay2.status,reason:'confirmation note provided'});
const book = bookingRepository.upsert(hot.id,{status:'requested'});
const book2 = bookingRepository.upsert(hot.id,{status:'booked',scheduled_time:'2026-05-10T10:00:00Z'});
auditLogRepository.add({actor:'admin',scan_id:hot.id,action:'booking_marked_booked',new_value:book2.status,reason:'manual confirmation'});

ok('payment status manual_confirmed supported',pay2.status==='manual_confirmed');
ok('booking status booked supported',book2.status==='booked');
ok('dry run payment requested exists',pay.status==='requested');

const dryRunStages = [
  !!hot.id,
  hot.recommended_system==='Missed Lead Fix',
  hot.deposit_allowed===true,
  hot.next_best_action==='Send Recommendation',
  pay.status==='requested',
  pay2.status==='manual_confirmed',
  getNextBestAction({status:'deposit_paid'}).label==='Schedule Activation Call',
  book.status==='requested',
  book2.status==='booked',
  evaluateBuildReady('Missed Lead Fix',{}).blocked===true,
  evaluateBuildReady('Missed Lead Fix', {'lead source to connect':1,'staff alert contact':1,'customer reply tone':1,'business hours':1,'booking/callback link':1,'owner approval contact':1,'follow-up timing preference':1}).blocked===false,
  getNextBestAction({status:'build_ready'}).label==='Start Build',
  getNextBestAction({status:'in_build'}).label==='Continue Build / QA',
  getNextBestAction({status:'qa_testing'}).label==='Request Final Payment',
  getNextBestAction({status:'handoff_sent'}).label==='Offer Care',
  getNextBestAction({status:'care_offered'}).label==='Ask For Referral / Case Study'
];
ok('dry run chain', dryRunStages.every(Boolean));

let fail=0; for(const r of results){ if(!r.c) fail++; console.log(`${r.c?'PASS':'FAIL'}: ${r.n}`);} console.log(`\nTOTAL: ${results.length-fail}/${results.length} passing`); if(fail) process.exit(1);
