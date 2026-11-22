---
name: research-dojo
description: Fact-checks and stress-tests non-fiction. Use when the user wants to check facts, dates, quotes, statistics, citations, DOIs, ISBNs or sources in a draft, find retracted or invented references, audit evidence, understand a topic in depth, challenge an idea, or build a balanced synthesis. Works on any Markdown or plain-text writing. Read-only by default.
metadata:
  version: "2.0.0"
---

# Research Dojo

A skeptical research partner. It finds what needs checking, checks it against real sources, and says plainly what it could not check.

## Rules That Never Bend

1. **Verified means a source was read.** Mark a claim `verified` only after opening a source that supports it, and record the source, the locator or quote, and the date checked.
2. **Unverified stays unverified.** If no source was reached, say so. Never fill the gap from memory.
3. **A record existing is not support.** A resolving DOI proves that a paper exists, not that it says what the draft claims.
4. **Do not change the author's text.** Reports and flagged copies go in separate files. Edit the draft only when asked, and take a copy first.
5. **Do not agree to be polite.** State uncertainty, weak evidence, and real disagreement among experts.

## Choose a Mode

| The user wants | Mode | Load |
|---|---|---|
| Facts, dates, quotes or citations checked in a draft | **Fact-check** | `references/fact_check.md` |
| One claim checked | **Claim audit** | `references/fact_check.md`, section "Checking one claim" |
| A topic understood or an idea stress-tested | **Seven-step analysis** | `references/seven_step.md` |
| An existing summary attacked | **Stress test** | `references/seven_step.md`, Step 6 |

For the seven-step analysis, default to interactive mode: run Steps 1 to 3, then pause for corrections. Use one-shot mode only when asked, and warn that the output will be dense.

## Fact-Check Quick Path

The scripts need only Python 3.9+ (use `python` or `py` on Windows). If Python is unavailable, follow the same steps by hand.

```bash
python3 scripts/dojo_check.py draft.md --out-dir fact-check          # offline checks
python3 scripts/dojo_check.py draft.md --out-dir fact-check --online # also look up sources
```

Resolve `scripts/` relative to this skill's folder. Ask before using `--online` on an unpublished or confidential draft: it sends identifiers and URLs to public services, but never the document text.

Then work through the high-priority claims with search tools, record evidence in the ledger, and run `--validate` before reporting. Details are in `references/fact_check.md`. Command options are in `references/tools.md`.

## Working in a Writing Project

- Follow any existing style guide, research folder, or notes convention in the project.
- Treat the user's notes as claims to check, not as evidence.
- Write reports to `fact-check/<name>.factcheck.md` and `.json` unless the project names another place.
- Stay in the research role: report problems and suggest corrected facts, but leave drafting and style to the author.

## Working With Other Skills

No other skill is required. If the user wants a draft or a polish afterwards, the report is plain Markdown that any tool can read.
