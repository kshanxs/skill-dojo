# Tool Reference

All scripts use only the Python standard library (3.9+) and never modify the input file.

| Script | Purpose |
|---|---|
| `dojo_check.py` | Full report and ledger. Start here |
| `extract_claims.py FILE [--priority high]` | List checkable claims as JSON |
| `check_dates.py FILE [--as-of YYYY-MM-DD]` | Date findings as JSON |
| `check_sources.py FILE [--online]` | Identifier and URL status as JSON |

## `dojo_check.py` Options

| Option | Effect |
|---|---|
| `--out-dir DIR` | Write `<name>.factcheck.md` and `.json` |
| `--online` | Look up sources in public services |
| `--as-of DATE` | Treat this date as today |
| `--annotate COPY` | Write a flagged copy. Refuses the input path or an existing file |
| `--format md\|json` | Format for stdout |
| `--validate LEDGER` | Exit 1 if any review status lacks evidence |

## Privacy and Network

Offline is the default. `--online` sends DOIs, arXiv IDs, ISBNs and the URLs found in the document to Crossref, doi.org, arXiv, Open Library, and the linked sites. It does not send document text. It refuses private and local network addresses, including through redirects.

Set `CROSSREF_MAILTO` to your own address if you want Crossref's polite pool. Nothing is sent otherwise.
