from __future__ import annotations

import csv
from pathlib import Path

# ponytail: Simple static CSV validation; upgrade to an automated evaluator script when implementing issue #15 (eval/run.py)

EVAL_CSV = Path(__file__).resolve().parents[1] / "eval" / "cases.csv"


def test_eval_cases_file_exists():
    assert EVAL_CSV.is_file(), f"Expected benchmark file at {EVAL_CSV}"


def test_eval_cases_schema_and_contents():
    with EVAL_CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["question", "expected", "category"]
        rows = list(reader)

    assert len(rows) >= 15, f"Expected at least 15 benchmark questions, found {len(rows)}"

    allowed_categories = {"normal", "edge", "out-of-scope"}
    edge_cases = 0

    for idx, row in enumerate(rows, start=1):
        assert row["question"].strip() != "" or row["category"] == "edge", (
            f"Row {idx} has an empty question outside of intentional edge cases."
        )
        assert row["expected"].strip() != "", f"Row {idx} has an empty expected answer."
        assert row["category"] in allowed_categories, (
            f"Row {idx} has invalid category '{row['category']}'."
        )
        if row["category"] == "edge":
            edge_cases += 1

    assert edge_cases >= 3, f"Expected at least 3 edge cases, found {edge_cases}"
