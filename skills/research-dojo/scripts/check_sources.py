#!/usr/bin/env python3
"""Check DOIs, ISBNs, ISSNs, arXiv IDs and URLs. Read-only.

Offline by default: checks format and checksums only. With --online, it sends
identifiers and URLs (never document text) to public services. A found record
proves the source exists. It does not prove the source supports the claim.
"""
from __future__ import annotations

import argparse
import datetime as dt
import ipaddress
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

sys.dont_write_bytecode = True  # leave the installed skill folder untouched
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _mdtext import LineIndex, read_document, utf8_output  # noqa: E402

USER_AGENT = "research-dojo-source-check/2.0"
TIMEOUT = 15
DOI = re.compile(r"\b10\.\d{4,9}/[^\s\"'<>\]]+", re.I)
ISBN = re.compile(r"\bISBN(?:-1[03])?:?\s*([0-9Xx][0-9Xx\s-]{8,20}[0-9Xx])", re.I)
ISSN = re.compile(r"\bISSN:?\s*(\d{4}-?\d{3}[\dXx])\b", re.I)
ARXIV = re.compile(r"\barXiv:\s*(\d{4}\.\d{4,5}(?:v\d+)?|[a-z-]+(?:\.[A-Z]{2})?/\d{7}(?:v\d+)?)", re.I)
ARXIV_URL = re.compile(r"\barxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5}(?:v\d+)?)", re.I)
URL = re.compile(r"\bhttps?://[^\s<>\"'\])]+", re.I)
TRAILING = ".,;:!?)]}*_"

# Status words. None of them means a claim is true.
FORMAT_OK = "format_ok"
FORMAT_INVALID = "format_invalid"
NOT_CHECKED = "not_checked"
FOUND = "source_found"
MISMATCH = "metadata_mismatch"
NOT_FOUND = "not_found"
UNREACHABLE = "unreachable"
RETRACTED = "retracted"
BLOCKED = "blocked"

Fetcher = Callable[[str], Tuple[int, str]]


def isbn_valid(value: str) -> bool:
    digits = re.sub(r"[\s-]", "", value).upper()
    if len(digits) == 10 and re.fullmatch(r"\d{9}[\dX]", digits):
        total = sum((10 - i) * (10 if c == "X" else int(c)) for i, c in enumerate(digits))
        return total % 11 == 0
    if len(digits) == 13 and digits.isdigit() and digits[:3] in ("978", "979"):
        return sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(digits)) % 10 == 0
    return False


def issn_valid(value: str) -> bool:
    digits = value.replace("-", "").upper()
    if not re.fullmatch(r"\d{7}[\dX]", digits):
        return False
    total = sum((8 - i) * int(c) for i, c in enumerate(digits[:7]))
    check = (11 - total % 11) % 11
    return ("X" if check == 10 else str(check)) == digits[7]


def arxiv_valid(value: str, today: Optional[dt.date] = None) -> bool:
    today = today or dt.date.today()
    match = re.match(r"(\d{2})(\d{2})\.(\d{4,5})", value)
    if not match:
        return bool(re.match(r"[a-z-]+(?:\.[A-Z]{2})?/\d{7}", value))
    year, month = 2000 + int(match[1]), int(match[2])
    if not 1 <= month <= 12 or year < 2007 or (year, month) > (today.year, today.month):
        return False
    return len(match[3]) == (5 if year >= 2015 else 4)


def _clean(value: str) -> str:
    value = value.rstrip(TRAILING)
    while value.endswith(")") and value.count("(") < value.count(")"):
        value = value[:-1]
    return value


def extract(text: str) -> List[Dict]:
    index = LineIndex(text)
    lines = text.split("\n")
    items: List[Dict] = []
    seen = set()

    def add(kind: str, value: str, offset: int) -> None:
        key = (kind, value.lower())
        if key in seen:
            return
        seen.add(key)
        line = index.line(offset)
        items.append({"kind": kind, "value": value, "line": line, "context": lines[line - 1].strip()[:400]})

    doi_spans = []
    for m in DOI.finditer(text):
        value = _clean(m.group())
        doi_spans.append((m.start(), m.end()))
        add("doi", value, m.start())
    for m in ISBN.finditer(text):
        add("isbn", re.sub(r"[\s-]", "", m[1]).upper(), m.start())
    for m in ISSN.finditer(text):
        add("issn", m[1].upper(), m.start())
    for pattern in (ARXIV, ARXIV_URL):
        for m in pattern.finditer(text):
            add("arxiv", re.sub(r"v\d+$", "", m[1]), m.start())
    for m in URL.finditer(text):
        value = _clean(m.group())
        host = urllib.parse.urlsplit(value).netloc.lower()
        if host.endswith("doi.org") and any(a <= m.end() and m.start() <= b for a, b in doi_spans):
            continue
        if host.endswith("arxiv.org") and ARXIV_URL.search(value):
            continue
        add("url", value, m.start())
    return sorted(items, key=lambda item: item["line"])


