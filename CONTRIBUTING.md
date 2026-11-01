# Contributing

## Workflow

1. Create a branch for your task from `main` (for example `feat/8-partial-names`).
2. Make focused changes and run `python -m pytest -q` before you push.
3. Commit with a Conventional Commit message (`docs:`, `feat:`, `fix:`, `test:`, `chore:`).
4. Open a Pull Request that links the issue (`Closes #<issue>`) and assign a teammate to review it.

The team's [Definition of Done](lab02/templates/DEFINITION_OF_DONE.md) applies to every PR.

## Secrets

- Never commit secrets: API keys, tokens, passwords, private keys, or personal data.
- Keep local secrets in a `.env` file. `.env` and `.env.*` are listed in `.gitignore`.
- The only tracked env file is `.env.example`. It contains variable names with empty
  placeholders, never real values. Add a new variable to `.env.example` in the same PR
  that starts using it.
- Set up your own file with `cp .env.example .env` (Windows: `copy .env.example .env`).
- Read secrets from environment variables in code. Do not print or log them.
- If you commit a secret by mistake, treat it as leaked: revoke or rotate it first,
  then tell the team. Deleting the file in a later commit does not remove it from git history.
- Use only public information in `data/`; do not add private student records.
