# Fact-Check Workflow

## 1. Run the Offline Checks

```bash
python3 scripts/dojo_check.py draft.md --out-dir fact-check
```

This writes `draft.factcheck.md` (for people) and `draft.factcheck.json` (the ledger). The draft is not changed.

The offline pass finds:

- impossible dates, wrong weekdays, reversed ranges, age and "N years later" arithmetic
- past-tense events dated in the future
- invalid ISBN, ISSN and arXiv identifiers
- sentences with checkable claims, ranked by priority

A clean date check means the dates agree with the calendar and with each other. It does not mean they are historically right.

## 2. Look Up Sources

With permission, add `--online`. It checks DOIs against Crossref and doi.org, arXiv IDs against arXiv, ISBNs against Open Library, and whether URLs load.

| Status | Meaning | What to do |
|---|---|---|
| `format_ok` | Valid format, not looked up | Look it up |
| `not_checked` | URL not fetched | Open it |
| `format_invalid` | Fails its checksum or format | Likely a typo or invention |
| `source_found` | A record or page exists | Read it and compare with the claim |
| `metadata_mismatch` | Record differs from the citation | Likely a wrong or invented reference |
| `not_found` | The service has no record | Search elsewhere before calling it fake |
| `unreachable` | Service or site failed | Unknown. Try by hand |
| `blocked` | Not a public address | Skipped for safety |
| `retracted` | Marked retracted or withdrawn | Tell the author. Do not rely on it |

Books, grey literature, older works and non-English sources are often missing from these services. `not_found` is a reason to look harder, not proof of fabrication.

## 3. Check the Claims

Work from high priority to low. For each claim:

1. Search for the **primary source**: the original paper, dataset, statute, letter, or official record.
2. Read the part that matters. Do not rely on a search snippet.
3. Compare the exact detail: number, unit, date, name, scope, and wording of any quotation.
4. Look for one independent source, and for corrections, retractions, or newer data.
5. Record the result in the ledger.

Prefer sources in this order: primary records, peer-reviewed work and official statistics, reputable reference works and established journalism, then everything else. Trace a claim back: ten articles repeating one press release count as one source.

Common failures to look for: a quotation that was paraphrased or misattributed, a percentage with the wrong base, a correlation reported as a cause, an old figure stated as current, a study of mice reported as a finding in people, and a date from the wrong calendar (Old Style or New Style).

## 4. Record Results in the Ledger

Set each claim's `status` in the JSON file:

| Status | Requires |
|---|---|
| `unchecked` | Nothing. This is the default |
| `verified` | Evidence that supports the claim |
| `contradicted` | Evidence against it, and the corrected fact in `note` |
| `disputed` | Evidence on more than one side |
| `unverifiable` | A `note` saying what was searched |

```json
{
  "status": "verified",
  "evidence": [
    {
      "source": "https://doi.org/10.1038/nature14539",
      "locator": "p. 436, first paragraph",
      "quote": "short exact quotation",
      "checked_on": "2026-11-22"
    }
  ],
  "note": ""
}
```

Each evidence item needs a `source`, a `locator` or `quote`, and a `checked_on` date. Then validate:

```bash
python3 scripts/dojo_check.py --validate fact-check/draft.factcheck.json
```

Re-running the tool keeps reviews for unchanged sentences. If a sentence changes, its review resets to `unchecked`, because the old evidence may no longer apply.

## 5. Report

Lead with the count: how many claims were verified, contradicted, disputed, unverifiable and unchecked. List errors first, with the correction and source. Never call a draft "fact-checked" while high-priority claims remain unchecked.

To give the author a marked-up copy:

```bash
python3 scripts/dojo_check.py draft.md --annotate fact-check/draft.flagged.md
```

Flags are plain text at the end of the affected line: `[UNVERIFIED C012]`, `[CONTRADICTED C004]`, `[DISPUTED C007]`, `[DATE: ...]`, `[SOURCE retracted: ...]`.

## Checking One Claim

For a single claim, skip the script. Find the primary source, compare the exact detail, and answer with: verdict, the source and locator, the best counter-evidence, your confidence, and what new evidence would change the answer. If no source could be reached, the verdict is `unverifiable`.