def _public_host(host: Optional[str]) -> bool:
    if not host:
        return False
    try:
        infos = socket.getaddrinfo(host, None)
    except OSError:
        return True  # let the request fail and report as unreachable
    for info in infos:
        address = ipaddress.ip_address(info[4][0].split("%")[0])
        if not address.is_global:
            return False
    return True


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: N802
        parts = urllib.parse.urlsplit(newurl)
        if parts.scheme not in ("http", "https") or not _public_host(parts.hostname):
            raise urllib.error.URLError("redirect to a non-public address blocked")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url: str) -> Tuple[int, str]:
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https") or not _public_host(parts.hostname):
        return -1, ""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json, application/atom+xml, text/html;q=0.8, */*;q=0.5"})
    opener = urllib.request.build_opener(_SafeRedirect)
    code = 0
    for attempt in range(3):  # retry a brief outage or rate limit
        if attempt:
            time.sleep(1.5 * attempt)
        try:
            with opener.open(request, timeout=TIMEOUT) as response:
                return response.status, response.read(2_000_000).decode("utf-8", "replace")
        except urllib.error.HTTPError as error:
            code = error.code
            if code not in (429, 502, 503, 504):
                return code, ""
        except (urllib.error.URLError, OSError, ValueError):
            code = 0
    return code, ""


def _names(context: str) -> set:
    return {w.lower() for w in re.findall(r"[^\W\d_]{2,}", context)}


def _doi_online(item: Dict, fetcher: Fetcher) -> None:
    query = ""
    mail = os.environ.get("CROSSREF_MAILTO", "").strip()
    if mail:
        query = "?" + urllib.parse.urlencode({"mailto": mail})
    code, body = fetcher("https://api.crossref.org/works/" + urllib.parse.quote(item["value"], safe="/") + query)
    if code == 404:
        code, _ = fetcher("https://doi.org/api/handles/" + urllib.parse.quote(item["value"], safe="/"))
        if code == 200:
            item.update(status=FOUND, detail="The DOI resolves, but Crossref has no metadata. Compare the title by hand.")
        elif code == 404:
            item.update(status=NOT_FOUND, detail="Neither Crossref nor doi.org knows this DOI.")
        else:
            item.update(status=UNREACHABLE, detail="doi.org could not be reached.")
        return
    if code != 200:
        item.update(status=UNREACHABLE, detail=f"Crossref answered {code or 'nothing'}.")
        return
    work = json.loads(body)["message"]
    title = (work.get("title") or [""])[0]
    parts = (work.get("issued") or {}).get("date-parts") or [[None]]
    year = parts[0][0]
    authors = [a.get("family", "") for a in work.get("author", []) if a.get("family")]
    item["record"] = {"title": title, "year": year, "authors": authors[:5], "venue": (work.get("container-title") or [""])[0]}
    updates = [u for u in work.get("updated-by", []) if str(u.get("type", "")).lower() in ("retraction", "withdrawal", "removal")]
    if updates:
        item.update(status=RETRACTED, detail=f"Marked {updates[0]['type']} (notice {updates[0].get('DOI', 'unknown')}, via {updates[0].get('source', 'Crossref')}).")
        return
    item.update(_compare(item["context"], item["value"], title, year, authors))


def _compare(context: str, identifier: str, title: str, year, authors: List[str]) -> Dict:
    identifiers = sum(len(p.findall(context)) for p in (DOI, ISBN, ISSN, ARXIV))
    if identifiers > 1:
        return {"status": FOUND, "detail": "A record exists. This line has several identifiers, so compare the citation by hand."}
    stripped = URL.sub(" ", context.replace(identifier, " "))
    problems = []
    years = {int(y) for y in re.findall(r"(?<![\d./-])(1[5-9]\d{2}|20\d{2})(?![\d-])", stripped)}
    if years and year and not any(abs(y - int(year)) <= 1 for y in years):
        problems.append(f"the record's year is {year}, the text says {sorted(years)}")
    words = _names(stripped)
    title_words = {w for w in _names(title) if len(w) > 3}
    has_reference_text = len(stripped.split()) >= 6
    if has_reference_text and title_words:
        overlap = len(title_words & words) / len(title_words)
        surnames = {w for a in authors for w in _names(a)}
        if overlap < 0.3 and not surnames & words:
            problems.append(f"neither the title nor an author matches the record ('{title[:70]}')")
    if problems:
        return {"status": MISMATCH, "detail": "; ".join(problems) + "."}
    return {"status": FOUND, "detail": "A record exists. Read it to confirm that it supports the claim."}


def _arxiv_online(item: Dict, fetcher: Fetcher) -> None:
    code, body = fetcher("https://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(item["value"], safe="/"))
    if code != 200:
        item.update(status=UNREACHABLE, detail=f"arXiv answered {code or 'nothing'}.")
        return
    ns = {"a": "http://www.w3.org/2005/Atom"}
    try:
        entry = ET.fromstring(body).find("a:entry", ns)
    except ET.ParseError:
        item.update(status=UNREACHABLE, detail="arXiv returned an unreadable answer.")
        return
    title = entry.findtext("a:title", "", ns).strip() if entry is not None else ""
    if not title or title.lower() == "error":
        item.update(status=NOT_FOUND, detail="arXiv has no paper with this ID.")
        return
    published = entry.findtext("a:published", "", ns)[:4]
    authors = [a.findtext("a:name", "", ns).split()[-1] for a in entry.findall("a:author", ns)]
    item["record"] = {"title": " ".join(title.split()), "year": int(published) if published else None, "authors": authors[:5]}
    item.update(_compare(item["context"], item["value"], title, item["record"]["year"], authors))


def _isbn_online(item: Dict, fetcher: Fetcher) -> None:
    code, body = fetcher(f"https://openlibrary.org/isbn/{item['value']}.json")
    if code == 404:
        item.update(status=NOT_FOUND, detail="Open Library has no record. Its coverage is partial, so check another catalog.")
    elif code != 200:
        item.update(status=UNREACHABLE, detail=f"Open Library answered {code or 'nothing'}.")
    else:
        data = json.loads(body)
        item["record"] = {"title": data.get("title", ""), "publish_date": data.get("publish_date", "")}
        item.update(status=FOUND, detail="A record exists. Compare its title and edition with the citation.")


def _url_online(item: Dict, fetcher: Fetcher) -> None:
    code, _ = fetcher(item["value"])
    if code == -1:
        item.update(status=BLOCKED, detail="Skipped: not a public web address.")
    elif code in (404, 410):
        item.update(status=NOT_FOUND, detail=f"The page answered {code}. Look for an archived copy.")
    elif 200 <= code < 400:
        item.update(status=FOUND, detail="The page loads. Read it to confirm that it supports the claim.")
    else:
        item.update(status=UNREACHABLE, detail=f"The site answered {code or 'nothing'}. Many sites refuse scripts, so check by hand.")


def check(items: List[Dict], online: bool = False, fetcher: Fetcher = fetch, delay: float = 0.2) -> List[Dict]:
    validators = {"isbn": isbn_valid, "issn": issn_valid, "arxiv": arxiv_valid}
    for item in items:
        validator = validators.get(item["kind"])
        if validator and not validator(item["value"]):
            item.update(status=FORMAT_INVALID, detail=f"This is not a valid {item['kind'].upper()}. Likely a typo or an invented identifier.")
            continue
        item.update(status=FORMAT_OK if item["kind"] != "url" else NOT_CHECKED, detail="Format only. The source was not looked up.")
        if not online:
            continue
        handler = {"doi": _doi_online, "arxiv": _arxiv_online, "isbn": _isbn_online, "url": _url_online}.get(item["kind"])
        if handler:
            try:
                handler(item, fetcher)
            except (ValueError, KeyError, TypeError, AttributeError):
                item.update(status=UNREACHABLE, detail="The service returned an unexpected answer.")
            if delay:
                time.sleep(delay)
    return items


def main(argv: Optional[List[str]] = None) -> int:
    utf8_output()
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("file", type=Path)
    parser.add_argument("--online", action="store_true", help="look identifiers up in public services")
    args = parser.parse_args(argv)
    result = check(extract(read_document(args.file)), online=args.online)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
