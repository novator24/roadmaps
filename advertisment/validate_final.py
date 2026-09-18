#!/usr/bin/env python3
"""Acceptance checks for advertisment/FINAL.docx."""

from pathlib import Path
from zipfile import BadZipFile, ZipFile
import re
import sys


ROOT = Path(__file__).resolve().parent
DRAFT = ROOT / "DRAFT.docx"
FINAL = ROOT / "FINAL.docx"


def inspect_docx(path: Path) -> tuple[int, str]:
    if not path.exists():
        raise AssertionError(f"Missing file: {path}")
    try:
        with ZipFile(path) as archive:
            bad_member = archive.testzip()
            if bad_member:
                raise AssertionError(f"Corrupt ZIP member in {path.name}: {bad_member}")
            xml = archive.read("word/document.xml").decode("utf-8")
    except (BadZipFile, KeyError, UnicodeDecodeError) as exc:
        raise AssertionError(f"Invalid DOCX {path.name}: {exc}") from exc

    pages = len(re.findall(r'w:type="page"', xml)) + 1
    text = " ".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml, flags=re.S))
    text = (
        text.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
    )
    return pages, text


def main() -> int:
    draft_pages, draft_text = inspect_docx(DRAFT)
    final_pages, final_text = inspect_docx(FINAL)

    assert draft_pages == final_pages, (
        f"Page count differs: DRAFT={draft_pages}, FINAL={final_pages}"
    )

    required = [
        "Armenia",
        "5 FTE",
        "UAE",
        "30 FTE",
        "125 FTE",
        "Hong Kong",
        "Total 126",
        "NPS",
        "Mitigation",
        "Response",
        "бюджет",
        "Q1:",
        "Q2:",
        "Q3:",
        "Q4:",
        "Security by design",
    ]
    missing = [phrase for phrase in required if phrase.casefold() not in final_text.casefold()]
    assert not missing, f"Missing required phrases: {', '.join(missing)}"

    forbidden = ["TODO", "TBD", "XXX", "Lorem ipsum"]
    new_placeholders = [
        phrase
        for phrase in forbidden
        if phrase.casefold() in final_text.casefold()
        and phrase.casefold() not in draft_text.casefold()
    ]
    assert not new_placeholders, f"New placeholders found: {', '.join(new_placeholders)}"

    print(f"DRAFT: {draft_pages}")
    print(f"FINAL: {final_pages}")
    print("DOCX: VALID")
    print("REQUIRED CONTENT: PASS")
    print("PLACEHOLDERS: PASS")
    print("STATUS: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"STATUS: FAIL — {error}", file=sys.stderr)
        raise SystemExit(1)