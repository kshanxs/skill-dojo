# Tool Reference

All scripts use only the Python standard library (3.9+). None of them changes the file it reads.

| Script | Purpose |
|---|---|
| `prose_lint.py FILE` | Find errors and overused patterns |
| `preserve_check.py ORIGINAL EDITED` | Find lost or changed facts. Exit 1 if any |
| `voice_profile.py ORIGINAL --against EDITED` | Show where an edit drifts from the original's habits |
| `snapshot.py FILE` | Save a dated copy before editing |

## `prose_lint.py` Options

| Option | Effect |
|---|---|
| `--format md\|json` | Report format |
| `--out PATH` | Write the report to a file. Refuses the input path |
| `--config PATH` | Use this settings file |
| `--fail-on error\|warning\|never` | Exit 1 at this severity. Default `never` |

Severities: `error` is very likely wrong, `warning` deserves a look, and `info` is a note. Code, links, front matter and comments are skipped. Style rules also skip quotations.

## Project Settings

Put `.calligraph.json` in the project. The nearest one above the file is used.

```json
{
  "allow": ["colour", "learnt"],
  "deny": ["utilize"],
  "disable": ["negative-parallel"],
  "em_dash": "allow",
  "em_dash_limit": 2
}
```

| Setting | Meaning |
|---|---|
| `allow` | Terms never flagged |
| `deny` | Terms always flagged |
| `disable` | Rule names to turn off |
| `em_dash` | `allow`, `limit` (default), or `avoid` |
| `em_dash_limit` | Per-paragraph limit for `limit` |

## Limits

- `prose_lint.py` is not an AI detector, and a clean report says nothing about authorship. It is not a full grammar checker either. It catches a small set of high-confidence errors.
- `voice_profile.py` is meaningful only for an edit against its own original. Separate passages by one author can differ widely.
- `preserve_check.py` compares surface items. It cannot judge meaning, so a person should still read the edit.
- If LanguageTool, Vale, or proselint is already installed or configured in the project, you may run it as well. None is required.
