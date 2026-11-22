# Calligraph Sensei Usage Guide

This guide shows you how to interact with Calligraph Sensei, how its automatic intent routing operates, and what the output formats look like.

---

## Quick Start

You do not need to memorize commands. Just speak naturally:
```text
"Polish this paragraph and make it more engaging: [paste]"
```
Calligraph Sensei will automatically identify the intent, select the appropriate mode, and return the formatted output.

---

## How It Chooses a Mode

| You ask to | Mode |
|---|---|
| Proofread, fix grammar, spelling, or typos | Proofreading |
| Audit, diagnose, or review style | Audit (no changes) |
| Polish a story or chapter | Creative |
| Polish an essay or paper | Academic-Formal |
| Make it casual or conversational | Conversational |
| Polish, tighten, or humanise | General |

If it could be either a proofread or a rewrite, it picks the smaller edit and tells you.

## Safe File Editing

```bash
python3 scripts/snapshot.py chapter.md            # 1. save a copy
# 2. edit chapter.md
python3 scripts/preserve_check.py <snapshot> chapter.md   # 3. confirm nothing was lost
python3 scripts/voice_profile.py <snapshot> --against chapter.md   # 4. check for drift
```

## Using Your Style Guide

If your project has a style guide or voice notes, tell the skill or keep them in the project. For the linter, add `.calligraph.json`:

```json
{ "allow": ["learnt"], "deny": ["utilize"], "em_dash": "allow" }
```

## Output Examples

### Style Edit Example

**Prompt:** `"Polish this: It is important to note that the algorithm is efficient."`

```text
### Edit: General, light

The algorithm is efficient.

| Change | Example | Why |
|---|---|---|
| Cut filler | "It is important to note that" | The opener added nothing |

Preservation: passed
Questions for the author: Can you say how efficient? A number would be stronger.
```

### Proofreading Example

**Prompt:** `"Proofread this paragraph: We has went to the store yesterday and buyed some apple's. It was a very importent task."`

**Output:**
```text
### Proofread

| Location | Original | Corrected | Type | Reason |
|---|---|---|---|---|
| 1 | "We has went to the store yesterday" | "We went to the store yesterday" | Grammar | Fixed auxiliary verb usage |
| 1 | "buyed" | "bought" | Grammar | Corrected irregular verb conjugation |
| 1 | "apple's" | "apples" | Punctuation | Removed errant possessive apostrophe from plural |
| 1 | "importent" | "important" | Spelling | Fixed typographical spelling error |

We went to the store yesterday and bought some apples. It was a very important task.

Queries (not changed): None
Preservation: passed
```
