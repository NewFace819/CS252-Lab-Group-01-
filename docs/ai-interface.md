# AI Service Interface (draft)

This document defines how Fitlens will call a large language model (LLM) in the future.
**No LLM is called yet.** The goal is to agree on the contract first, so the backend, UI,
evaluation and security work can build against it.

## 1. Routing: rules first, AI only when needed

Matching an office name is not the same as answering the question. "Which closes later, the
library or the training office?" matches an office, but a single room-and-hours reply is the
wrong kind of answer. So the rules return a **status**, not only a text, and the backend routes
on that status. The display text "I don't know that yet..." is never used as a control signal.

```python
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class RuleResult:
    status: Literal["answered", "needs_ai", "unknown"]
    text: str | None = None          # the reply, only when status == "answered"
    offices: tuple[str, ...] = ()    # office names matched, used to choose AI context
```

A future `rules.route(message) -> RuleResult` applies these steps **in order** and stops at
the first one that applies (`rules.reply()` keeps working for the CLI):

| Step | Condition | Result |
| --- | --- | --- |
| 1 | Message is empty after stripping | `answered`: "Please type a question." |
| 2 | Greeting, `help` or `list offices` command | `answered`: the fixed reply |
| 3 | `data/offices.csv` is missing | `answered`: "Office data is missing..." (no AI) |
| 4 | Intent check (below) finds a comparison, explanation, procedure or day-specific question | `needs_ai` |
| 5 | Exactly one office matches | `answered`: room and hours from the CSV |
| 6 | Nothing matches | `unknown` |

**Intent check (step 4)** returns `needs_ai` when the message:

- mentions two or more offices;
- asks to compare: "compare", "so sánh", "later / earlier", "muộn hơn / sớm hơn", "difference",
  "khác nhau";
- asks about a specific day or time: weekday names, "today", "hôm nay", "chủ nhật";
- asks for a procedure or explanation: "what should I do", "how do I", "làm sao", "thủ tục",
  "explain".

