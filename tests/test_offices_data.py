import csv
from pathlib import Path

import pytest

from assistant import rules

OFFICES_CSV = Path(__file__).resolve().parents[1] / "data" / "offices.csv"


def read_rows():
    with OFFICES_CSV.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        assert reader.fieldnames == ["name", "room", "hours"]
        return list(reader)


def test_csv_is_valid_and_has_six_offices():
    rows = read_rows()
    assert len(rows) >= 6
    for row in rows:
        assert all((row[field] or "").strip() for field in ("name", "room", "hours")), row


def test_office_names_are_unique_after_normalization():
    names = [rules.normalize(row["name"]) for row in read_rows()]
    assert len(names) == len(set(names))


@pytest.mark.parametrize(
    ("question", "expected"),
    [
        (
            "Where is the Faculty of Information Technology Office?",
            "Faculty of Information Technology Office: room I.53 (Building I), "
            "open Mon-Fri 08:00-12:00 and 13:30-17:00.",
        ),
        (
            "văn phòng khoa CNTT ở đâu?",
            "Faculty of Information Technology Office: room I.53 (Building I), "
            "open Mon-Fri 08:00-12:00 and 13:30-17:00.",
        ),
        (
            "Where is the Inspection and Legal Office?",
            "Inspection and Legal Office: room F107 (Nguyen Van Cu campus), "
            "open Not published on the office page.",
        ),
        (
            "phòng thanh tra pháp chế ở đâu",
            "Inspection and Legal Office: room F107 (Nguyen Van Cu campus), "
            "open Not published on the office page.",
        ),
    ],
)
def test_lookup_of_new_offices(question, expected):
    assert rules.reply(question) == expected


def test_list_offices_includes_new_offices():
    answer = rules.reply("list offices")
    for name in ("Library", "Special Programs Office", "Inspection and Legal Office"):
        assert f"- {name}" in answer
