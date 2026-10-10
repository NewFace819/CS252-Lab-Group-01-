# User Interface Module (`ui/`)

This directory contains user interface implementations, presentation components, and front-end interaction layers for the **Smart Virtual Assistant** (`CSC10014`).

---

## 🎯 Purpose & Scope

The `ui/` module is responsible for:
- Capturing user input (prompts, questions, command options).
- Presenting the assistant's responses and suggestions cleanly.
- Decoupling visual and interaction presentation from backend rule parsing (`src/assistant/`).

---

## 🏗️ Recommended Structure

As the project evolves, the UI layer can be organized as follows:

```text
ui/
├── cli/                 # Terminal-based interactive interfaces (e.g., rich, prompt_toolkit)
├── web/                 # Web interface (e.g., Streamlit, Gradio, or lightweight HTML/CSS)
│   ├── app.py           # Web app entry point
│   ├── static/          # Static assets (stylesheets, icons, logos)
│   └── templates/       # HTML templates (if using Flask / FastAPI)
├── components/          # Reusable UI widgets / message bubbles
└── README.md            # UI module documentation and guidelines
```

---

## 📐 UI Development Rules & Guidelines

1. **Separation of Concerns**:
   - UI code must only handle layout, rendering, and event handling.
   - All intent classification, query resolution, and rule evaluation must call the core backend (`src/assistant`).

2. **Handling User Input**:
   - Strip leading/trailing whitespaces from input before passing to the backend.
   - Support both English and Vietnamese characters (UTF-8 safe).
   - Provide clear fallback or help messages when user input is empty or unrecognized.

3. **Response Rendering**:
   - Format responses clearly (e.g., using Markdown or structured text for multi-item office information).
   - Display appropriate loading/typing indicators for asynchronous interactions.

4. **Extensibility**:
   - Keep the UI interface decoupled from the underlying assistant implementation so that transitioning from rule-based to AI/LLM-based backends requires zero UI changes.

---

## 🚀 Running the UI

- **Default Starter CLI**:
  ```bash
  python -m assistant
  # Or with a single query:
  python -m assistant "where is the training office?"
  ```
- *(Future Web/GUI UI)*: Document run commands here once implemented (e.g., `streamlit run ui/web/app.py`).