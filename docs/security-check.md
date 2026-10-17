# Security check: personal data and secrets

Issue: #17. Date: 2026-10-17. Reviewer: Nguyen Pham Duc Huy.

Scope: `origin/main` at `44ba937` (working tree and the full git history, 11
commits on all branches).

## Manual check

| Check | Method | Result |
| --- | --- | --- |
| Hard-coded secrets in code (`api_key`, `secret`, `token`, `password`, `AKIA`, `sk-`, `ghp_`, `BEGIN ... KEY`) | `grep` over `src/`, `scripts/`, `tests/`, `lab02/`, `.github/`, `pyproject.toml`, `requirements.txt` | None found |
| Secrets anywhere in history | `git log --all -p` with the same patterns | Only prose ("do not commit API keys"); no real values |
| Secret or env files ever committed (`.env`, keys, certs) | `git log --all --name-only` | None |
| `.gitignore` covers secrets | Reviewed | `.env`, `.env.*` (keeps `.env.example`), venvs and caches are ignored |
| Large files | `du` over tracked files | Largest file is 8 KB |
| Personal data in data files | Reviewed `data/` | Only public office names, rooms and opening hours |
| Personal data in docs | Reviewed `docs/team.md` | **Finding 1** |
| Personal data in git metadata | `git log --all --format='%an <%ae>'` | **Finding 2** |

## Gitleaks

Tool: gitleaks 8.30.1, default ruleset.

```bash
gitleaks detect --source . --log-opts="--all" --redact
```

Result: 11 commits scanned, no leaks found.

## Findings

1. **Student IDs in `docs/team.md`**: full names with student numbers are
   personal data. The team should decide whether to keep them in this repo.
   If not, remove the ID column; the old values stay in git history unless
   the history is rewritten.
2. **Personal emails in commit metadata**: author emails of several members
   (gmail addresses) appear in history. This is normal for git. Members who do
   not want this public can use their GitHub `noreply` address for future
   commits.

No secrets, credentials or tokens were found.

## Rules going forward

- Keep secrets in `.env` (ignored); commit only `.env.example` with placeholders.
- Keep only public information in `data/`; no private student records.
