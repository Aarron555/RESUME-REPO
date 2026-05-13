import { requiredBusinessFields } from "../schemas/scanSchema.js";

export function getMissingInfo(scan) {
  const missing = [];
  for (const f of requiredBusinessFields) if (!scan[f]) missing.push(`Missing ${f.replaceAll("_", " ")}`);
  if (!scan.phone && !scan.email) missing.push("Missing phone or email");
  if (!scan.lead_sources?.length) missing.push("Missing lead source");
  if (!scan.pain_points?.length) missing.push("Missing pain point");
  return missing;
}
