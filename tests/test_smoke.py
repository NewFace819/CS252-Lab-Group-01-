from assistant.rules import reply


def test_greeting():
    assert "Hello" in reply("hi")


def test_office_lookup(sample_offices):
    assert "I.101" in reply("Where is the Training Office?", sample_offices)


def test_unknown():
    assert "don't know" in reply("what is the meaning of life")


def test_empty():
    assert reply("   ") == "Please type a question."
