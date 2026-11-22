#!/usr/bin/env python3
"""Measure a writer's habits and compare an edit against them. Read-only.

  voice_profile.py sample.md                  print a profile
  voice_profile.py original.md --against edit.md  show where the edit drifts

Compare an edit with its own original passage. One author's different passages
vary widely, so a gap between unrelated passages means little. The profile
describes surface habits. It does not identify an author.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.dont_write_bytecode = True  # leave the installed skill folder untouched
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _mdtext import mask, read_document, sentences, utf8_output  # noqa: E402

WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?")
FIRST = {"i", "me", "my", "mine", "we", "us", "our", "ours"}
SECOND = {"you", "your", "yours"}
FUNCTION = "the of and to a in that it is was for on with as but be at by this have from or not are his her they you".split()
MIN_WORDS = 300
TOLERANCE = {
    "mean_sentence_words": 0.25, "sentence_length_sd": 0.35, "contractions_per_1000": 0.5,
    "first_person_per_1000": 0.5, "second_person_per_1000": 0.5, "em_dashes_per_1000": 0.6,
    "semicolons_per_1000": 0.6, "colons_per_1000": 0.6, "questions_share": 0.6, "commas_per_sentence": 0.3,
}
MIN_DELTA = {
    "mean_sentence_words": 2.0, "sentence_length_sd": 2.0, "contractions_per_1000": 3.0,
    "first_person_per_1000": 4.0, "second_person_per_1000": 4.0, "em_dashes_per_1000": 1.5,
    "semicolons_per_1000": 1.5, "colons_per_1000": 1.5, "questions_share": 0.05, "commas_per_sentence": 0.3,
}


def profile(text: str) -> Dict:
    masked = mask(text)
    spans = [masked[a:b] for a, b in sentences(masked) if not masked[a:b].lstrip().startswith(("#", "|"))]
    lengths = [n for n in (len(WORD.findall(s)) for s in spans) if n]
    words = [w.lower().replace("’", "'") for w in WORD.findall(" ".join(spans))]
    total = len(words)
    if not total or not lengths:
        return {"words": 0}
    rate = lambda n: round(n * 1000 / total, 1)
    result = {
        "words": total,
        "mean_sentence_words": round(total / len(lengths), 1),
        "sentence_length_sd": round(statistics.pstdev(lengths), 1),
        "contractions_per_1000": rate(sum("'" in w and not w.endswith("'s") for w in words)),
        "first_person_per_1000": rate(sum(w in FIRST for w in words)),
        "second_person_per_1000": rate(sum(w in SECOND for w in words)),
        "em_dashes_per_1000": rate(masked.count("—")),
        "semicolons_per_1000": rate(masked.count(";")),
        "colons_per_1000": rate(masked.count(":")),
        "questions_share": round(sum(s.rstrip(" \"'”’)").endswith("?") for s in spans) / len(spans), 3),
        "commas_per_sentence": round(masked.count(",") / len(lengths), 2),
        "function_words": {w: round(words.count(w) / total, 4) for w in FUNCTION},
    }
    return result


def compare(sample: Dict, edit: Dict) -> List[Dict]:
    drift = []
    for key, tolerance in TOLERANCE.items():
        before, after = sample.get(key, 0), edit.get(key, 0)
        delta = after - before
        if abs(delta) >= MIN_DELTA[key] and abs(delta) > tolerance * max(abs(before), 0.01):
            drift.append({"metric": key, "sample": before, "edit": after, "direction": "higher" if delta > 0 else "lower"})
    return drift


def main(argv: Optional[List[str]] = None) -> int:
    utf8_output()
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("sample", type=Path)
    parser.add_argument("--against", type=Path, metavar="EDIT")
    args = parser.parse_args(argv)
    sample = profile(read_document(args.sample))
    output: Dict = {"profile": sample}
    if sample.get("words", 0) < MIN_WORDS:
        output["warning"] = f"The sample has {sample.get('words', 0)} words. Under {MIN_WORDS}, the measurements are unreliable."
    if args.against:
        edit = profile(read_document(args.against))
        output["edit"] = edit
        output["drift"] = compare(sample, edit)
    json.dump(output, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 1 if output.get("drift") else 0


if __name__ == "__main__":
    raise SystemExit(main())
