#!/usr/bin/env python3
"""Lint prose for errors and overused patterns. Read-only.

Findings are prompts for a human editor. This tool does not detect AI authorship,
and a clean result says nothing about who wrote a text.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

sys.dont_write_bytecode = True  # leave the installed skill folder untouched
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _mdtext import LineIndex, mask, paragraphs, read_document, sentences, utf8_output  # noqa: E402

CONFIG_NAME = ".calligraph.json"
DEFAULTS = {"allow": [], "deny": [], "disable": [], "em_dash": "limit", "em_dash_limit": 2}
WORD = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*")

DOUBLED_OK = {"had", "that", "so", "very", "really", "bye", "no", "yes", "well", "there", "now", "many", "far", "hear", "is", "do", "pooh", "little", "long", "again", "knock", "night", "come", "go", "run", "away", "more", "out"}
SHORT_WORDS = {"the", "a", "an", "of", "to", "in", "on", "at", "by", "it", "and", "or", "for", "but", "as", "be", "we", "he", "she", "you", "are", "was", "not", "his", "her"}  # other short repeats are usually interjections
AN_CONSONANT_SOUND = re.compile(r"^(?:uni(?!n|m)|use|usu|uti|ura|eu|ewe|one\b|once\b|ubiq|u-)", re.I)
A_VOWEL_SOUND = re.compile(r"^(?:hour|honest|honou?r|heir)", re.I)
MISSPELLINGS = {
    "accomodate": "accommodate", "acheive": "achieve", "adress": "address", "alot": "a lot",
    "arguement": "argument", "beleive": "believe", "calender": "calendar", "collegue": "colleague",
    "concious": "conscious", "definately": "definitely", "definitly": "definitely", "enviroment": "environment",
    "existance": "existence", "goverment": "government", "gaurd": "guard", "harrass": "harass",
    "independant": "independent", "occured": "occurred", "occurence": "occurrence", "occurance": "occurrence",
    "persistant": "persistent", "posession": "possession", "prefered": "preferred", "publically": "publicly",
    "recieve": "receive", "recieved": "received", "refered": "referred", "relevent": "relevant",
    "seperate": "separate", "seperately": "separately", "succesful": "successful", "tommorow": "tomorrow",
    "tounge": "tongue", "truely": "truly", "untill": "until", "wierd": "weird", "wich": "which", "teh": "the",
    "thier": "their", "importent": "important", "buyed": "bought",
}
GRAMMAR = [
    (re.compile(r"\b(could|should|would|must|might)\s+of\s+(?:been|had|done|gone|seen|known|made|taken|got|said|\w+ed)\b", re.I), "modal-of", "Use '{1} have', not '{1} of'."),
    (re.compile(r"\b(your)\s+welcome\b", re.I), "your-youre", "Use \"you're welcome\"."),
    (re.compile(r"\bits'", re.I), "its-apostrophe", "\"its'\" is not a word. Use 'its' or \"it's\"."),
    (re.compile(r"\b(?:he|she|it)\s+don't\b", re.I), "subject-verb", "Use \"doesn't\" with he, she or it."),
    (re.compile(r"\b(?:we|they|you)\s+(?:was)\b(?!\s+to\b)", re.I), "dialect-or-agreement", "Standard English uses 'were' here. Keep it if the dialect is deliberate."),
    (re.compile(r"\b(?:we|they)\s+has\b", re.I), "subject-verb", "Use 'have' with we or they."),
    (re.compile(r"\b(?:has|have|had)\s+went\b", re.I), "verb-form", "Use 'gone' after has, have or had."),
    (re.compile(r"\bet\.\s+al\b"), "et-al", "Write 'et al.' with no period after 'et'."),
]
CHAT_RESIDUE = re.compile(
    r"\bas an ai(?: language model| assistant)?\b|\bas of my (?:last )?(?:knowledge|training)\b|\bmy knowledge cutoff\b"
    r"|\bi hope this helps\b|^\s*great question[!.,]|\bhere(?:'s| is) (?:a |an |the )?(?:revised|polished|rewritten|updated) (?:version|draft)\b"
    r"|\bwould you like me to\b|\blet me know if you(?:'d| would)? like\b|\[insert [^\]]+\]",
    re.I | re.M,
)
STOCK_PHRASES = re.compile(
    r"\bin today's (?:fast-paced|digital|modern|ever-changing|rapidly evolving)\b"
    r"|\bever-(?:evolving|changing) (?:landscape|world)\b|\bstands? as a testament\b|\ba testament to\b"
    r"|\b(?:rich|intricate|vibrant) tapestry\b|\bdelves? into\b|\bplays? a (?:crucial|pivotal|vital|key) role\b"
    r"|\bit(?:'s| is) (?:important|worth|crucial) (?:to note|noting|mentioning|to remember)\b"
    r"|\bnavigat(?:e|ing) the (?:complexities|challenges|landscape|intricacies)\b|\bunlock(?:ing)? the (?:power|potential)\b"
    r"|\bthe (?:ever-)?(?:evolving|changing) landscape\b|\bgame[- ]changer\b"
    r"|\bseamless(?:ly)? integrat|\bfoster(?:ing)? (?:a sense of|innovation|collaboration)\b"
    r"|\bleverag(?:e|es|ing) the power\b|\bin conclusion, it is clear\b|\bmake no mistake\b|\blet that sink in\b"
    r"|\bhere's the thing\b|\bthe uncomfortable truth\b",
    re.I,
)
OVERUSED = {"delve", "delves", "delving", "tapestry", "multifaceted", "underscore", "underscores", "underscoring", "pivotal", "seamless", "seamlessly", "robust", "leverage", "leveraging", "leverages", "showcase", "showcases", "showcasing", "foster", "fosters", "fostering", "realm", "beacon", "crucial", "landscape", "holistic", "nuanced", "transformative", "groundbreaking", "unprecedented", "streamline", "streamlines", "harness", "harnessing", "elevate", "elevates"}
NEGATIVE_PARALLEL = re.compile(
    r"\b(?:it|this|that)(?:'s| is|’s)\s+not\s+(?:just\s+|only\s+|merely\s+|simply\s+|about\s+)?[^.;:!?\n]{1,50}[.;:,—–]\s*(?:it|this|that)(?:'s| is|’s)\s"
    r"|\bnot\s+(?:just|merely|simply)\s+[^.;:!?\n]{1,50}[,;—–]\s*but\b|\bmore than just\b",
    re.I,
)
VAGUE_SOURCE = re.compile(r"\b(?:experts|observers|critics|analysts|scholars|researchers|studies|research)\s+(?:say|says|agree|believe|note|suggest|suggests|show|shows|argue|have shown)\b|\bit is (?:widely|generally|commonly) (?:believed|accepted|known|thought)\b|\bmany (?:people )?believe\b", re.I)
WORDY = {"due to the fact that": "because", "in spite of the fact that": "although", "at this point in time": "now", "in the event that": "if", "for the purpose of": "to", "has the ability to": "can", "a large number of": "many", "needless to say": "(cut)", "at the end of the day": "(cut)"}
_WORDY = re.compile("|".join(r"\b" + re.escape(k) + r"\b" for k in WORDY), re.I)
PASSIVE = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(?:\w+ed|built|done|given|known|made|seen|shown|taken|written|found|held|left|paid|said|sent|told)\b", re.I)
SPELLING_PAIRS = [("organize", "organise"), ("realize", "realise"), ("recognize", "recognise"), ("analyze", "analyse"), ("color", "colour"), ("favor", "favour"), ("honor", "honour"), ("center", "centre"), ("defense", "defence"), ("traveled", "travelled")]


def load_config(path: Optional[Path], start: Optional[Path]) -> Dict:
    config = dict(DEFAULTS)
    if path is None and start is not None:
        for parent in [start.resolve().parent, *start.resolve().parents]:
            if (parent / CONFIG_NAME).is_file():
                path = parent / CONFIG_NAME
                break
    if path is not None:
        loaded = json.loads(Path(path).read_text(encoding="utf-8"))
        unknown = set(loaded) - set(DEFAULTS)
        if unknown:
            raise ValueError(f"unknown settings in {path}: {', '.join(sorted(unknown))}")
        config.update(loaded)
    if config["em_dash"] not in ("allow", "limit", "avoid"):
        raise ValueError("em_dash must be allow, limit or avoid")
    return config


def _syllables(word: str) -> int:
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    count = len(re.findall(r"[aeiouy]+", word))
    if word.endswith("e") and not word.endswith(("le", "ee")) and count > 1:
        count -= 1
    return max(count, 1)


def stats(text: str) -> Dict:
    masked = mask(text)
    lengths = []
    passive = 0
    syllables = 0
    for start, end in sentences(masked):
        sentence = masked[start:end]
        if sentence.lstrip().startswith(("#", "|")):
            continue
        words = WORD.findall(sentence)
        if words:
            lengths.append(len(words))
            syllables += sum(_syllables(w) for w in words)
            passive += bool(PASSIVE.search(sentence))
    words = sum(lengths)
    result = {"words": words, "sentences": len(lengths)}
    if not lengths:
        return result
    per_sentence = words / len(lengths)
    per_word = syllables / words
    result.update(
        mean_sentence_words=round(per_sentence, 1),
        sentence_length_sd=round(statistics.pstdev(lengths), 1),
        passive_share=round(passive / len(lengths), 2),
        flesch_reading_ease=round(206.835 - 1.015 * per_sentence - 84.6 * per_word, 1),
        flesch_kincaid_grade=round(0.39 * per_sentence + 11.8 * per_word - 15.59, 1),
        em_dashes_per_1000=round(masked.count("—") * 1000 / words, 1),
    )
    return result


def lint(text: str, config: Optional[Dict] = None) -> Dict:
    config = {**DEFAULTS, **(config or {})}
    allow = {term.lower() for term in config["allow"]}
    disabled = set(config["disable"])
    index = LineIndex(text)
    masked = mask(text)
    prose = mask(text, quotes=True)  # style rules skip quoted material
    findings: List[Dict] = []

    def add(rule: str, severity: str, offset: int, snippet: str, message: str) -> None:
        if rule in disabled or snippet.lower().strip() in allow:
            return
        findings.append({"rule": rule, "severity": severity, "line": index.line(offset), "text": " ".join(snippet.split())[:80], "message": message})

    for m in re.finditer(r"\b([^\W\d_]+)[ \t]+\1\b", masked, re.I):
        word = m[1].lower()
        if word not in DOUBLED_OK and (len(word) > 3 or word in SHORT_WORDS):
            add("doubled-word", "error", m.start(), m.group(), f"Repeated word: '{m[1]}'.")
    for m in WORD.finditer(masked):
        fix = MISSPELLINGS.get(m.group().lower())
        if fix:
            add("spelling", "error", m.start(), m.group(), f"Did you mean '{fix}'?")
    for pattern, rule, message in GRAMMAR:
        for m in pattern.finditer(prose):
            severity = "warning" if rule == "dialect-or-agreement" else "error"
            add(rule, severity, m.start(), m.group(), message.replace("{1}", m[1].lower() if m.groups() else ""))
    for m in re.finditer(r"\b(a|an)\s+([A-Za-z][\w-]*)", prose):
        article, word = m[1], m[2]
        if word.isupper() or len(word) < 2:
            continue
        vowel = word[0].lower() in "aeiou"
        if article == "a" and ((vowel and not AN_CONSONANT_SOUND.match(word)) or A_VOWEL_SOUND.match(word)):
            add("a-an", "warning", m.start(), m.group(), f"Use 'an {word}'.")
        elif article == "an" and not vowel and word[0].lower() != "h":  # "an historic" is accepted usage
            add("a-an", "warning", m.start(), m.group(), f"Use 'a {word}'.")
        elif article == "an" and AN_CONSONANT_SOUND.match(word):
            add("a-an", "warning", m.start(), m.group(), f"Use 'a {word}'.")
    for m in re.finditer(r"[^\W\d_]{2} +[,;:!?](?=\s|$)", prose, re.M):
        add("space-before-punctuation", "warning", m.start(), m.group(), "Remove the space before the punctuation mark.")
    for start, end in paragraphs(masked):
        block = masked[start:end]
        if block.count("(") != block.count(")") and not re.search(r"^\s*(?:\d+|[a-z])\)", block, re.M):
            add("unbalanced-parens", "info", start, block[:60], "Parentheses do not balance in this paragraph.")

    for m in CHAT_RESIDUE.finditer(prose):
        add("chat-residue", "error", m.start(), m.group(), "Looks like leftover assistant text. Remove it.")
    for m in STOCK_PHRASES.finditer(prose):
        add("stock-phrase", "warning", m.start(), m.group(), "Stock phrase. Say the specific thing.")
    for m in NEGATIVE_PARALLEL.finditer(prose):
        add("negative-parallel", "info", m.start(), m.group(), "'Not X, but Y' framing. Keep it only if someone really thinks X.")
    for m in VAGUE_SOURCE.finditer(prose):
        add("vague-source", "warning", m.start(), m.group(), "Who? Name the source or soften the claim.")
    for m in _WORDY.finditer(prose):
        add("wordy", "info", m.start(), m.group(), f"Shorter: {WORDY[m.group().lower()]}.")
    for term in config["deny"]:
        for m in re.finditer(r"\b" + re.escape(term) + r"\b", masked, re.I):
            findings.append({"rule": "project-deny", "severity": "error", "line": index.line(m.start()), "text": m.group(), "message": "The project style guide bans this term."})

    words = [w.lower() for w in WORD.findall(prose)]
    total = max(len(words), 1)
    hits = Counter(w for w in words if w in OVERUSED and w not in allow)
    density = sum(hits.values()) * 1000 / total
    if "overused-word" not in disabled and sum(hits.values()) >= 3 and density >= 4:
        first = next(re.finditer(r"\b(?:" + "|".join(hits) + r")\b", prose, re.I))
        findings.append({"rule": "overused-word", "severity": "warning", "line": index.line(first.start()), "text": ", ".join(f"{k} ×{v}" for k, v in hits.most_common(8)), "message": f"{density:.1f} per 1,000 words. Replace the ones that carry no specific meaning."})

    if config["em_dash"] != "allow" and "em-dash" not in disabled:
        for start, end in paragraphs(prose):
            count = prose.count("—", start, end) + len(re.findall(r"(?<=\w) -- (?=\w)", prose[start:end]))
            limit = 0 if config["em_dash"] == "avoid" else int(config["em_dash_limit"])
            if count > limit:
                add("em-dash", "warning" if config["em_dash"] == "avoid" else "info", start, prose[start:end].strip()[:60], f"{count} em dashes in this paragraph (limit {limit}).")

    if "spelling-consistency" not in disabled:
        lower = masked.lower()
        for us, uk in SPELLING_PAIRS:
            a = len(re.findall(r"\b" + us + r"(?:s|d|r|rs|ing|ation|ations)?\b", lower))
            b = len(re.findall(r"\b" + uk + r"(?:s|d|r|rs|ing|ation|ations)?\b", lower))
            if a and b:
                findings.append({"rule": "spelling-consistency", "severity": "info", "line": 1, "text": f"{us} ×{a}, {uk} ×{b}", "message": "Both US and UK spellings appear."})

    order = {"error": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["line"]))
    return {"stats": stats(text), "counts": dict(Counter(f["severity"] for f in findings)), "findings": findings}


def render(result: Dict, name: str) -> str:
    s = result["stats"]
    lines = [f"# Prose lint: {name}", ""]
    if s.get("sentences"):
        lines.append(f"{s['words']} words, {s['sentences']} sentences. Mean sentence {s['mean_sentence_words']} words (SD {s['sentence_length_sd']}). Flesch {s['flesch_reading_ease']}, grade {s['flesch_kincaid_grade']}. Passive about {round(s['passive_share'] * 100)}%. Em dashes {s['em_dashes_per_1000']} per 1,000 words.")
    c = result["counts"]
    lines += ["", f"{c.get('error', 0)} errors, {c.get('warning', 0)} warnings, {c.get('info', 0)} notes. This is an editing aid and does not detect AI authorship.", ""]
    if result["findings"]:
        lines += ["| Line | Severity | Rule | Text | Suggestion |", "|---:|---|---|---|---|"]
        for f in result["findings"]:
            text = f["text"].replace("|", "\\|")
            lines.append(f"| {f['line']} | {f['severity']} | {f['rule']} | {text} | {f['message']} |")
    return "\n".join(lines) + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    utf8_output()
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("file", type=Path)
    parser.add_argument("--config", type=Path, help=f"settings file (default: nearest {CONFIG_NAME})")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    parser.add_argument("--out", type=Path, help="write the report here instead of stdout")
    parser.add_argument("--fail-on", choices=["error", "warning", "never"], default="never", help="exit 1 at this severity")
    args = parser.parse_args(argv)
    if not args.file.is_file():
        parser.error(f"no such file: {args.file}")
    if args.out and args.out.resolve() == args.file.resolve():
        parser.error("--out must not point at the input file")
    try:
        config = load_config(args.config, args.file)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    result = lint(read_document(args.file), config)
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n" if args.format == "json" else render(result, args.file.name)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    counts = result["counts"]
    failed = (args.fail_on == "error" and counts.get("error")) or (args.fail_on == "warning" and (counts.get("error") or counts.get("warning")))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
