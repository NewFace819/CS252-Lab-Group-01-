# Security check: personal data and secrets

Issue: #17. Date: 2026-10-17. Reviewer: Nguyen Pham Duc Huy.

Scope: working tree of `feat/tests-and-check-env`, plus full git history of all
local and remote branches (11 commits: `main`, `wii-init`,
`feat/assistant-backend`, `feat/tests-and-check-env`).

## Manual check

| Check | Method | Result |
| --- | --- | --- |
| Hard-coded secrets in code (`api_key`, `secret`, `token`, `password`, `AKIA`, `sk-`, `ghp_`, `BEGIN ... KEY`) | `grep` over `src/`, `scripts/`, `tests/`, `pyproject.toml`, `requirements.txt` | None found |
| Secrets anywhere in history | `git log --all -p` piped through the same patterns | Only prose in docs/commit text ("do not commit API keys"); no real values |
| Secret/env files ever committed (`.env`, keys, certs) | `git log --all --name-only` | None; only source, docs, CSV and config files |
| `.gitignore` covers secrets | Reviewed | `.env`, `.env.*` (keeps `.env.example`), venvs, caches ignored |
| Data files contain personal data | Reviewed `data/offices.csv` | Only public office names, rooms and opening hours |
| Personal data in docs | Reviewed `docs/team.md` (on `origin/main`) | **Finding 1** |
| Personal data in git metadata | `git log --all --format='%an <%ae>'` | **Finding 2** |

## Gitleaks

Not run: `gitleaks` is not installed on the reviewer's machine. The manual
pattern scan above was used instead. Before closing the issue, someone with
gitleaks should run:

```bash
gitleaks detect --source . --log-opts="--all" --redact
```

and append the result here.

## Findings

1. **Student IDs in `docs/team.md`** (on `origin/main`): full names with
   student numbers. These are personal data. Decide whether the team agrees to
   keep them in a public repo. If not, remove the ID column. It stays in git
   history unless the history is rewritten.
2. **Personal emails in commit metadata**: author emails of five members
   (gmail addresses) appear in history. This is normal for git, but members who
   do not want this public should use the GitHub `noreply` address
   (`git config user.email <id>+<user>@users.noreply.github.com`) for future
   commits.

No secrets, credentials or tokens were found.

## Rules going forward

- Keep secrets in `.env` (ignored); commit only `.env.example` with placeholders.
- Keep only public information in `data/`; no private student records.
