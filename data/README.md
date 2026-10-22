# Data sources and ownership

This directory stores office records used by the rule-based campus assistant.
The inventory below describes the current repository, not a verified campus
directory. Never invent room numbers or opening hours to fill missing records.

## Inventory

| File | Source and current status | Data owner | Update frequency |
| --- | --- | --- | --- |
| `offices.csv` | Six public office records for the Nguyen Van Cu campus (227 Nguyen Van Cu St.), copied from the official pages listed in the source register below. Added in [issue #10](https://github.com/NewFace819/CS252-Lab-Group-01-/issues/10). | `@npdwuy`, assigned to issue #10; documentation maintained by `@vbthg` under issue #11. | Update when an official source changes or an error is confirmed; recheck sources before each data PR and each lab/milestone submission. |

The update frequency is the maintenance policy for this dataset. Every record in
`offices.csv` is backed by a page in the source register below.
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
| Library | https://glib.hcmus.edu.vn/contact (HCMUS Library) | Location (Building I, 9th and 10th floor) and hours | 2026-10-22 | `@npdwuy` |
| Special Programs Office | https://www.ctda.hcmus.edu.vn/vi/contact/ (FIT, VNUHCM-US program office) | Room I.53 (Building I, 5th floor) and hours Mon-Fri 08:00-17:00 | 2026-10-22 | `@npdwuy` |
| Faculty of Information Technology Office | https://www.fit.hcmus.edu.vn/tin-tuc/d/thong-bao-ve-van-phong-khoa-cong-nghe-thong-tin (Faculty of IT notice dated 2025-06-06) | Room I.53 (Building I) and hours Mon-Fri 08:00-12:00, 13:30-17:00 | 2026-10-22 | `@npdwuy` |
| Testing and Quality Assurance Office | https://ktdbcl.hcmus.edu.vn/index.php (HCMUS Testing and Quality Assurance Office) | Hours Mon-Fri 07:30-11:30, 13:30-17:00. The page gives no room number, so `room` records the gap. | 2026-10-22 | `@npdwuy` |
| Information and Communications Office | https://tuyensinh.hcmus.edu.vn/lien-he/ (HCMUS admissions portal) | Room F02. The page lists only the hotline hours (08:00-17:00), so `hours` says so. | 2026-10-22 | `@npdwuy` |
| Inspection and Legal Office | https://ttpc.hcmus.edu.vn/ (HCMUS Inspection and Legal Office) | Room F107. The page gives no hours, so `hours` records the gap. | 2026-10-22 | `@npdwuy` |

The room `I.101` appearing in tests is a starter expectation, not source evidence
for a real campus location. Synthetic test records belong in tests and must be
labelled as synthetic; do not copy them into this source register as verified data.
Where a source does not publish a room or opening hours, the CSV says so instead of
guessing; fill the gap when an official page or notice provides the value.

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
