# Calligraph Sensei Features

**v2.0.0**

## Editing Modes

| Mode | Use for | Changes |
|---|---|---|
| Proofreading | Final drafts | Objective errors only. Style and punctuation choices stay |
| General (default) | Articles, documentation, non-fiction | Clarity, directness, rhythm |
| Creative | Fiction and narrative | Prose only. Plot, facts, and dialogue voice stay |
| Academic-Formal | Essays and papers | Formal clarity, with every hedge and citation kept |
| Conversational | Emails, posts, messages | Warmer and looser, still the author |
| Code comments | Source code | Comments only. Code never changes |
| Audit | Any text | Nothing. Report only |

## Tools

| Tool | What it does |
|---|---|
| `prose_lint.py` | Finds doubled words, misspellings, grammar slips, a/an errors, assistant residue, stock phrases, vague sourcing, em dash overuse, and mixed spelling |
| `preserve_check.py` | Compares an edit with its original for numbers, dates, citations, links, quotations, code, and headings, and raises names, negation, and hedges for review |
| `voice_profile.py` | Compares sentence length, contractions, person, and punctuation habits between an original and its edit |
| `snapshot.py` | Saves a checksum-verified copy before editing |

All tools skip code, links, and front matter, need only Python 3.9+, and never change the file they read.

## Calibration

The linter was tuned on about 1.6 million words of human writing: 14 public-domain books and 10 Wikipedia articles. On that set, it raises about 0.2 errors and warnings per 1,000 words. Short public-domain excerpts in `tests/corpus/` guard this in the test suite.

## Project Settings

`.calligraph.json` sets allowed and banned terms, disabled rules, and the em dash policy. See the [tool reference](../references/tools.md).

## Commands

| Say | What happens |
|---|---|
| `Proofread this: [text]` | Proofreading |
| `Polish this: [text]` | General edit |
| `Polish this story: [text]` | Creative edit |
| `Polish this essay: [text]` | Academic edit |
| `Make this more conversational: [text]` | Conversational edit |
| `Clean up the comments in this code` | Code comments |
| `Audit my writing: [text]` | Report only |

## Limits

- It is not an AI detector and makes no claim about who wrote a text.
- The linter catches a small set of high-confidence errors. It does not replace a full grammar checker or a human editor.
- Rules are English-focused.
- `preserve_check.py` compares surface details and cannot judge meaning.
