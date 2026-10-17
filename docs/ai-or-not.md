# Which Questions Need AI? (draft)

Fitlens answers with rules first (`src/assistant/rules.py`) and only calls an AI model when the
rules cannot help (see [ai-interface.md](ai-interface.md)). This table shows where that line is.

**Rule of thumb:** if the answer is one fixed row of our data or a fixed reply, rules are enough.
If the bot must understand intent, combine several sources or explain something, it needs AI —
and even then the AI may only use our data.

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

## 10 questions that DO need AI

| # | Question | Reason |
| --- | --- | --- |
| 11 | I lost my student card, what should I do? | Needs a short multi-step answer, not a single data lookup. |
| 12 | So sánh giờ mở cửa thư viện và phòng CNTT giúp mình | Combines two rows; rules would answer only the first office they match. |
| 13 | Where can I print documents on campus? | Intent ("printing") has no keyword in our data; the bot must infer the right office. |
| 14 | Mình cần xin giấy xác nhận sinh viên thì đi đâu? | No office name in the question; must map the request to Student Affairs. |
| 15 | What is the difference between Student Affairs and the Training Office? | Asks for an explanation; rules would wrongly reply with one office's room. |
| 16 | Is the library open on Sunday? | Must reason over the hours text and answer yes/no; rules only print the hours. |
| 17 | Summarize the opening hours of all offices in one sentence. | Summarizing several rows into new text. |
| 18 | My Wi-Fi password does not work, who can help? | Problem description without an office name; must route to IT Helpdesk. |
| 19 | Thư viện với phòng đào tạo, chỗ nào đóng cửa muộn hơn? | Comparison and ordering across two rows. |
| 20 | I'm a new student, what should I do in my first week? | Open-ended; needs to plan an answer from several sources. |

## Notes

- Questions 1–10 assume `data/offices.csv` contains the Training Office, Library,
  Student Affairs and IT Helpdesk rows.
- For questions 11–20, the AI may only use the context the backend passes in. If our data does
  not contain the answer (for example the student card procedure in #11), the correct reply is
  "I don't have that information yet", not a guess.
- Questions 12, 15, 16 and 19 contain an office name, so today's rules return an answer —
  but the wrong kind (one office's room and hours). Before calling the AI, the backend must
  notice comparison or explanation words ("so sánh", "difference", "open on Sunday",
  "muộn hơn"), not only "no match".
- Out-of-scope questions (for example "what is the meaning of life") need neither path:
  the bot should politely say it only covers campus offices.
- These 20 questions can seed the benchmark in `eval/cases.csv` (issue #14).
