"""A small rule-based campus assistant; no external AI service required."""
from __future__ import annotations

import csv
from pathlib import Path
import re
import unicodedata

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
GREETINGS = {"hi", "hello", "hey", "xin chao", "chao", "good morning"}
HELP_COMMANDS = {"help", "tro giup", "huong dan"}
LIST_COMMANDS = {"list offices", "offices", "danh sach van phong"}
# Aliases point to names in the CSV; locations and hours always come from data.
OFFICE_ALIASES = {
    "training office": ("phong dao tao", "dao tao"),
    "student affairs": ("phong cong tac sinh vien", "cong tac sinh vien", "ctsv"),
    "library": ("thu vien",),
    "it helpdesk": ("it", "helpdesk", "ho tro cntt", "phong cntt"),
    "special programs office": ("van phong cac chuong trinh dao tao theo de an",),
    "faculty of information technology office": (
        "van phong khoa cong nghe thong tin", "van phong khoa cntt",
    ),
    "testing and quality assurance office": ("phong khao thi va dam bao chat luong",),
    "information and communications office": ("phong thong tin truyen thong",),
    "inspection and legal office": ("phong thanh tra phap che", "thanh tra phap che"),
}
HELP_TEXT = (
    "I can look up campus office locations and opening hours.\n"
    "Commands: help / tro giup; list offices / danh sach van phong.\n"
    "Examples: where is the training office?; thu vien o dau?; "
    "phong dao tao mo cua khi nao?\n"
    "Vietnamese text may include or omit accents. Type 'quit' to exit interactive mode."
)


def normalize(text: str) -> str:
    """Ignore case, Vietnamese accents, punctuation and extra whitespace."""
    text = unicodedata.normalize("NFD", text.casefold().replace("đ", "d"))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(re.sub(r"[^\w\s]", " ", text).split())


def load_offices(path: Path = DATA_DIR / "offices.csv") -> dict[str, dict[str, str]]:
    """Return {normalized_office_name: row} from a UTF-8 CSV (BOM supported)."""
    with path.open(encoding="utf-8-sig", newline="") as file:
        return {normalize(row["name"]): row for row in csv.DictReader(file)}


def contains_phrase(text: str, phrase: str) -> bool:
    """Match complete words so the short alias 'it' does not match 'visit'."""
    return f" {normalize(phrase)} " in f" {text} "


def reply(message: str, offices: dict[str, dict[str, str]] | None = None) -> str:
    """Answer greetings, help, office lists and office lookup questions."""
    text = normalize(message)
    if not text:
        return "Please type a question."
    if text in GREETINGS:
        return "Hello! Ask me where an office is, or when it opens."
    if text in HELP_COMMANDS:
        return HELP_TEXT
    if offices is None:
        try:
            offices = load_offices()
        except FileNotFoundError:
            return "Office data is missing. Add data/offices.csv to the repository."
    if text in LIST_COMMANDS:
        if not offices:
            return "No offices are available in the data yet."
        lines = ["Available offices:"]
        lines.extend(f"- {row['name']}" for row in offices.values())
        return "\n".join(lines)
    for name, row in offices.items():
        canonical = normalize(name)
        names = (canonical, normalize(row["name"]), *OFFICE_ALIASES.get(canonical, ()))
        if any(contains_phrase(text, candidate) for candidate in names):
            return f"{row['name']}: room {row['room']}, open {row['hours']}."
    # Full names and aliases take priority. Partial names must identify one office.
    generic_words = {"office", "offices", "department", "center", "centre", "unit"}
    matches = []
    for row in offices.values():
        words = normalize(row["name"]).split()
        if any(
            len(word) > 3 and word not in generic_words and contains_phrase(text, word)
            for word in words
        ):
            matches.append(row)
    if len(matches) == 1:
        row = matches[0]
        return f"{row['name']}: room {row['room']}, open {row['hours']}."
    if matches:
        names = ", ".join(row["name"] for row in matches)
        return f"Please specify an office: {names}."
    return "I don't know that yet. Type 'help' for examples or 'list offices' for office names."
