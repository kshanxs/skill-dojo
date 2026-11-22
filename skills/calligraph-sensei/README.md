# 🖋️ Calligraph Sensei

**Polish and proofread your writing while it stays yours.**

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill calligraph-sensei
```

## Try It

```text
Proofread this: [paste or file]
Polish this chapter, but keep my voice
Audit my writing, don't change anything
Cut the em dashes and stock phrases from this
```

## What You Get

| | |
|---|---|
| ✍️ **Six editing modes** | Proofreading, General, Creative, Academic, Conversational, and code comments |
| 🔎 **Prose linter** | Catches real errors and overused patterns, tuned on 1.6 million words of human prose |
| 🧷 **Preservation check** | Proves numbers, quotes, citations, links, and code survived the edit |
| 🎙️ **Voice check** | Shows where an edit drifted from your habits |
| 💾 **Snapshots** | Saves a copy before any file is edited |
| 📏 **Your rules win** | Follows your style guide, voice notes, and `.calligraph.json` |

It will not invent facts, opinions, or anecdotes. It does not detect AI writing or promise any detector result.

## Run the Tools Directly

Python 3.9+ with no dependencies:

```bash
python3 scripts/prose_lint.py draft.md
python3 scripts/snapshot.py draft.md
python3 scripts/preserve_check.py draft-original.md draft.md
```

## Learn More

[Usage](docs/USAGE.md) · [Features](docs/FEATURES.md) · [Tool reference](references/tools.md) · [Changelog](CHANGELOG.md)

Works on its own. It also pairs well with [Research Dojo](../research-dojo/README.md) and [TrueDraft](../truedraft/README.md).
