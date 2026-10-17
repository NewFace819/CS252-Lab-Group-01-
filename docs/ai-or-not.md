# Which Questions Need AI? (draft)

Fitlens answers with rules first (`src/assistant/rules.py`) and only calls an AI model when the
routing rules in [ai-interface.md](ai-interface.md) §1 say so. This page gives examples on each
side of that line.

**Rule of thumb:** if the answer is one fixed row of our data or a fixed reply, rules are enough.
If the bot must understand a free-form request, combine several rows or explain something, it is
a **candidate** for AI — and even then the AI may only use our data.

"Candidate" matters: some of these questions are AI-assisted only because **today's rules do
not support them**, not because they cannot be solved deterministically. Comparing closing times
(Q12, Q19), checking a weekday (Q16) or listing all hours (Q17) could be done with structured
hours data and normal code. The team should pick the simplest option that can be tested, at the
lowest cost and latency.

## Test fixture

Results below were checked by running each question through `reply()` with these four sample rows.
They are **not** verified campus data. The real `data/offices.csv` is currently empty, so Q5–Q9
are not yet proven with real data.

| name | room | hours |
| --- | --- | --- |
| Training Office | I.101 | 7:30-16:30 |
| Library | C.201 | 7:30-20:00 |
| Student Affairs | B.1 | 8-16 |
| IT Helpdesk | E.1 | 8-17 |

## 10 questions that do NOT need AI

| # | Question | Reason |
| --- | --- | --- |
| 1 | hi | Fixed greeting; exact match in `GREETINGS`. |
| 2 | xin chào | Same greeting after removing accents (`normalize`). |
| 3 | help | Fixed command with a fixed reply (`HELP_TEXT`). |
| 4 | danh sach van phong | Fixed command; the list comes straight from `offices.csv`. |
| 5 | Where is the Training Office? | Office name appears in the question; room is one CSV cell. |
| 6 | thu vien o dau? | Alias "thu vien" maps to Library; deterministic lookup. |
| 7 | Phòng Đào tạo mở cửa khi nào? | Accents removed, alias "phong dao tao" matches; hours are one CSV cell. |
| 8 | ctsv o dau | Short alias for Student Affairs; a keyword match is enough. |
| 9 | IT helpdesk room? | Office name match; whole-word matching avoids false hits like "visit". |
| 10 | good morning | Fixed greeting; an AI call would only add cost and latency. |

## 10 candidate AI-assisted questions

"Today's rules" is what `reply()` returns with the fixture above. "Expected" is the correct
behaviour once the routing in [ai-interface.md](ai-interface.md) is built.

| # | Question | Why rules are not enough today | Expected |
| --- | --- | --- | --- |
| 11 | I lost my student card, what should I do? | Asks for a procedure; rules return "I don't know". | Answer only if the context has an official student-card procedure; otherwise abstain. |
| 12 | So sánh giờ mở cửa thư viện và phòng CNTT giúp mình | Two offices; rules return only Library. Could be deterministic with structured hours. | Compare both opening hours, citing both rows. |
| 13 | Where can I print documents on campus? | No office name or keyword in our data; rules return "I don't know". | Point to an office only if the context has an official printing-service source; otherwise abstain. |
| 14 | Mình cần xin giấy xác nhận sinh viên thì đi đâu? | No office name; our schema (name/room/hours) has no list of services. | Route to an office only if the context has an official source for this service; otherwise abstain. |
| 15 | What is the difference between Student Affairs and the Training Office? | Asks for an explanation; rules wrongly reply with Training Office's room. | Explain only from official descriptions in the context; with today's schema, abstain. |
| 16 | Is the library open on Sunday? | Needs a yes/no about one day; rules only print Library's hours. Could be deterministic with structured opening days. | Yes/no based on the Library row; abstain if the hours do not mention days. |
| 17 | Summarize the opening hours of all offices in one sentence. | Combines all rows; rules return "I don't know". A template could also do it. | One sentence covering every office, citing all rows. |
| 18 | My Wi-Fi password does not work, who can help? | Problem description without an office name; rules return "I don't know". | Route to IT Helpdesk only if the context says it handles Wi-Fi; otherwise abstain. |
| 19 | Thư viện với phòng đào tạo, chỗ nào đóng cửa muộn hơn? | Two offices; rules return only Training Office. Could be deterministic with structured hours. | "Library closes later (20:00 vs 16:30)", citing both rows. |
| 20 | I'm a new student, what should I do in my first week? | Open-ended; rules return "I don't know". | Short answer from available sources only; abstain on anything not in our data. |

## Notes

- **Matched is not answered.** Q12, Q15, Q16 and Q19 contain an office name, so today's rules
  return one office's room and hours — the wrong kind of answer, not "unknown". The routing rule
  in [ai-interface.md](ai-interface.md) §1 (intent check before lookup) sends them to the AI path.
  The trigger words there are examples, not a complete list; equivalent phrasings and questions
  about several offices need the same treatment.
- Partial-name matching (issue #8) may increase false matches. Re-run this table when it is
  merged.
- **Abstain is a correct answer.** If our data does not contain the answer, the correct reply is
  "I don't have that information yet", not a guess from the model's general knowledge.
- Out-of-scope questions (for example "what is the meaning of life") need neither path: the bot
  should politely say it only covers campus offices.
- **For the benchmark (issue #14):** reuse the fixture rows, the question, and the "Expected"
  column — not only a "needs AI" label — so the evaluation can tell a correct answer, a correct
  abstention and a made-up answer apart.
