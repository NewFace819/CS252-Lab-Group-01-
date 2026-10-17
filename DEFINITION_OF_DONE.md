# Fitlens — Definition of Done (DoD)

This document establishes the official **Definition of Done** for all features, documentation, and components developed in the **Fitlens** repository.

A task, user story, or backlog item is only considered **Done** when all the following criteria are satisfied.

---

## 1. Acceptance Criteria Satisfied

- [ ] All explicit acceptance criteria specified in the issue/task description are fully met.
- [ ] Any required architectural diagrams, plans, or visual assets are created and linked in the appropriate directory (e.g., `docs/` or `ui/`).

---

## 2. Documentation & Clarity

- [ ] All documentation is written in clear, professional English.
- [ ] Technical architecture and integration mechanisms are clearly explained (e.g., how the UI communicates with the backend).
- [ ] All markdown links (relative paths) are valid, clickable, and resolve to existing files.
- [ ] Directory README files (`ui/README.md`, `docs/README.md`, etc.) are updated to reflect any new files or workflow changes.

---

## 3. Code Quality & Standards

- [ ] Code adheres to standard Python styling guidelines (PEP 8).
- [ ] No hardcoded secrets, personal tokens, or extraneous debug print statements.
- [ ] Separation of concerns is preserved (e.g., UI presentation logic is decoupled from backend business logic).
- [ ] Placeholder files and prototypes are runnable or syntactically valid with clear usage instructions.

---

## 4. Verification & Testing

- [ ] The automated test suite (`pytest`) runs cleanly and reports passing status for active tests.
- [ ] Code and scripts execute without syntax or import errors.
- [ ] Changes are verified manually in the target environment (e.g., checking Streamlit UI rendering).

---

## 5. Version Control & Pull Request Readiness

- [ ] Changes are committed on a dedicated feature/task branch.
- [ ] Commit messages follow the **Conventional Commits** specification (e.g., `docs:`, `feat:`, `fix:`, `test:`).
- [ ] `.gitignore` rules are respected; no virtual environments, `.pyc` caches, or IDE files are staged.
- [ ] A Pull Request is opened with a descriptive summary of changes and reference to the ticket.
