# Security Policy

## Project scope

AXE-LAB is a deterministic local evaluation harness simulator. It is not a deployed production service and does not process secrets by default.

## Security principles

- Treat generated text and user-provided input as untrusted.
- Avoid unsafe code execution where possible.
- Keep deterministic local test mode as the safe default.
- Do not commit API keys, tokens, credentials, or private datasets.
- Document any future live API integration clearly.
- Prefer environment variables for secrets if live providers are added.

## High-risk areas

The highest-risk areas are validators and any code path that evaluates generated output. Extra review is required for:

- `src/evaluation/validators/code_validator.py`
- `src/core/iteration_runner.py`
- future live API adapters
- future dashboard deployment code
- GitHub Actions workflow changes

## Reporting issues

For now, open a GitHub issue with:

- affected file
- expected behavior
- actual behavior
- reproduction steps
- potential impact

Do not include secrets or private credentials in issue text.

## Current limitations

This project is local-first and not hardened for public multi-user deployment. A deployed version would require authentication, authorization, logging controls, dependency scanning, secret handling, rate limiting, and a fuller threat model.
