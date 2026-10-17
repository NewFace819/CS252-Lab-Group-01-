# Data sources and ownership

This directory stores office records used by the rule-based campus assistant.
The inventory below describes the current repository, not a verified campus
directory. Never invent room numbers or opening hours to fill missing records.

## Inventory

| File | Source and current status | Data owner | Update frequency |
| --- | --- | --- | --- |
| `offices.csv` | Empty in the Lab 1 setup (`v0.1-setup`). No external source URL or verified office records have been supplied. Adding public office data is tracked in [issue #10](https://github.com/NewFace819/CS252-Lab-Group-01-/issues/10). | `@npdwuy`, assigned to issue #10; documentation maintained by `@vbthg` under issue #11. | Update when an official source changes or an error is confirmed; recheck sources before each data PR and each lab/milestone submission. |

The update frequency is the maintenance policy for this dataset, not a claim
that the currently empty file has already been checked against official sources.
If ownership changes, update this table in the same PR that changes the assignment.

## CSV format

The loader in [`src/assistant/rules.py`](../src/assistant/rules.py) expects UTF-8
(a UTF-8 BOM is also accepted) with the following header:

```csv
name,room,hours
```

- `name`: the office's public display name.
- `room`: the location exactly as stated by the source.
- `hours`: the public opening hours, including qualifications where necessary.

Use a CSV writer or quote values containing commas. Keep names unique after
case/accent normalization, and provide all three fields for each office. When
information cannot be verified, document the gap instead of guessing a value.

## Source records required for new data

Before merging office records, the data owner must add an entry to the source
register below for each office (several offices may share one source). Use public,
official university/office pages or a public official notice. Record the exact URL,
publisher, access date, which fields it supports, and the owner who verified it.
If different pages support location and hours, record both.

| Office / records covered | Public source URL and publisher | Fields supported | Accessed / verified on | Verified by |
| --- | --- | --- | --- | --- |
| None yet: `offices.csv` is empty. | No source supplied. | No verified fields. | Not yet verified. | Pending issue #10 (`@npdwuy`). |

The room `I.101` appearing in tests is a starter expectation, not source evidence
for a real campus location. Synthetic test records belong in tests and must be
labelled as synthetic; do not copy them into this source register as verified data.

## Update and review procedure

1. The data owner checks the public source and updates the CSV and source register
   together on a feature branch. Record source/access-date changes even if the
   office information itself stays the same.
2. Validate the header and non-empty fields, check for duplicate office names, and
   confirm that every record has source evidence. Do not include private contact
   details, student information, credentials or API keys.
3. Run `python -m pytest -q` from the repository root. For new office records,
   include lookup checks such as those required by issue #10.
4. Open a PR linking the data issue. A teammate verifies the source register and
   results before approval and merge, following the team's
   [Definition of Done](../lab02/templates/DEFINITION_OF_DONE.md).

This documentation change adds no office records and makes no claim that issue
#10 or real-data validation has been completed.
