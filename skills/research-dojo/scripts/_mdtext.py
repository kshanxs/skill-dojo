"""Markdown-aware text helpers. Standard library only.

`mask` blanks out everything that is not the author's prose while keeping every
character offset and newline, so a finding in masked text maps to the same line
in the original file.
"""
from __future__ import annotations

import bisect
import re
import sys
from typing import Iterator, List, Tuple

_FRONTMATTER = re.compile(r"\A---[ \t]*\n.*?\n(?:---|\.\.\.)[ \t]*(?:\n|\Z)", re.S)
_FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_PATTERNS = [
    re.compile(r"<!--.*?-->", re.S),
    re.compile(r"(?<!`)(`+)(?!`).+?(?<!`)\1(?!`)", re.S),
    re.compile(r"!\[[^\]]*\]\([^)]*\)"),
    re.compile(r"^ {0,3}\[[^\]]+\]:\s+\S.*$", re.M),
    re.compile(r"</?[A-Za-z][^<>]*>"),
    re.compile(r"\bhttps?://[^\s<>)\]]+"),
    re.compile(r"\bwww\.[^\s<>)\]]+"),
    re.compile(r"\[(?:CITE|UNVERIFIED|TODO|TK)\b[^\]]*\]"),
]
_LINK_TARGET = re.compile(r"(?<=\])\([^)\s]*(?:\s+\"[^\"]*\")?\)")
_QUOTE_LINE = re.compile(r"^ {0,3}>.*$", re.M)
_INLINE_QUOTE = re.compile(r"“[^”\n]*”|\"[^\"\n]*\"")

ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "prof", "st", "mt", "sr", "jr", "rev", "gen", "col",
    "capt", "lt", "sgt", "gov", "sen", "rep", "hon", "vs", "etc", "e.g", "i.e",
    "cf", "al", "fig", "figs", "no", "nos", "vol", "vols", "ed", "eds", "pp", "p",
    "ch", "sec", "approx", "ca", "c", "inc", "ltd", "co", "corp", "dept", "univ",
    "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov",
    "dec", "u.s", "u.k", "a.m", "p.m", "b.c", "a.d", "ph.d",
}


def read_document(path) -> str:
    """Read UTF-8 text, accepting a byte-order mark and any line ending."""
    try:
        with open(path, encoding="utf-8-sig", newline=None) as handle:
            return handle.read()
    except UnicodeDecodeError:
        raise SystemExit(f"error: {path} is not UTF-8 text. Convert it to UTF-8 and try again.")
    except OSError as error:
        raise SystemExit(f"error: cannot read {path}: {error.strerror}")


def utf8_output() -> None:
    """Keep reports printable on consoles with a legacy encoding."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def _blank(chars: List[str], start: int, end: int) -> None:
    for index in range(start, end):
        if chars[index] != "\n":
            chars[index] = " "


def mask(text: str, quotes: bool = False) -> str:
    """Return `text` with non-prose blanked. `quotes=True` also blanks quotations."""
    chars = list(text)
    match = _FRONTMATTER.match(text)
    if match:
        _blank(chars, 0, match.end())

    # Plain-text files often indent every paragraph. That is prose, not Markdown code.
    nonblank = [line for line in text.splitlines() if line.strip()]
    indented = sum(line.startswith(("    ", "\t")) for line in nonblank)
    indented_is_code = indented * 2 < len(nonblank)

    offset = 0
    fence = None
    fence_start = 0
    previous_blank = True
    for line in text.splitlines(keepends=True):
        end = offset + len(line)
        if offset >= (match.end() if match else 0):
            opener = _FENCE_OPEN.match(line)
            if fence:
                stripped = line.strip()
                if stripped and set(stripped) == {fence[0]} and len(stripped) >= len(fence):
                    _blank(chars, fence_start, end)
                    fence = None
            elif opener:
                fence = opener.group(1)
                fence_start = offset
            elif indented_is_code and previous_blank and (line.startswith("    ") or line.startswith("\t")) and line.strip():
                _blank(chars, offset, end)
                offset = end
                continue
        previous_blank = not line.strip()
        offset = end
    if fence:
        _blank(chars, fence_start, len(chars))

    current = "".join(chars)
    for pattern in _PATTERNS:
        for found in pattern.finditer(current):
            _blank(chars, found.start(), found.end())
        current = "".join(chars)
    for found in _LINK_TARGET.finditer(current):
        _blank(chars, found.start(), found.end())
    current = "".join(chars)
    if quotes:
        for pattern in (_QUOTE_LINE, _INLINE_QUOTE):
            for found in pattern.finditer(current):
                _blank(chars, found.start(), found.end())
            current = "".join(chars)
    return current


class LineIndex:
    """Map character offsets to 1-based line numbers."""

    def __init__(self, text: str) -> None:
        self.starts = [0] + [m.end() for m in re.finditer(r"\n", text)]

    def line(self, offset: int) -> int:
        return bisect.bisect_right(self.starts, offset)


def paragraphs(masked: str) -> Iterator[Tuple[int, int]]:
    """Yield (start, end) spans of blocks separated by blank lines."""
    for match in re.finditer(r"(?:[^\n]*\S[^\n]*(?:\n|\Z))+", masked):
        yield match.start(), match.end()


_BOUNDARY = re.compile(r"[.!?…]+[\"'”’)\]]*(?=\s+|\Z)")


def sentences(masked: str) -> Iterator[Tuple[int, int]]:
    """Yield (start, end) sentence spans. Headings, list items and rows stand alone."""
    for block_start, block_end in paragraphs(masked):
        for line_match in _block_units(masked, block_start, block_end):
            yield from _split(masked, *line_match)


def _block_units(masked: str, start: int, end: int) -> Iterator[Tuple[int, int]]:
    unit_start = None
    offset = start
    for line in masked[start:end].splitlines(keepends=True):
        stripped = line.lstrip()
        structural = bool(re.match(r"(#{1,6}\s|[-*+]\s|\d+[.)]\s|\|)", stripped))
        if structural:
            if unit_start is not None:
                yield unit_start, offset
                unit_start = None
            yield offset, offset + len(line)
        elif unit_start is None:
            unit_start = offset
        offset += len(line)
    if unit_start is not None:
        yield unit_start, end


def _split(masked: str, start: int, end: int) -> Iterator[Tuple[int, int]]:
    cursor = start
    for match in _BOUNDARY.finditer(masked, start, end):
        before = masked[cursor:match.start()].rsplit(None, 1)
        token = before[-1].lower().lstrip("([\"'“‘") if before else ""
        following = masked[match.end():end].lstrip()
        if match.group().startswith(".") and len(match.group()) == 1:
            if token in ABBREVIATIONS or re.fullmatch(r"[a-z]", token):
                continue
            if re.fullmatch(r"(?:[a-z]\.)+[a-z]", token):
                continue
        if following and following[0].islower():
            continue
        if masked[cursor:match.end()].strip():
            yield _trim(masked, cursor, match.end())
        cursor = match.end()
    if masked[cursor:end].strip():
        yield _trim(masked, cursor, end)


def _trim(masked: str, start: int, end: int) -> Tuple[int, int]:
    while start < end and masked[start].isspace():
        start += 1
    while end > start and masked[end - 1].isspace():
        end -= 1
    return start, end
