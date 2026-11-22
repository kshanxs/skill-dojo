#!/usr/bin/env python3
"""Find dates that are impossible or inconsistent inside a document. Read-only, offline.

A clean result means the dates agree with the calendar and each other. It does
not mean they are historically correct.
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.dont_write_bytecode = True  # leave the installed skill folder untouched
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _mdtext import LineIndex, mask, paragraphs, read_document, sentences, utf8_output  # noqa: E402

MONTH_NAMES = list(calendar.month_name)[1:]
MONTH_ABBR = {name[:3].lower(): i + 1 for i, name in enumerate(MONTH_NAMES)}
MONTH = r"(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan\.?|Feb\.?|Mar\.?|Apr\.?|Jun\.?|Jul\.?|Aug\.?|Sept?\.?|Oct\.?|Nov\.?|Dec\.?)"
WEEKDAY = r"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
_MDY = re.compile(rf"(?:(?P<wd>{WEEKDAY}),?\s+)?(?:the\s+)?\b(?P<mon>{MONTH})\s+(?P<day>\d{{1,2}})(?:st|nd|rd|th)?,\s*(?P<year>\d{{4}})\b")
_DMY = re.compile(rf"(?:(?P<wd>{WEEKDAY}),?\s+)?(?:the\s+)?\b(?P<day>\d{{1,2}})(?:st|nd|rd|th)?\s+(?:of\s+)?(?P<mon>{MONTH})(?:,)?\s+(?P<year>\d{{4}})\b")
_ISO = re.compile(r"(?<![\d-])(?P<year>\d{4})-(?P<mon>\d{2})-(?P<day>\d{2})(?![\d-])")
_RANGE = re.compile(r"(?<![\d.,:/-])(?P<a>1[0-9]{3}|20[0-9]{2})\s?[-–—]\s?(?P<b>1[0-9]{3}|20[0-9]{2}|\d{2})(?![\d-])")
_LIFESPAN = re.compile(r"(?P<name>[A-Z][\w'’.-]+(?:\s+[A-Z][\w'’.-]+)*)\s*\((?:b\.\s*)?(?P<a>1[0-9]{3}|20[0-9]{2})\s?[-–—]\s?(?:d\.\s*)?(?P<b>1[0-9]{3}|20[0-9]{2})\)")
_BORN = re.compile(r"\bborn\b[^.;]{0,60}?\b(?P<y>1[0-9]{3}|20[0-9]{2})\b", re.I)
_DIED = re.compile(r"\bdied\b[^.;]{0,60}?\b(?P<y>1[0-9]{3}|20[0-9]{2})\b", re.I)
_AGE = re.compile(r"\b(?:at (?:the )?age(?: of)?|aged)\s+(?P<age>\d{1,3})\b", re.I)
_AGE_IN = re.compile(r"\b(?:at (?:the )?age(?: of)?|aged)\s+(?P<age>\d{1,3})\b[^.;]{0,30}?\bin\s+(?P<y>1[0-9]{3}|20[0-9]{2})\b|\bin\s+(?P<y2>1[0-9]{3}|20[0-9]{2})\b[^.;]{0,30}?\b(?:at (?:the )?age(?: of)?|aged)\s+(?P<age2>\d{1,3})\b", re.I)
NUMBER_WORDS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
_RELATIVE = re.compile(r"\b(?P<n>\d{1,3}|" + "|".join(NUMBER_WORDS) + r")\s+years?\s+(?P<dir>later|after|earlier|before),?\s+(?:in|by)\s+(?P<y>1[0-9]{3}|20[0-9]{2})\b", re.I)
_YEAR = re.compile(r"(?<![\d,.-])(1[0-9]{3}|20[0-9]{2})(?![\d-])")
_NUMERIC = re.compile(r"(?<![\d/])(\d{1,2})/(\d{1,2})/(\d{2,4})(?![\d/])")
_PAST = re.compile(r"\b(?:was|were|had|died|won|announced|published|signed|founded|elected|launched|released|fought|ended|began)\b", re.I)
_FUTURE_HINT = re.compile(r"\b(?:will|by|until|plans?|planned|expected|projected|forecast|scheduled|target|aims?|could|may|might|would)\b", re.I)
_SKIP_RANGE = re.compile(r"(?:\bpp?\.|\bpages?|ISBN|ISSN|doi|\btel\.?|\bphone|\bno\.)\s*$", re.I)
MAX_LIFESPAN = 122  # the longest verified human life
GREGORIAN_START = dt.date(1582, 10, 15)
GREGORIAN_EVERYWHERE = dt.date(1927, 1, 1)  # after the last national adoptions in common use


def _month(value: str) -> int:
    return int(value) if value.isdigit() else MONTH_ABBR[value[:3].lower()]


def julian_weekday(year: int, month: int, day: int) -> str:
    """Weekday of a date read in the Julian calendar."""
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    jdn = day + (153 * m + 2) // 5 + 365 * y + y // 4 - 32083
    return calendar.day_name[jdn % 7]


def _finding(rule: str, severity: str, line: int, text: str, message: str) -> Dict:
    return {"rule": rule, "severity": severity, "line": line, "text": text.strip(), "message": message}


def _check_exact(masked: str, index: LineIndex, as_of: dt.date) -> List[Dict]:
    findings: List[Dict] = []
    seen = set()
    for pattern in (_MDY, _DMY, _ISO):
        for m in pattern.finditer(masked):
            key = (m.start("day"), m.start("year"))
            if key in seen:
                continue
            seen.add(key)
            line = index.line(m.start())
            year, month, day = int(m["year"]), _month(m["mon"]), int(m["day"])
            if not 1 <= month <= 12 or year < 1:
                findings.append(_finding("impossible-date", "error", line, m.group(), "This month does not exist."))
                continue
            last = calendar.monthrange(year, month)[1]
            if day < 1 or day > last:
                extra = ""
                if month == 2 and day == 29:
                    extra = f" {year} is not a Gregorian leap year."
                findings.append(_finding("impossible-date", "error", line, m.group(), f"{MONTH_NAMES[month - 1]} has {last} days in {year}.{extra}"))
                continue
            weekday = m.groupdict().get("wd")
            if weekday:
                date = dt.date(year, month, day)
                actual = calendar.day_name[date.weekday()]
                if actual != weekday:
                    julian = julian_weekday(year, month, day)
                    if date < GREGORIAN_START:
                        if julian != weekday:
                            findings.append(_finding("weekday-mismatch", "warning", line, m.group(), f"In the Julian calendar this date was a {julian}."))
                    elif date < GREGORIAN_EVERYWHERE and julian == weekday:
                        findings.append(_finding("calendar-style", "info", line, m.group(), f"{weekday} fits the Julian (Old Style) calendar. The Gregorian weekday is {actual}. Confirm which calendar the source uses."))
                    elif date < GREGORIAN_EVERYWHERE:
                        findings.append(_finding("weekday-mismatch", "warning", line, m.group(), f"This date was a {actual} (Gregorian) or {julian} (Julian), not a {weekday}."))
                    else:
                        findings.append(_finding("weekday-mismatch", "error", line, m.group(), f"This date was a {actual}, not a {weekday}."))
    return findings


def _check_ranges(masked: str, index: LineIndex) -> List[Dict]:
    findings = []
    for m in _RANGE.finditer(masked):
        if _SKIP_RANGE.search(masked[max(0, m.start() - 12):m.start()]):
            continue
        a, raw = int(m["a"]), m["b"]
        b = int(raw) if len(raw) == 4 else a - a % 100 + int(raw)
        if len(raw) == 2 and b < a:
            continue  # may cross a century, such as 1999-00
        if b < a:
            findings.append(_finding("reversed-range", "error", index.line(m.start()), m.group(), "The range ends before it begins."))
    for m in _LIFESPAN.finditer(masked):
        a, b = int(m["a"]), int(m["b"])
        if b - a > MAX_LIFESPAN:
            findings.append(_finding("implausible-lifespan", "warning", index.line(m.start()), m.group(), f"This span is {b - a} years, longer than any verified human life. If it is not a lifespan, ignore this."))
    return findings


def _check_ages(masked: str, index: LineIndex) -> List[Dict]:
    findings = []
    for start, end in paragraphs(masked):
        block = masked[start:end]
        spans = [(int(m["a"]), int(m["b"]), m) for m in _LIFESPAN.finditer(block)]
        born = _BORN.search(block)
        died = _DIED.search(block)
        birth = spans[0][0] if len(spans) == 1 else int(born["y"]) if born and len(_BORN.findall(block)) == 1 else None
        death = spans[0][1] if len(spans) == 1 else int(died["y"]) if died and len(_DIED.findall(block)) == 1 else None
        if birth and death and death < birth:
            findings.append(_finding("death-before-birth", "error", index.line(start), block[:80], f"Birth {birth} comes after death {death}."))
            continue
        if birth is None:
            continue
        checked = set()
        for m in _AGE_IN.finditer(block):
            age, year = int(m["age"] or m["age2"]), int(m["y"] or m["y2"])
            checked.add(m.start())
            if abs((year - birth) - age) > 1:
                findings.append(_finding("age-mismatch", "warning", index.line(start + m.start()), m.group(), f"Born {birth}, so age in {year} would be about {year - birth}, not {age}."))
        if death and len(spans) <= 1:
            for sentence_match in re.finditer(r"[^.!?]*\bdied\b[^.!?]*", block):
                age_match = _AGE.search(sentence_match.group())
                if age_match and not _AGE_IN.search(sentence_match.group()):
                    age = int(age_match["age"])
                    if abs((death - birth) - age) > 1:
                        findings.append(_finding("age-mismatch", "warning", index.line(start + sentence_match.start()), age_match.group(), f"Born {birth} and died {death}, so age at death would be about {death - birth}, not {age}."))
    return findings


def _check_relative(masked: str, index: LineIndex) -> List[Dict]:
    findings = []
    for start, end in paragraphs(masked):
        block = masked[start:end]
        for m in _RELATIVE.finditer(block):
            prior = _YEAR.findall(block[:m.start()])
            if not prior:
                continue
            raw = m["n"].lower()
            n = NUMBER_WORDS[raw] if raw in NUMBER_WORDS else int(raw)
            base = int(prior[-1])
            sign = 1 if m["dir"].lower() in ("later", "after") else -1
            expected = base + sign * n
            if abs(expected - int(m["y"])) > 1:
                findings.append(_finding("relative-date", "warning", index.line(start + m.start()), m.group(), f"The nearest earlier year is {base}, which gives about {expected}, not {m['y']}. Check which event this counts from."))
    return findings


def _check_context(masked: str, index: LineIndex, as_of: dt.date) -> List[Dict]:
    findings = []
    for m in _NUMERIC.finditer(masked):
        a, b = int(m[1]), int(m[2])
        if a <= 12 and b <= 12 and a != b:
            findings.append(_finding("ambiguous-date", "info", index.line(m.start()), m.group(), "Could be month/day or day/month. Prefer a written month."))
    for start, end in sentences(masked):
        sentence = masked[start:end]
        if not _PAST.search(sentence) or _FUTURE_HINT.search(sentence):
            continue
        for y in _YEAR.finditer(sentence):
            if int(y.group()) > as_of.year:
                findings.append(_finding("future-date", "warning", index.line(start + y.start()), sentence[:100], f"Past tense with a year after {as_of.isoformat()}."))
    return findings


def check(text: str, as_of: Optional[dt.date] = None) -> List[Dict]:
    as_of = as_of or dt.date.today()
    masked = mask(text)
    index = LineIndex(text)
    findings = (
        _check_exact(masked, index, as_of)
        + _check_ranges(masked, index)
        + _check_ages(masked, index)
        + _check_relative(masked, index)
        + _check_context(masked, index, as_of)
    )
    return sorted(findings, key=lambda item: (item["line"], item["rule"]))


def main(argv: Optional[List[str]] = None) -> int:
    utf8_output()
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("file", type=Path)
    parser.add_argument("--as-of", type=dt.date.fromisoformat, help="treat this ISO date as today")
    args = parser.parse_args(argv)
    json.dump(check(read_document(args.file), args.as_of), sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
