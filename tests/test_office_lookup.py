import pytest

from assistant import rules


@pytest.mark.parametrize(
    ("question", "expected"),
    [
        ("where is training", "Training Office: room I.101, open 08:00-16:00."),
        ("Where is STUDENT?", "Student Affairs: room I.102, open 09:00-17:00."),
    ],
)
def test_partial_office_name(question, expected, sample_offices):
    assert rules.reply(question, sample_offices) == expected


@pytest.mark.parametrize("question", ["where is the office", "retraining", "visit"])
def test_generic_words_and_substrings_do_not_match(question, sample_offices):
    assert "don't know" in rules.reply(question, sample_offices)


@pytest.mark.parametrize(
    ("question", "office"),
    [
        ("Where is the Training Office?", "Training Office"),
        ("Phòng đào tạo ở đâu?", "Training Office"),
        ("where is IT?", "IT Helpdesk"),
        ("thư viện ở đâu", "Library"),
    ],
)
def test_full_names_and_aliases_still_work(question, office, sample_offices):
    assert rules.reply(question, sample_offices).startswith(f"{office}: room ")


def test_ambiguous_partial_name_asks_for_clarification(sample_offices):
    sample_offices["training support"] = {
        "name": "Training Support", "room": "T.200", "hours": "09:00-15:00"
    }
    assert rules.reply("training", sample_offices) == (
        "Please specify an office: Training Office, Training Support."
    )
    assert rules.reply("Training Office", sample_offices).startswith(
        "Training Office: room I.101"
    )


def test_partial_lookup_loads_csv(tmp_path, monkeypatch):
    """Exercise the default loading path without relying on the team's live CSV."""
    path = tmp_path / "offices.csv"
    path.write_text(
        "name,room,hours\nTraining Office,I.101,08:00-16:00\n", encoding="utf-8-sig"
    )
    load_offices = rules.load_offices
    monkeypatch.setattr(rules, "load_offices", lambda: load_offices(path))
    assert rules.reply("training") == "Training Office: room I.101, open 08:00-16:00."


def test_lookup_with_no_offices_does_not_invent_an_answer():
    assert "don't know" in rules.reply("training", {})
