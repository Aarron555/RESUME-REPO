import { createScanSubmission } from '../schemas/scanSchema.js';
import { getMissingInfo } from '../utils/validation.js';
import { scoreScan } from '../engines/scoringEngine.js';
import { detectRiskFlags } from '../engines/redFlagEngine.js';
import { recommendSystem } from '../engines/recommendationEngine.js';
import { getConfidence } from '../engines/confidenceEngine.js';
import { getDepositEligibility } from '../engines/depositEligibilityEngine.js';
import { getNextBestAction } from '../engines/nextBestActionEngine.js';
import { generateBuildBrief } from '../engines/buildBriefGenerator.js';
import { generateCopyTemplates } from '../templates/copyTemplates.js';
import { scanRepository } from '../data/scanRepository.js';

export function processScan(input){
  const scan=createScanSubmission(input);
  const scores=scoreScan(scan);
  const risk_flags=detectRiskFlags(scan);
  const recommendation=recommendSystem(scan,scores,risk_flags);
  const confidence=getConfidence(scan,scores,recommendation,risk_flags);
  const missing_info=getMissingInfo(scan);
  const deposit=getDepositEligibility(scan,recommendation,confidence,risk_flags,missing_info);
  const merged={...scan,...scores,score_reasons:scores.reasons,risk_flags,missing_info,...recommendation,...confidence,...deposit,status:deposit.deposit_allowed?'recommendation_ready':'needs_review'};
  merged.next_best_action=getNextBestAction(merged).label;
  merged.internal_build_brief=generateBuildBrief(merged,recommendation,scores);
  merged.customer_recommendation_message=generateCopyTemplates(merged,recommendation).recommendation;
  return scanRepository.create(merged);
}