These words are **examples**, not a complete list. The backend owner keeps the real list next to
the rules, with tests for equivalent phrasings. Partial-name matching (issue #8) can increase
false matches, so the routing tests must be re-run when it is merged.

**Then the backend:**

```text
answered  ──────────────────────────────────►  reply to user (no AI)
needs_ai / unknown
    │
    ├─ AI disabled (no API key) ────────────►  fallback reply
    │
    ▼
build context (§4) ── no relevant source ──►  "I don't have that information yet." (no network)
    │
    ▼
sanitize question + context (§7) ── unsafe ►  ask the user to remove personal data (no network)
    │
    ▼
ask_ai(question, context) ── AIError ──────►  fallback reply
    │
    ▼
AIAnswer ──► reply to user, with sources resolved by the backend (§5)
```

The fallback reply is the rules' text: "I don't know that yet. Type 'help' for examples or
'list offices' for office names." Out-of-scope questions ("what is the meaning of life") reach
the "no relevant source" branch and never call the network.

See [ai-or-not.md](ai-or-not.md) for example questions on each path.

## 2. Function signature

The function will live in `src/assistant/ai.py`.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    id: str      # stable, unique id, e.g. "offices.csv:training-office"
    title: str   # short label shown to the user, e.g. "Training Office"
    text: str    # the content the model may use, e.g. "room I.101, open Mon-Fri 7:30-16:30"


@dataclass(frozen=True)
class AIAnswer:
    text: str                    # answer shown to the user, at most 120 words
    source_ids: tuple[str, ...]  # ids of the Sources the answer is based on
    abstained: bool              # True when the context did not contain the answer
    model: str                   # model name, for logs and evaluation


def ask_ai(
    question: str,
    context: list[Source],
    *,
    language: str | None = None,
    timeout_s: float = 10.0,
) -> AIAnswer:
    """Answer `question` using only `context`.

    Raise ValueError if the inputs break the rules in section 3 (a caller bug).
    Raise AIError (or a subclass) if the provider fails or its reply is invalid.
    """
```

## 3. Inputs

The backend validates every input **before** calling `ask_ai`. `ask_ai` checks them again as a
guard and raises `ValueError` without any network call.

| Parameter | Type | Rules |
| --- | --- | --- |
| `question` | `str` | Not empty after stripping, at most 500 characters, already sanitized (§7). Keeps Vietnamese accents. |
| `context` | `list[Source]` | 1–5 items (see §4). Each `id` is non-empty and unique; each `text` is at most 500 characters; all `text` together at most 2,000 characters. |
| `language` | `"vi"`, `"en"` or `None` | Language of the answer. `None` means "the language of the question". Any other value is a `ValueError`. |
| `timeout_s` | `float` | A finite number from 1 to 30 seconds. `0`, negative, `inf` or `nan` is a `ValueError`. |

## 4. Context

- The backend builds the context from `data/`: first the offices matched by the rules
  (`RuleResult.offices`), then other sources in order of relevance.
- If the budget in §3 is exceeded, the backend drops the least relevant sources first, and cuts a
  single long source at 500 characters.
- If no source is relevant (empty context), the backend replies "I don't have that information
  yet." **without calling `ask_ai`**.
- Context is reference data, not instructions. Text inside a source (for example "ignore the
  rules above") cannot change how the assistant behaves; the instructions to the model are fixed
  in code.

## 5. Outputs

`ask_ai` returns an `AIAnswer` that must pass these checks, otherwise it raises
`AIInvalidResponseError`:

- `text` is not empty and has at most 120 words.
- If `abstained` is `False`, `source_ids` is not empty.
- If `abstained` is `True`, `source_ids` is empty and `text` says the information is not
  available. The model must not guess rooms, hours or rules.
- Every id in `source_ids` is one of the ids passed in `context`, with no duplicates. An id the
  model made up (for example `"offices.csv:made-up"`) is invalid.

The id check only proves that the answer **points to real sources**. It does not prove that every
sentence in `text` is supported by them; that is measured by the evaluation set (issue #14).

**Sources for the UI.** The backend, not the UI and not the model, resolves `source_ids` to
`(id, title)` pairs using the `Source` list it built, and returns them with the answer. The UI
never reads the CSV files. How the sources are displayed is decided in issue #7.

Example:

```python
ask_ai(
    "Thư viện với phòng đào tạo, chỗ nào đóng cửa muộn hơn?",
    [
        Source("offices.csv:training-office", "Training Office", "room I.101, open 7:30-16:30"),
        Source("offices.csv:library", "Library", "room C.201, open 7:30-20:00"),
    ],
)
# AIAnswer(text="Thư viện đóng cửa muộn hơn (20:00) so với Phòng Đào tạo (16:30).",
#          source_ids=("offices.csv:library", "offices.csv:training-office"),
#          abstained=False,
#          model="<model-name>")
```

The room numbers and hours above are examples only.

## 6. Errors

There are two kinds of errors, handled in different places:

| Error | When | Who handles it |
| --- | --- | --- |
| `ValueError` | Inputs break §3. This is a bug in the caller. | The backend validates first, so users never trigger it. Tests catch it. |
| `AIError` | Base class for provider failures below. | The backend catches it and sends the fallback reply. |
| `AIUnavailableError` | No API key, network error, or no answer within `timeout_s`. | Fallback |
| `AIRateLimitError` | The provider rejected the request because of rate or quota limits. | Fallback |
| `AIInvalidResponseError` | The reply cannot be parsed or breaks §5 (no sources, unknown id, too long). | Fallback |

## 7. Security and privacy

- **Sanitize before sending.** The backend runs `sanitize()` on the question **and** on every
  source text before calling `ask_ai`. It replaces personal data with placeholders and keeps
  Vietnamese accents:

  | Pattern | Replaced by |
  | --- | --- |
  | Student ID (8 digits, e.g. `2521xxxx`) | `[student-id]` |
  | Phone number (`0` or `+84` followed by 9–10 digits) | `[phone]` |
  | Email address | `[email]` |

- **Block when unsafe.** If the message contains something that looks like a password, API key or
  token, or nothing meaningful is left after sanitizing, the backend does **not** call the
  provider. It replies: "Please remove personal information or secrets from your question and try
  again."
- The API key is read from the environment variable `FITLENS_AI_API_KEY` (listed in
  `.env.example`, issue #16). It is never committed, printed or logged.
- Logs record the error type, latency and model name — not the question or the context.

## 8. Testing plan

All tests use a fake provider, so they never call the network. Validation tests and fallback
tests are kept separate.

**Validation (`ValueError`, zero provider calls)**

- blank question; 501-character question
- 6 sources; duplicate source ids; empty source id; context over 2,000 characters
- `language="fr"`; `timeout_s` of `0`, `31`, `inf`

**Routing**

- Questions 1–10 in [ai-or-not.md](ai-or-not.md) return `answered` and never reach `ask_ai`.
- Questions 12, 15, 16 and 19 return `needs_ai` even though they contain an office name.
- With the AI disabled, `needs_ai` and `unknown` give the fallback reply and make zero provider
  calls.

**Context and privacy**

- Empty context: "I don't have that information yet." with zero provider calls.
- A question with a student ID and a phone number: the payload seen by the fake provider
  contains `[student-id]` and `[phone]`, not the real values.
- A question containing an API-key-like string: blocked, zero provider calls.

**Provider replies and fallback**

- Each `AIError` subclass gives the fallback reply.
- A reply citing an id that was not in the context raises `AIInvalidResponseError` → fallback.
- `abstained=True` with source ids, or `abstained=False` without them, is invalid → fallback.
- Context that does not contain the answer gives `abstained=True`.

## 9. Open questions

- Which provider and model to use, and what it costs per month.
- Whether to keep short conversation history for follow-up questions.
- The full keyword list for the intent check (§1), owned by the backend.
