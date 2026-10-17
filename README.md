# Fitlens

This repository provides the foundation for developing, testing, and maintaining the Fitlens application. It follows a reproducible Python development workflow so that every team member can set up the project and run it consistently.

## Features

- Organized Python project structure.
- Isolated development environment using Python virtual environments.
- Dependency management with pinned package versions.
- Automated testing with `pytest`.
- Version control and collaborative development using Git and GitHub.

> **Project status:** Initial setup and development. Application features will be documented as they are implemented.

## Prerequisites

Before setting up Fitlens, make sure you have installed:

- **Python 3.10 or newer**
- **Git**
- **GitHub Desktop** or Git command-line tools

Verify your installations:

```bash
python --version
git --version
```

On Windows, you can use `py --version` if the `python` command is unavailable.

## Getting Started

Follow these instructions to set up Fitlens on a fresh machine.

### 1. Clone the repository

Replace `<repository-url>` with the URL of your Fitlens GitHub repository.

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

A virtual environment keeps Fitlens dependencies separate from other Python projects on your machine.

### 3. Activate the virtual environment

**Windows — PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows — Git Bash:**

```bash
source .venv/Scripts/activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

After activation, your terminal should display the `(.venv)` prefix.

### 4. Install dependencies

With the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

These commands install the project's dependencies and the Fitlens package in editable mode.

### 5. Verify the environment

If the repository includes the environment-checking script, run:

```bash
python scripts/check_env.py
```

Resolve any reported issues before continuing.

## Running the Application

If the current application entry point is the Python package `assistant`, run:

```bash
python -m assistant
```

To provide a sample query:

```bash
python -m assistant "where is the IT helpdesk?"
```

### Help and available commands

Show the assistant's capabilities and example questions:

```bash
python -m assistant "help"
```

The help response explains office location/opening-hour lookup, the office-list
command, Vietnamese input with or without accents, and how to leave interactive
mode. `trợ giúp` and `hướng dẫn` also show help.

For an interactive session, run `python -m assistant`, type `help`, then enter a
question or `list offices`. Type `quit` or `exit` to leave. Help works even before
office data is available; live lookup and listing require `data/offices.csv` to
contain office records.

The commands above follow the current starter project's entry point. Update this section when the Fitlens application entry point and features are implemented.

## Running Tests

Run the automated test suite from the repository root:

```bash
pytest -q
```

A successful run should report that all tests have passed. The exact number of tests may change as the project develops.

## Project Structure

```text
Fitlens/
├── src/
│   └── assistant/       # Application source code
├── tests/               # Automated tests
├── data/                # Sample data and data documentation
├── docs/                # Project documentation
├── ui/                  # User interface plans and resources
├── scripts/             # Development and environment scripts
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project metadata and build configuration
├── .gitignore           # Files excluded from version control
└── README.md            # Project documentation
```

Some directories or files may be added as development progresses.

## Development Workflow

Fitlens uses Git and GitHub for collaborative development.

1. Create a separate branch for your task.
2. Implement your changes and test them locally.
3. Commit your changes using a descriptive commit message.
4. Push your branch to GitHub.
5. Open a Pull Request for review before merging into the main branch.

Example commit messages:

```text
docs: improve project setup instructions
feat: add a new application feature
test: add tests for input validation
fix: resolve an application error
```

## Troubleshooting

### `No module named assistant`

Activate the virtual environment and reinstall the project:

```bash
python -m pip install -e .
```

### `pytest` is not recognized

Run pytest through Python:

```bash
python -m pytest -q
```

If it is not installed, check `requirements.txt` and install the dependencies again.

### PowerShell blocks virtual environment activation

If PowerShell reports that script execution is disabled, use Git Bash or follow the Python environment activation guidance for your system.

### VS Code uses the wrong Python interpreter

Open the Command Palette with `Ctrl+Shift+P`, select **Python: Select Interpreter**, and choose the interpreter inside `.venv`.

## Contributing

All team members are encouraged to contribute through focused branches and Pull Requests. Changes should be tested before they are submitted for review.

Do not commit virtual environments, API keys, passwords, or other secrets to the repository.

## License

No license has been specified yet. Licensing information will be added when the project team makes a decision.

---
