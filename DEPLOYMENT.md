# Deployment
## Environment variables
PUBLIC_APP_URL, PUBLIC_BOOKING_LINK, PUBLIC_STRIPE_DEPOSIT_LINK, PUBLIC_STRIPE_FINAL_BALANCE_LINK, PUBLIC_CONTACT_EMAIL, PUBLIC_CONTACT_PHONE, ADMIN_EMAIL, ADMIN_AUTH_SECRET, DATA_FILE, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, EMAIL_API_KEY, EMAIL_FROM
## Build / checks
- Run `npm run qa`
## Storage
- `DATA_FILE` JSON datastore for private beta.
## Auth
- Implement real admin auth before production.
## Payment
- Manual confirmation required in private beta.
## Booking
- Manual confirmation required in private beta.
## Post-deploy verification
- Submit demo scan, confirm record persists, confirm deposit blocked on red flags.
