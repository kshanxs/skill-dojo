#!/usr/bin/env python3
"""Build a fact-check ledger and report for a document. Never edits the input.

  dojo_check.py draft.md                     print a report
  dojo_check.py draft.md --out-dir reports   write draft.factcheck.md and .json
  dojo_check.py draft.md --online            also look sources up
  dojo_check.py draft.md --annotate copy.md  write a flagged copy
  dojo_check.py --validate reports/draft.factcheck.json
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

sys.dont_write_bytecode = True  # leave the installed skill folder untouched
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _mdtext import read_document, utf8_output  # noqa: E402
import check_dates  # noqa: E402
import check_sources  # noqa: E402
import extract_claims  # noqa: E402

SCHEMA = 1
REVIEW_STATUSES = {"unchecked", "verified", "contradicted", "disputed", "unverifiable"}
NEEDS_EVIDENCE = {"verified", "contradicted", "disputed"}
SOURCE_PROBLEMS = {check_sources.FORMAT_INVALID, check_sources.NOT_FOUND, check_sources.MISMATCH, check_sources.RETRACTED}


def validate(ledger: Dict, today: Optional[dt.date] = None) -> List[str]:
    """Reject any review status that is not backed by a recorded source."""
    today = today or dt.date.today()
    errors = []
    for claim in ledger.get("claims", []):
        cid = claim.get("id", "?")
        status = claim.get("status")
        if status not in REVIEW_STATUSES:
            errors.append(f"{cid}: unknown status {status!r}")
            continue
        if status not in NEEDS_EVIDENCE:
            continue
        evidence = claim.get("evidence") or []
        if not evidence:
            errors.append(f"{cid}: marked {status} with no evidence")
        for number, item in enumerate(evidence, 1):
            if not isinstance(item, dict):
                errors.append(f"{cid}: evidence {number} must be an object")
                continue
            if not str(item.get("source", "")).strip():
                errors.append(f"{cid}: evidence {number} has no source")
            if not str(item.get("locator", "")).strip() and not str(item.get("quote", "")).strip():
                errors.append(f"{cid}: evidence {number} needs a locator or a quote")
            try:
                checked = dt.date.fromisoformat(str(item.get("checked_on", "")))
                if checked > today:
                    errors.append(f"{cid}: evidence {number} is dated in the future")
            except ValueError:
                errors.append(f"{cid}: evidence {number} needs checked_on as YYYY-MM-DD")
    return errors


def merge_reviews(claims: List[Dict], previous: Optional[Dict]) -> List[Dict]:
    """Keep earlier review work for sentences that have not changed."""
    if not previous:
        return claims
    known = {c.get("hash"): c for c in previous.get("claims", [])}
    for claim in claims:
        old = known.get(claim["hash"])
        if not old:
            continue
        for field in ("status", "evidence", "note"):
            claim[field] = old.get(field, claim[field])
        if validate({"claims": [claim]}):  # a status without evidence does not count
            claim["note"] = f"Reset from {claim['status']!r}: no valid evidence recorded. {claim['note']}".strip()
            claim["status"] = "unchecked"
    return claims


def build(text: str, source: str, online: bool, as_of: dt.date, previous: Optional[Dict] = None, fetcher=check_sources.fetch) -> Dict:
    claims = merge_reviews(extract_claims.extract(text), previous)
    return {
        "schema": SCHEMA,
        "source": source,
        "checked_on": as_of.isoformat(),
        "online": online,
        "summary": {
            "claims": len(claims),
            "claim_status": dict(Counter(c["status"] for c in claims)),
        },
        "claims": claims,
        "date_findings": check_dates.check(text, as_of),
        "sources": check_sources.check(check_sources.extract(text), online=online, fetcher=fetcher),
    }


def _cell(value: str, limit: int = 110) -> str:
    value = " ".join(str(value).split()).replace("|", "\\|")
    return value if len(value) <= limit else value[: limit - 1] + "…"


def render(ledger: Dict) -> str:
    claims = ledger["claims"]
    counts = Counter(c["status"] for c in claims)
    source_counts = Counter(s["status"] for s in ledger["sources"])
    problems = [s for s in ledger["sources"] if s["status"] in SOURCE_PROBLEMS]
    lines = [
        f"# Fact-check report: {ledger['source']}",
        "",
        f"Checked on {ledger['checked_on']}. Source lookup: {'on' if ledger['online'] else 'off (format checks only)'}.",
        "",
        f"**{counts.get('verified', 0)} of {len(claims)} claims are verified.** "
        f"{counts.get('unchecked', 0)} are unchecked, {counts.get('contradicted', 0)} contradicted, "
        f"{counts.get('disputed', 0)} disputed, {counts.get('unverifiable', 0)} unverifiable.",
        "",
        "A claim counts as verified only when a person or agent has read a source and recorded it in the ledger. "
        "Automatic checks cannot verify a claim.",
        "",
        "## Date problems",
        "",
    ]
    if ledger["date_findings"]:
        lines += ["| Line | Severity | Text | Problem |", "|---:|---|---|---|"]
        lines += [f"| {f['line']} | {f['severity']} | {_cell(f['text'], 60)} | {_cell(f['message'])} |" for f in ledger["date_findings"]]
    else:
        lines.append("No internal date conflicts found. The dates were not compared with outside sources.")
    lines += ["", "## Source problems", ""]
    if problems:
        lines += ["| Line | Type | Identifier | Status | Detail |", "|---:|---|---|---|---|"]
        lines += [f"| {s['line']} | {s['kind']} | {_cell(s['value'], 50)} | **{s['status']}** | {_cell(s['detail'], 130)} |" for s in problems]
    else:
        lines.append("None found by the checks that ran.")
    if ledger["sources"]:
        lines += ["", "Source status counts: " + ", ".join(f"{k} {v}" for k, v in sorted(source_counts.items())) + "."]
    lines += ["", "## Claims to check", ""]
    order = {"high": 0, "medium": 1, "low": 2}
    if claims:
        lines += ["| ID | Line | Priority | Status | Type | Claim |", "|---|---:|---|---|---|---|"]
        for c in sorted(claims, key=lambda c: (order[c["priority"]], c["line"])):
            lines.append(f"| {c['id']} | {c['line']} | {c['priority']} | {c['status']} | {', '.join(c['types'])} | {_cell(c['text'])} |")
    else:
        lines.append("No checkable claims detected.")
    return "\n".join(lines) + "\n"


def annotate(text: str, ledger: Dict) -> str:
    """Return a copy with visible flags at the end of affected lines."""
    flags: Dict[int, List[str]] = {}
    for c in ledger["claims"]:
        if c["status"] in ("unchecked", "unverifiable") and c["priority"] == "high":
            flags.setdefault(c["line"], []).append(f"[UNVERIFIED {c['id']}]")
        elif c["status"] in ("contradicted", "disputed"):
            flags.setdefault(c["line"], []).append(f"[{c['status'].upper()} {c['id']}]")
    for f in ledger["date_findings"]:
        if f["severity"] in ("error", "warning"):
            flags.setdefault(f["line"], []).append(f"[DATE: {f['message']}]")
    for s in ledger["sources"]:
        if s["status"] in SOURCE_PROBLEMS:
            flags.setdefault(s["line"], []).append(f"[SOURCE {s['status']}: {s['value']}]")
    lines = text.split("\n")
    for number, items in flags.items():
        line = lines[number - 1]
        flag = " ".join(items)
        stripped = line.rstrip()
        if stripped.endswith("|"):
            lines[number - 1] = stripped[:-1].rstrip() + " " + flag + " |"
        else:
            lines[number - 1] = stripped + " " + flag
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    utf8_output()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", type=Path, nargs="?")
    parser.add_argument("--online", action="store_true", help="look sources up in public services")
    parser.add_argument("--as-of", type=dt.date.fromisoformat, help="treat this ISO date as today")
    parser.add_argument("--out-dir", type=Path, help="write <name>.factcheck.md and .json here")
    parser.add_argument("--annotate", type=Path, metavar="COPY", help="write a flagged copy (never the input file)")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="stdout format")
    parser.add_argument("--validate", type=Path, metavar="LEDGER", help="check that review statuses have evidence")
    args = parser.parse_args(argv)

    if args.validate:
        errors = validate(json.loads(read_document(args.validate)))
        for error in errors:
            print(error, file=sys.stderr)
        print("Ledger is valid." if not errors else f"{len(errors)} problem(s) found.", file=sys.stderr)
        return 1 if errors else 0
    if not args.file:
        parser.error("a file is required unless --validate is used")
    if not args.file.is_file():
        parser.error(f"no such file: {args.file}")
    if args.annotate and args.annotate.resolve() == args.file.resolve():
        parser.error("--annotate must not point at the input file")
    if args.annotate and args.annotate.exists():
        parser.error(f"{args.annotate} already exists; choose a new path")

    text = read_document(args.file)
    as_of = args.as_of or dt.date.today()
    previous = None
    json_path = md_path = None
    if args.out_dir:
        json_path = args.out_dir / f"{args.file.stem}.factcheck.json"
        md_path = args.out_dir / f"{args.file.stem}.factcheck.md"
        if args.file.resolve() in (json_path.resolve(), md_path.resolve()):
            parser.error("report path would overwrite the input file")
        if json_path.exists():
            try:
                previous = json.loads(read_document(json_path))
            except ValueError:
                parser.error(f"{json_path} is not valid JSON. Fix or move it so that review work is not overwritten.")
    ledger = build(text, args.file.name, args.online, as_of, previous)
    report = render(ledger)
    if args.out_dir:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        md_path.write_text(report, encoding="utf-8")
        print(f"Wrote {md_path} and {json_path}", file=sys.stderr)
    else:
        sys.stdout.write(report if args.format == "md" else json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")
    if args.annotate:
        args.annotate.parent.mkdir(parents=True, exist_ok=True)
        args.annotate.write_text(annotate(text, ledger), encoding="utf-8")
        print(f"Wrote {args.annotate}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
