# Roadmap

This roadmap separates resume-ready improvements from future production upgrades.

## Phase 1 — Resume-ready proof asset

Status: mostly implemented in this PR.

- Professional README with scope and recruiter summary
- Deterministic local execution without API keys
- Dependency file
- Architecture documentation
- Evaluation method documentation
- Limitations documentation
- Claim map for resume-safe wording
- Recruiter review guide
- CI workflow for tests and benchmark smoke run
- Active-schema aligned statistics helper
- Expanded tests for validators, statistics, reports, and reproducibility

## Phase 2 — Stronger local evaluation platform

- Add larger task catalog
- Add golden fixture files under `fixtures/`
- Add CSV export for scored records
- Add dashboard filters for model, task, and prompt system
- Add artifact version stamps
- Add experiment comparison command
- Add richer failure taxonomy examples
- Add config validation with clearer error messages

## Phase 3 — Real model adapters

- Add optional OpenAI adapter behind environment variables
- Add optional Anthropic adapter behind environment variables
- Add local model adapter for local inference endpoints
- Add response cache to control cost and reproducibility
- Add provider/model/version metadata per run
- Keep deterministic test mode as the default

## Phase 4 — AI operations dashboard

- Add persistent experiment registry
- Add reviewer annotations
- Add human review queue
- Add drift and regression comparisons
- Add dashboard authentication if deployed
- Add model cost reports
- Add exportable executive summaries

## Phase 5 — Portfolio integration

- Add a one-page project case study
- Add screenshots of report and dashboard
- Add short demo walkthrough
- Add resume claim mapping to project sections
- Link portfolio and resume to this repo

## Non-goals for current version

- No claim of universal prompt superiority
- No claim of live commercial model benchmark accuracy
- No enterprise deployment claim
- No security or compliance certification claim
