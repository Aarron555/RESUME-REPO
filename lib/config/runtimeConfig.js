const requiredPublic = ['PUBLIC_APP_URL','PUBLIC_BOOKING_LINK','PUBLIC_STRIPE_DEPOSIT_LINK','PUBLIC_CONTACT_EMAIL','PUBLIC_CONTACT_PHONE'];
export function getRuntimeConfig(){
  const cfg = Object.fromEntries(requiredPublic.map((k)=>[k,process.env[k]||'']));
  cfg.ADMIN_EMAIL = process.env.ADMIN_EMAIL || '';
  cfg.ADMIN_AUTH_SECRET = process.env.ADMIN_AUTH_SECRET || '';
  const missing = requiredPublic.filter((k)=>!cfg[k]);
  return { cfg, missing, safeWarnings: missing.map((k)=>`${k} missing`) };
}
export function canShowDepositCta(depositAllowed){ return depositAllowed && !!process.env.PUBLIC_STRIPE_DEPOSIT_LINK; }
export function canShowBookingCta(){ return !!process.env.PUBLIC_BOOKING_LINK; }
