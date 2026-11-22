# Research Dojo Features

**v2.0.0**

## Fact-Check Mode

| Feature | What it does |
|---|---|
| Claim extraction | Finds sentences with dates, numbers, quotations, attributions, superlatives, and causal claims, ranked by priority |
| Date checks | Flags impossible dates, wrong weekdays, reversed ranges, implausible lifespans, age errors, elapsed-time errors, future events in the past tense, and ambiguous numeric dates |
| Calendar awareness | Separates true errors from dates that fit the Julian (Old Style) calendar |
| Identifier checks | Validates ISBN and ISSN checksums and DOI and arXiv formats offline |
| Source lookup | With `--online`, checks Crossref, doi.org, arXiv, Open Library, and linked pages |
| Retraction flags | Reports works marked retracted or withdrawn in Crossref, including Retraction Watch data |
| Mismatch detection | Compares a citation's year, title, and authors with the record |
| Evidence ledger | Stores the status, source, locator, and date for each claim |
| Honest status | `--validate` rejects a `verified` claim with no recorded evidence |
| Safe re-runs | Keeps reviews of unchanged sentences and resets changed ones |

## Seven-Step Analysis

1. **Build the map:** core question, concepts, misconceptions, debates, and blind spots.
2. **Multi-perspective analysis:** six viewpoints, with domain-specific swaps.
3. **Contradiction analysis:** evidence conflicts and value conflicts.
4. **Evidence audit:** confidence, best evidence, counter-evidence, and what would change the conclusion.
5. **Synthesis:** beginner and expert explanations, a mental model, and implications.
6. **Stress test:** the strongest hostile critique.
7. **Final judgment:** what holds up, what is uncertain, and what to do.

## Commands

| Say | What happens |
|---|---|
| `Fact-check this draft: [file or paste]` | Fact-check mode |
| `Check the dates in this` | Date checks |
| `Are these references real?` | Source checks |
| `Audit this claim: [claim]` | Single-claim audit |
| `I want to understand the topic: [topic]` | Seven-step analysis |
| `Run in interactive mode` | Pauses after Step 3 |
| `Run in one-shot mode` | All seven steps at once |
| `Challenge the synthesis` | Step 6 on an existing summary |

## Package Layout

```text
skills/research-dojo/
├── SKILL.md            Agent instructions
├── references/         Workflows, loaded when needed
├── scripts/            Standard-library Python tools
├── evals/              Test prompts
└── docs/               Usage and features
```

## Limits

- Automatic checks find inconsistencies and bad identifiers. They cannot establish that a claim is true.
- Claim extraction is English-focused and may miss implied claims.
- Coverage gaps in public databases mean `not_found` is not proof that a source is fake.
