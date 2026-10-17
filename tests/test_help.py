import pytest

from assistant import rules
from assistant.__main__ import main


@pytest.mark.parametrize(
    "command", ["help", "HELP", "  help  ", "Help!", "trợ giúp", "huong dan"]
)
def test_help(command):
    response = rules.reply(command, {})
    assert "office locations and opening hours" in response
    assert "list offices" in response
    assert "Examples:" in response
    assert "quit" in response


def test_help_does_not_require_office_data(monkeypatch):
    def unexpected_load():
        pytest.fail("Help should not need to read the office CSV")

    monkeypatch.setattr(rules, "load_offices", unexpected_load)
    assert "Commands:" in rules.reply("help")


def test_help_from_command_line(capsys):
    assert main(["help"]) == 0
    output = capsys.readouterr().out
    assert "office locations and opening hours" in output
    assert "list offices" in output


def test_help_in_interactive_mode(monkeypatch, capsys):
    messages = iter(["help", "quit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(messages))
    assert main([]) == 0
    output = capsys.readouterr().out
    assert "Commands:" in output
    assert "list offices" in output
