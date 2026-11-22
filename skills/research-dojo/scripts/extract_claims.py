#!/usr/bin/env python3
"""List the checkable claims in a Markdown or text file. Read-only.

Every claim starts as `unchecked`. This tool finds what needs checking. It never
decides whether a claim is true.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

sys.dont_write_bytecode = True  # leave the installed skill folder untouched
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _mdtext import LineIndex, mask, read_document, sentences, utf8_output  # noqa: E402

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
SIGNALS = {
    "date": re.compile(
        rf"\b(?:{MONTHS})\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{3,4}}\b|\b\d{{1,2}}\s+(?:{MONTHS})\s+\d{{3,4}}\b"
        r"|\b(?:in|by|since|until|from|during|around|circa|c\.)\s+(?:1[0-9]{3}|20[0-9]{2})\b"
        r"|\b(?:1[0-9]{3}|20[0-9]{2})\s*[-–—]\s*(?:1[0-9]{3}|20[0-9]{2}|\d{2})\b"
        r"|\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}(?:st|nd|rd|th)[- ]century\b"
    ),
    "number": re.compile(
        r"(?<![\w.])(?:[$€£¥]\s?\d[\d,.]*(?:\s?(?:thousand|million|billion|trillion))?"
        r"|\d[\d,.]*\s?(?:%|percent\b|per cent\b)"
        r"|\d[\d,.]*\s(?:thousand|million|billion|trillion)\b"
        r"|\d{1,3}(?:,\d{3})+\b"
        r"|\d+(?:\.\d+)?\s?(?:km|kg|mph|miles|meters|metres|tons|tonnes|people|deaths|soldiers|years old)\b)",
        re.I,
    ),
    "attribution": re.compile(
        r"(?i:\baccording to\b|\b(?:studies|research|experts|scientists|historians|researchers|reports?)\s+"
        r"(?:show|shows|found|find|suggest|suggests|say|says|claim|claims|argue|argues|indicate|indicates|confirm|confirms)\b)"
        r"|\b[A-Z][a-z]+\s+(?:said|wrote|argued|claimed|stated|observed|reported|declared|noted)\b"
    ),
    "superlative": re.compile(
        r"\b(?:the\s+)?(?:first|last|only|largest|smallest|oldest|youngest|biggest|highest|lowest|fastest|earliest|"
        r"longest|shortest|most\s+\w+)\s+(?:\w+\s+)?(?:ever|in\s+(?:the\s+)?(?:world|history|country|nation)|to\s+\w+)\b",
        re.I,
    ),
    "causal": re.compile(
        r"\b(?:caused|causes|proved|proves|led directly to|resulted in|was responsible for|is responsible for|"
        r"invented|discovered|founded)\b",
        re.I,
    ),
}
QUOTE = re.compile(r"“([^”\n]{20,})”|\"([^\"\n]{20,})\"")
CITATION = re.compile(
    r"\(\s*[A-Z][\w'’-]+(?:\s+(?:et al\.?|and|&)\s*[\w'’-]*)?,?\s+\d{4}[a-z]?(?:,\s*pp?\.\s*\d+[-–\d]*)?\s*\)"
    r"|\[\d+(?:[,-–]\s*\d+)*\]|\[\^[^\]]+\]|\bdoi:|\bdoi\.org/",
    re.I,
)
WEIGHTS = {"quote": 3, "number": 3, "date": 2, "attribution": 2, "superlative": 2, "causal": 1}


def fingerprint(sentence: str) -> str:
    """Stable id for a sentence, so review notes survive edits elsewhere in the file."""
    normal = re.sub(r"\s+", " ", sentence).strip().lower()
    return hashlib.sha256(normal.encode("utf-8")).hexdigest()[:12]


def extract(text: str) -> List[Dict]:
    masked = mask(text)
    index = LineIndex(text)
    claims: List[Dict] = []
    for start, end in sentences(masked):
        prose = masked[start:end]
        if prose.lstrip().startswith("#"):
            continue
        types = [name for name, pattern in SIGNALS.items() if pattern.search(prose)]
        if QUOTE.search(prose):
            types.insert(0, "quote")
        if not types:
            continue
        original = re.sub(r"\s+", " ", text[start:end]).strip()
        has_citation = bool(CITATION.search(text[start:end]))
        score = sum(WEIGHTS[name] for name in types)
        priority = "high" if score >= 4 and not has_citation else "medium" if score >= 2 else "low"
        claims.append(
            {
                "id": f"C{len(claims) + 1:03d}",
                "hash": fingerprint(original),
                "line": index.line(start),
                "text": original,
                "types": types,
                "has_citation": has_citation,
                "priority": priority,
                "status": "unchecked",
                "evidence": [],
                "note": "",
            }
        )
    return claims


def main(argv: List[str] | None = None) -> int:
    utf8_output()
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("file", type=Path)
    parser.add_argument("--priority", choices=["high", "medium", "low"], help="only this priority")
    args = parser.parse_args(argv)
    claims = extract(read_document(args.file))
    if args.priority:
        claims = [claim for claim in claims if claim["priority"] == args.priority]
    json.dump(claims, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
