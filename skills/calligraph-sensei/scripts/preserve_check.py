#!/usr/bin/env python3
"""Compare an original and an edit for lost or changed facts. Read-only.

Exit code 0 means no protected item changed, 1 means at least one did. It checks
numbers, dates, names, citations, links, quotations, code, headings and negation.
It cannot judge meaning, so a human should still read the edit.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

sys.dont_write_bytecode = True  # leave the installed skill folder untouched
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _mdtext import mask, read_document, utf8_output  # noqa: E402

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[`~]*[ \t]*$", re.M | re.S)
INLINE_CODE = re.compile(r"(?<!`)`[^`\n]+`(?!`)")
URL = re.compile(r"https?://[^\s<>)\]]+")
CITATION = re.compile(r"\[(?:CITE|UNVERIFIED)[^\]]*\]|\[\^[^\]]+\]|\[\d+(?:\s*[,–-]\s*\d+)*\]|\(\s*[A-Z][\w'’-]+(?:\s+(?:et al\.?|and|&)\s*[\w'’-]*)?,?\s+\d{4}[a-z]?(?:,\s*pp?\.\s*\d+[-–\d]*)?\s*\)|\b10\.\d{4,9}/[^\s\"'<>\])]+")
NUMBER = re.compile(r"(?<![\w.])[$€£¥]?\d[\d,]*(?:\.\d+)?(?:st|nd|rd|th)?%?")
QUOTE = re.compile(r"“([^”\n]{12,})”|(?<![\w])\"([^\"\n]{12,})\"")
HEADING = re.compile(r"^ {0,3}#{1,6}\s+(.+?)\s*#*$", re.M)
NAME = re.compile(r"(?<![.!?:]\s)(?<!^)(?<!\n)\b[A-Z][\w'’-]+(?:\s+(?:of\s+|de\s+|van\s+|von\s+)?[A-Z][\w'’-]+)*")
NEGATION = re.compile(r"\b(?:not|no|never|none|neither|nor|without|cannot|\w+n['’]t)\b", re.I)
HEDGE = re.compile(r"\b(?:may|might|could|perhaps|possibly|probably|likely|suggests?|appears?|seems?|roughly|about|approximately|nearly|almost|around|estimated)\b", re.I)
COMMON_START = {"The", "A", "An", "This", "That", "These", "Those", "It", "He", "She", "They", "We", "I", "In", "On", "At", "But", "And", "Or", "If", "When", "While", "As", "For", "To", "By", "With", "From"}


def _multiset(items) -> Counter:
    return Counter(" ".join(str(item).split()) for item in items)


def _numbers(text: str) -> Counter:
    return Counter(n.replace(",", "") for n in NUMBER.findall(mask(text)))


def _names(text: str) -> Counter:
    found = Counter()
    for m in NAME.finditer(mask(text)):
        name = " ".join(m.group().split())
        if name not in COMMON_START:
            found[name] += 1
    return found


def _quotes(text: str) -> Counter:
    return _multiset(a or b for a, b in QUOTE.findall(mask(text)))


def extract(text: str) -> Dict[str, Counter]:
    return {
        "code_block": _multiset(m.group() for m in FENCE.finditer(text)),
        "inline_code": _multiset(INLINE_CODE.findall(FENCE.sub("", text))),
        "url": _multiset(URL.findall(text)),
        "citation": _multiset(CITATION.findall(FENCE.sub("", text))),
        "number": _numbers(text),
        "quotation": _quotes(text),
        "heading": _multiset(HEADING.findall(FENCE.sub("", text))),
    }


def compare(original: str, edited: str) -> Dict:
    before, after = extract(original), extract(edited)
    changes: List[Dict] = []
    for kind in before:
        for item, count in (before[kind] - after[kind]).items():
            changes.append({"kind": kind, "change": "lost", "item": item[:120], "count": count})
        for item, count in (after[kind] - before[kind]).items():
            changes.append({"kind": kind, "change": "added", "item": item[:120], "count": count})
    review: List[Dict] = []
    names_before, names_after = set(_names(original)), set(_names(edited))
    joined_after = " ".join(names_after)
    joined_before = " ".join(names_before)
    for name in sorted(names_before - names_after):
        if name not in joined_after:
            review.append({"kind": "name", "change": "lost", "item": name})
    for name in sorted(names_after - names_before):
        if name not in joined_before:
            review.append({"kind": "name", "change": "added", "item": name})
    for label, pattern in (("negation", NEGATION), ("hedge", HEDGE)):
        a, b = len(pattern.findall(mask(original))), len(pattern.findall(mask(edited)))
        if a != b:
            review.append({"kind": label, "change": "count", "item": f"{a} before, {b} after"})
    return {"preserved": not changes, "changes": changes, "review": review}


def render(result: Dict) -> str:
    lines = ["# Preservation check", "", "All protected items match." if result["preserved"] else f"**{len(result['changes'])} protected item(s) changed.** Restore them or confirm with the author.", ""]
    if result["changes"]:
        lines += ["| Type | Change | Item |", "|---|---|---|"]
        lines += [f"| {c['kind']} | {c['change']} | {c['item'].replace('|', chr(92) + '|')} |" for c in result["changes"]]
        lines.append("")
    if result["review"]:
        lines += ["Worth a human look (these can change harmlessly):", ""]
        lines += [f"- {r['kind']} {r['change']}: {r['item']}" for r in result["review"]]
    return "\n".join(lines) + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    utf8_output()
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("original", type=Path)
    parser.add_argument("edited", type=Path)
    parser.add_argument("--format", choices=["md", "json"], default="md")
    args = parser.parse_args(argv)
    result = compare(read_document(args.original), read_document(args.edited))
    sys.stdout.write(json.dumps(result, indent=2, ensure_ascii=False) + "\n" if args.format == "json" else render(result))
    return 0 if result["preserved"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
