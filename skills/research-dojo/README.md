# 🔬 Research Dojo

**Check the facts, dates, and sources in any non-fiction, and find out what you actually know.**

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill research-dojo
```

## Try It

```text
Fact-check this draft: chapter-3.md
Is this reference real? [paste citation]
Audit this claim: [claim]
I want to understand the topic: [topic]
```

## What You Get

| | |
|---|---|
| 📋 **Claim ledger** | Every checkable claim, ranked, with its evidence and status |
| 📅 **Date checks** | Impossible dates, wrong weekdays, reversed ranges, and age arithmetic |
| 📚 **Source checks** | DOI, ISBN, ISSN, and arXiv validation, dead links, and retractions |
| 🛡️ **Honest status** | Nothing is `verified` until someone has read a source |
| ⚔️ **Seven-step analysis** | Map a topic, compare perspectives, then attack the conclusion |

Your draft is never changed. Reports go to separate files, and any flagged copy is a new file.

## Run the Tools Directly

Python 3.9+ with no dependencies:

```bash
python3 scripts/dojo_check.py draft.md --out-dir fact-check
python3 scripts/dojo_check.py draft.md --out-dir fact-check --online
```

The first command is fully offline. `--online` sends identifiers and URLs to public services, never your text.

## Learn More

[Usage](docs/USAGE.md) · [Features](docs/FEATURES.md) · [Fact-check workflow](references/fact_check.md) · [Tool reference](references/tools.md) · [Changelog](CHANGELOG.md)

Works on its own. It also pairs well with [TrueDraft](../truedraft/README.md) and [Calligraph Sensei](../calligraph-sensei/README.md).
