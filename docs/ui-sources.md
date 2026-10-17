# UI Design: Showing Sources Under Each Answer

This document specifies the design and layout for displaying **sources and citations** under each answer in the Fitlens campus assistant user interface.

- **Component**: `ui`
- **Issue**: UI: show sources under each answer (Size M)
- **Acceptance Criteria**: Mockup in `docs/ui-sources.md` with 2 examples.

---

## 1. Overview & Objectives

When students ask questions about campus locations, department hours, or academic policies, displaying the underlying data source builds trust and enables students to verify critical information.

### Design Goals
1. **Clear Attribution**: Every factual answer displays the exact dataset, document, or record it was derived from.
2. **Uncluttered Presentation**: The answer itself remains primary and easy to read; source details sit directly below in a dedicated citation tray.
3. **Traceability**: Sources link back to the local data repository (e.g., `data/offices.csv`) or official campus publications.

---

## 2. Visual Mockup & Component Layout

Each assistant message is rendered in a chat card. The answer is presented first, followed immediately by a **"Sources"** container.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🤖 Fitlens Assistant                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Training Office: room I.101, open 07:30 - 11:30 and 13:00 - 16:30          │
│  (Mon - Fri).                                                               │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📚 Sources (1)                                                            ▲ │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ 🏢 Campus Office Directory                        [data/offices.csv]    │ │
│ │ Entry: Training Office · Room: I.101                                    │ │
│ │ Schedule: 07:30 - 11:30, 13:00 - 16:30 (Mon - Fri)                      │ │
│ │ Confidence: 100% exact match                                            │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown
- **Answer Text**: Prominent response formatted in clean markdown.
- **Sources Divider**: Subtle horizontal rule separating the answer from attribution.
- **Source Header**: `📚 Sources (N)` with an expand/collapse toggle for mobile screens.
- **Source Item Card**:
  - **Icon & Title**: Visual category icon (`🏢` for offices, `📘` for handbooks, `📅` for calendar).
  - **Source File / URL Tag**: Monospace badge indicating the file path (e.g., `data/offices.csv`).
  - **Matched Record Details**: Key-value pairs extracted from the data source.
  - **Verification Status**: Badge showing `Verified Data` or confidence indicator.

---

## 3. Concrete Examples (Acceptance Criteria)

Below are **two realistic examples** showing how different student queries display sources under their respective answers.

---

### Example 1: Office Location & Hours Lookup (Single Source)

#### Student Query
> *"Where is the Training Office and when does it open?"*

#### UI Mockup

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 👤 Student: Where is the Training Office and when does it open?             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🤖 Fitlens Assistant                                                        │
│                                                                             │
│ The Training Office is located in room I.101. It is open Monday through     │
│ Friday from 07:30 to 11:30 and 13:00 to 16:30.                              │
│                                                                             │
│ ─────────────────────────────────────────────────────────────────────────── │
│ 📚 Sources (1)                                                              │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ 🏢 Campus Office Directory                        [Source: Verified CSV]│ │
│ │ File: data/offices.csv (Row 1)                                          │ │
│ │ Match: name = "Training Office"                                         │ │
│ │ Record:                                                                 │ │
│ │   • room: I.101                                                         │ │
│ │   • hours: 07:30 - 11:30 and 13:00 - 16:30 (Mon - Fri)                  │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Example 2: Study Space & Weekend Facility Query (Multiple / Extended Source)

#### Student Query
> *"Can I study at the library this Saturday?"*

#### UI Mockup

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 👤 Student: Can I study at the library this Saturday?                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🤖 Fitlens Assistant                                                        │
│                                                                             │
│ Yes! The Campus Library is located in room B.201 and is open on Saturdays.  │
│ Operating hours are from 08:00 to 20:00 (Monday through Saturday).          │
│                                                                             │
│ ─────────────────────────────────────────────────────────────────────────── │
│ 📚 Sources (1)                                                              │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ 📖 Central Campus Library Directory               [Source: Verified CSV]│ │
│ │ File: data/offices.csv (Row 3)                                          │ │
│ │ Match: name = "Library"                                                 │ │
│ │ Record:                                                                 │ │
│ │   • room: B.201                                                         │ │
│ │   • hours: 08:00 - 20:00 (Mon - Sat)                                    │ │
│ │   • note: Open on Saturday; closed on Sunday and public holidays        │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Backend Data Schema

To support this UI component, the backend response format will return both the generated reply and the list of source records:

```json
{
  "query": "Where is the Training Office?",
  "reply": "Training Office: room I.101, open 07:30 - 11:30 and 13:00 - 16:30 (Mon - Fri).",
  "sources": [
    {
      "id": "src-office-001",
      "type": "csv_record",
      "title": "Campus Office Directory",
      "file": "data/offices.csv",
      "matched_key": "Training Office",
      "data": {
        "room": "I.101",
        "hours": "07:30 - 11:30 and 13:00 - 16:30 (Mon - Fri)"
      },
      "confidence": 1.0
    }
  ]
}
```

---

## 5. Streamlit Rendering Implementation

In Streamlit (`ui/app.py`), sources are rendered directly beneath the chat response using `st.expander`:

```python
import streamlit as st


def render_response_with_sources(response: dict) -> None:
    # 1. Main answer
    st.markdown(response["reply"])

    # 2. Sources container under the answer
    sources = response.get("sources", [])
    if sources:
        with st.expander(f"📚 Sources ({len(sources)})", expanded=True):
            for src in sources:
                st.caption(f"**{src['title']}** — `{src['file']}`")
                for key, val in src.get("data", {}).items():
                    st.write(f"- **{key.title()}:** {val}")
```

---

## 6. Definition of Done Compliance

- [x] Acceptance criteria in the issue are met (Mockup in `docs/ui-sources.md` with 2 examples).
- [x] Code / design is on a dedicated feature branch (`issue-7-show-sources-under-each-answer`).
- [x] Written 100% in clear, concise English.
- [x] No secrets, personal data, or large binary files committed.
- [x] Streamlit implementation pattern and data schema defined.
