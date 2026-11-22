# Editing Workflows and Output Templates

## Audit (read-only)

1. Run `scripts/prose_lint.py` if possible, or review by hand with `references/humanise.md`.
2. Separate objective errors from style observations.
3. Report using Template 1. Do not rewrite unless asked.

Sentence statistics describe the text. They are not a score, and they do not indicate who wrote it.

## Style Edit

1. Confirm the mode, the edit depth (light, standard, or heavy), and protected terms.
2. Take a snapshot if you will edit a file.
3. Edit paragraph by paragraph, using `references/humanise.md` and `references/rhythm.md`.
4. Run the preservation audit.
5. Deliver using Template 2.

## Proofreading

1. Do not load `references/rhythm.md`. Do not change style.
2. Fix spelling, grammar, punctuation, and consistency errors only.
3. Respect the document's dialect (US, UK, or other) and any house style.
4. Leave dialogue, dialect, and deliberate fragments alone. Query them if unsure.
5. Log every change, run the preservation audit, and deliver using Template 3.

## Template 1: Audit

```text
### Style Audit: [name]

[words], [sentences], mean sentence [x] words, readability [Flesch]

| Priority | Location | Issue | Suggestion |
|---|---|---|---|
| Error | line 12 | "recieved" | received |
| Style | line 30 | "plays a crucial role" | Say what depends on it |

What works: [specific strengths worth keeping]
Questions for the author: [anything only they can decide]
```

## Template 2: Style Edit

```text
### Edit: [mode], [depth]

[edited text, or path to edited file and snapshot]

| Change | Example | Why |
|---|---|---|
| Cut filler | "It is important to note that the algorithm is efficient." -> "The algorithm is efficient." | The opener added nothing |

Preservation: [passed / items to review / not run]
Questions for the author: [or "None"]
```

## Template 3: Proofread

```text
### Proofread

[corrected text, or path to corrected file and snapshot]

| Location | Original | Corrected | Type | Reason |
|---|---|---|---|---|
| Para 1 | "We has checked" | "We have checked" | Grammar | Subject-verb agreement |

Queries (not changed): [or "None"]
Preservation: [passed / items to review / not run]
```
