"""Fitlens — Campus Virtual Assistant (UI Prototype & Placeholder).

This module provides the Streamlit user interface for the Fitlens campus assistant.
It demonstrates the integration between the UI presentation layer and the core backend
rules engine (``src/assistant/rules.py``).

Usage:
    streamlit run ui/app.py
"""
from __future__ import annotations

import sys
from pathlib import Path
import streamlit as st

# Ensure src/ is on Python module search path
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Attempt backend import
try:
    from assistant.rules import reply, load_offices
    BACKEND_AVAILABLE = True
    BACKEND_ERROR = None
except Exception as exc:  # pragma: no cover - fallback safety
    BACKEND_AVAILABLE = False
    BACKEND_ERROR = str(exc)

    def reply(message: str) -> str:  # type: ignore
        return f"[Fallback UI Response] Backend unavailable ({exc}). Input was: {message}"

    def load_offices() -> dict:  # type: ignore
        return {}


def init_session_state() -> None:
    """Initialize Streamlit session state for conversation messages and language."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "👋 **Hello! Welcome to Fitlens Campus Assistant.**\n\n"
                    "I can help you look up campus office locations, operating hours, and student services. "
                    "Try asking a question in English or Vietnamese, or click one of the quick suggestions below!"
                ),
            }
        ]
    if "language" not in st.session_state:
        st.session_state.language = "English"


def handle_user_query(query: str) -> None:
    """Process a user query by calling the assistant backend and appending to chat history."""
    clean_query = query.strip()
    if not clean_query:
        return

    # Append user message
    st.session_state.messages.append({"role": "user", "content": clean_query})

    # Call backend responder (src/assistant/rules.py)
    try:
        backend_response = reply(clean_query)
    except Exception as exc:
        backend_response = f"⚠️ An error occurred while contacting the backend: {exc}"

    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": backend_response})


def render_sidebar() -> None:
    """Render the sidebar containing campus office directory and backend status."""
    with st.sidebar:
        st.markdown("## 🎓 Fitlens Assistant")
        st.caption("Campus Virtual Assistant — UI Prototype")

        # System Status Pill
        if BACKEND_AVAILABLE:
            st.success("🟢 Backend: Connected (`src.assistant.rules`)", icon="✅")
        else:
            st.error(f"🔴 Backend Offline: {BACKEND_ERROR}", icon="⚠️")

        st.divider()

        # Language Selector
        st.markdown("### 🌐 Language / Ngôn ngữ")
        selected_lang = st.radio(
            "Select language:",
            ["English", "Tiếng Việt"],
            index=0 if st.session_state.get("language", "English") == "English" else 1,
            label_visibility="collapsed",
        )
        st.session_state.language = selected_lang

        st.divider()

        # Campus Office Directory Quick Lookup
        st.markdown("### 🏢 Campus Directory")
        try:
            offices = load_offices()
            if offices:
                for _, info in offices.items():
                    with st.expander(f"📍 {info['name']}"):
                        st.write(f"**Room:** {info['room']}")
                        st.write(f"**Hours:** {info['hours']}")
            else:
                st.info("Directory data currently empty or loading.")
        except Exception:
            st.info("Directory data currently loading.")

        st.divider()

        # Quick Actions
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            init_session_state()
            st.rerun()

        st.caption("Fitlens UI Module · Component: ui · Size: S · CS252 Group 01")


def render_chat_interface() -> None:
    """Render the main chat feed, quick action prompt chips, and input container."""
    st.title("💬 Fitlens Campus Chat")
    st.markdown(
        "Ask questions about campus offices and student regulations in **English** or **Vietnamese**."
    )

    # Quick Suggestion Chips
    st.markdown("##### ⚡ Quick Questions:")
    chip_col1, chip_col2, chip_col3, chip_col4 = st.columns(4)

    with chip_col1:
        if st.button("📍 Where is Training Office?", use_container_width=True):
            handle_user_query("Where is the Training Office?")
            st.rerun()
    with chip_col2:
        if st.button("📚 Library Hours?", use_container_width=True):
            handle_user_query("library opening hours")
            st.rerun()
    with chip_col3:
        if st.button("📋 List All Offices", use_container_width=True):
            handle_user_query("list offices")
            st.rerun()
    with chip_col4:
        if st.button("ℹ️ Help / Hướng dẫn", use_container_width=True):
            handle_user_query("help")
            st.rerun()

    st.write("")

    # Chat history display
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input box
    prompt = st.chat_input("Ask Fitlens anything about campus locations or hours...")
    if prompt:
        handle_user_query(prompt)
        st.rerun()


def render_architecture_expander() -> None:
    """Render expandable section showing architectural call stack for documentation."""
    with st.expander("🛠️ How this UI calls the Backend (Architecture & API)"):
        st.markdown(
            """
            ### Backend Call Sequence
            1. **User Interaction**: Student enters a query via `st.chat_input()` or clicks a quick prompt pill.
            2. **UI Handler**: `handle_user_query(query)` normalizes and trims the query.
            3. **Backend Invocation**: Directly invokes `assistant.rules.reply(clean_query)` from `src/assistant/rules.py`.
            4. **Data Normalization & Lookup**: Backend removes diacritics/case, checks aliases, and queries `data/offices.csv`.
            5. **Response Render**: The returned string is added to `st.session_state.messages` and rendered in `st.chat_message()`.
            """
        )


def main() -> None:
    """Main entry point for the Streamlit application."""
    init_session_state()
    render_sidebar()
    render_chat_interface()
    render_architecture_expander()


if __name__ == "__main__":
    main()
