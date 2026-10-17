# AI Service Interface (draft)

This document defines how Fitlens will call a large language model (LLM) in the future.
**No LLM is called yet.** The goal is to agree on the contract first, so the backend, UI,
evaluation and security work can build against it.

## 1. Where the AI fits

Rules answer first. The AI is only a fallback for questions the rules cannot answer.

```text
user message
    │
    ▼
rules.reply(message)  ── matched ──►  answer from data (no AI)
    │
    │ not matched ("I don't know that yet...")
    ▼
retrieve context (rows from data/, at most 5)
    │
    ▼
ask_ai(question, context)  ── ok ──►  AIAnswer (with sources)
    │
    │ AIError
    ▼
fallback: the rules' "I don't know" reply + hint to type 'help'
```

See [ai-or-not.md](ai-or-not.md) for which questions belong on each path.

## 2. Function signature

The function will live in `src/assistant/ai.py`.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    id: str      # stable id, e.g. "offices.csv:training-office"
    title: str   # short label shown to the user, e.g. "Training Office"
    text: str    # the content the model may use, e.g. "room I.101, open Mon-Fri 7:30-16:30"


@dataclass(frozen=True)
class AIAnswer:
    text: str                    # answer shown to the user
    source_ids: tuple[str, ...]  # ids of the Sources the answer is based on
    model: str                   # model name, for logs and evaluation
    used_ai: bool = True


def ask_ai(
    question: str,
    context: list[Source],
    *,
    language: str | None = None,
    timeout_s: float = 10.0,
) -> AIAnswer:
    """Answer `question` using only `context`. Raise AIError on any failure."""
```

## 3. Inputs

| Parameter | Type | Rules |
| --- | --- | --- |
| `question` | `str` | Stripped, not empty, at most 500 characters. Raw user text (not the normalized form), so the model sees accents. |
| `context` | `list[Source]` | 0–5 items, chosen by the backend from `data/`. Never the whole dataset. |
| `language` | `"vi"`, `"en"` or `None` | Language of the answer. `None` means "answer in the language of the question". |
| `timeout_s` | `float` | Maximum wait for the model, 1–30 seconds. |

## 4. Outputs

`ask_ai` returns an `AIAnswer`:

- `text` answers the question in at most 120 words.
- Every fact in `text` comes from `context`. `source_ids` lists the sources used and is never
  empty when the answer contains a fact.
- If `context` does not contain the answer, `text` says so (for example
  "I don't have that information yet.") and `source_ids` is empty. The model must not guess
  rooms, hours or rules.

Example:

```python
ask_ai(
    "Phòng đào tạo với thư viện, chỗ nào đóng cửa muộn hơn?",
    [
        Source("offices.csv:training-office", "Training Office", "room I.101, open 7:30-16:30"),
        Source("offices.csv:library", "Library", "room C.201, open 7:30-20:00"),
    ],
)
# AIAnswer(text="Thư viện đóng cửa muộn hơn (20:00) so với Phòng Đào tạo (16:30).",
#          source_ids=("offices.csv:library", "offices.csv:training-office"),
#          model="<model-name>")
```

The room numbers and hours above are examples only.

## 5. Errors

All errors inherit from one base class, so callers can catch them in one place.

| Error | When |
| --- | --- |
| `ValueError` | `question` is empty or too long, `context` has more than 5 items, or `timeout_s` is out of range. This is a bug in the caller, not an AI failure. |
| `AIError` | Base class for the errors below. |
| `AIUnavailableError` | No API key, network error, or the model did not answer within `timeout_s`. |
| `AIRateLimitError` | The provider rejected the request because of rate or quota limits. |
| `AIInvalidResponseError` | The reply cannot be parsed, or it states facts without any `source_ids`. |

## 6. Fallback

The user never sees an AI error or a stack trace.

1. If `ask_ai` raises any `AIError`, the backend returns the rules' reply:
   "I don't know that yet. Type 'help' for examples or 'list offices' for office names."
2. The error type (not the question, not the key) is logged for the team.
3. If the AI is turned off (no API key configured), the backend skips `ask_ai` entirely.

## 7. Security and privacy

- The API key is read from the environment variable `FITLENS_AI_API_KEY`
  (listed in `.env.example`, issue #16). It is never committed, printed or logged.
- Only `question` and the selected `context` are sent to the provider. No student IDs,
  names, phone numbers or other personal data are put in `context`.
- Logs record the error type, latency and model name — not the full question.

## 8. Testing plan

- Unit tests replace `ask_ai` with a fake, so tests never call the network.
- One test per error type checks that the user receives the fallback reply.
- One test checks that questions answered by rules never reach `ask_ai`.
- The evaluation set (issue #14) marks which benchmark questions are expected to use AI.

## 9. Open questions

- Which provider and model to use, and what it costs per month.
- Whether to keep short conversation history (follow-up questions).
- Whether answers should show sources to the user (see issue #7, UI sources).
