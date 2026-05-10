import { Status } from "../types/scanTypes.js";
export const allowedTransitions = {
  [Status.NEW_SCAN]: [Status.NEEDS_REVIEW, Status.RECOMMENDATION_READY, Status.NOT_FIT],
  [Status.RECOMMENDATION_READY]: [Status.RECOMMENDATION_SENT],
  [Status.RECOMMENDATION_SENT]: [Status.DEPOSIT_REQUESTED, Status.CLOSED_LOST],
  [Status.DEPOSIT_REQUESTED]: [Status.DEPOSIT_PAID, Status.CLOSED_LOST],
  [Status.DEPOSIT_PAID]: [Status.ACTIVATION_SCHEDULED],
  [Status.ACTIVATION_SCHEDULED]: [Status.ONBOARDING_SENT],
  [Status.ONBOARDING_SENT]: [Status.ONBOARDING_COMPLETE],
  [Status.ONBOARDING_COMPLETE]: [Status.BUILD_READY],
  [Status.BUILD_READY]: [Status.IN_BUILD],
  [Status.IN_BUILD]: [Status.QA_TESTING],
  [Status.QA_TESTING]: [Status.CLIENT_REVIEW, Status.FINAL_PAYMENT_DUE],
  [Status.FINAL_PAYMENT_DUE]: [Status.HANDOFF_SENT],
  [Status.HANDOFF_SENT]: [Status.CARE_OFFERED],
  [Status.CARE_OFFERED]: [Status.CARE_ACTIVE]
};
