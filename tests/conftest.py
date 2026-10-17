import pytest

from assistant.rules import normalize


@pytest.fixture
def sample_offices():
    """Synthetic locations for tests; not verified campus information."""
    rows = [
        {"name": "Training Office", "room": "I.101", "hours": "08:00-16:00"},
        {"name": "Student Affairs", "room": "I.102", "hours": "09:00-17:00"},
        {"name": "Library", "room": "L.201", "hours": "07:00-18:00"},
        {"name": "IT Helpdesk", "room": "I.103", "hours": "08:00-17:00"},
    ]
    return {normalize(row["name"]): row for row in rows}
