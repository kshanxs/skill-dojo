# Preservation Audit

Run this before delivering any edit.

## 1. Machine Check

When the text is in files and Python is available:

```bash
python3 scripts/preserve_check.py original.md edited.md
```

It compares numbers, dates, citations, links, quotations, code, and headings, and raises changed names, negations, and hedges for review. Exit code 1 means a protected item changed. Restore it unless the author asked for that change.

## 2. Human Read

Compare each paragraph with its original.

- [ ] **Meaning:** no claim added, removed, strengthened, or weakened.
- [ ] **Hedges:** "may", "about", and "suggests" still present where the author used them.
- [ ] **Negation:** every "not", "never", and "without" still applies to the same thing.
- [ ] **Attribution:** every statement still belongs to the same person or source.
- [ ] **Terms:** proper nouns, technical terms, equations, and variables unchanged.
- [ ] **Structure:** headings, lists, tables, footnotes, and links intact.
- [ ] **Annotations:** placeholders and flags such as `[CITE: ...]`, `[UNVERIFIED ...]`, `TODO`, and editor notes preserved verbatim.
- [ ] **Voice:** still sounds like the author, with no invented opinions or anecdotes.
- [ ] **Style guide:** the project's rules were followed where they differ from this skill's defaults.

If a sentence fails, restore the original and try a smaller edit.

## 3. What to Deliver

1. The edited text, or the path of the edited file and its snapshot.
2. A short change table with the reason for each kind of change.
3. Anything you could not resolve, as a query to the author.
4. The preservation result, or a note that it was not run.
