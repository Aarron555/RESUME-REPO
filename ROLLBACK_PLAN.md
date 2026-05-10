# Rollback Plan
1. Stop intake by disabling scan submit endpoint or hiding CTA.
2. Backup `data/db.json`.
3. Revert to previous git commit.
4. Restore prior `data/db.json` backup.
5. Run `npm run qa`.
6. Re-open intake only after critical checks pass.
