# Changelog

All notable changes to the `research-dojo` skill will be documented in this file.

## v2.0.0 — 2026-11-22

### Breaking
- **Removed workspace-specific behavior.** The skill no longer changes behavior based on a particular project folder. It now follows generic conventions in any writing project.
- **`SKILL.md` restructured.** The seven-step detail moved to `references/seven_step.md`, loaded only when needed.

### Added
- **Fact-check mode** with a claim ledger, a report, and optional flagged copies. The input file is never changed.
- `scripts/check_dates.py`: finds impossible dates, wrong weekdays (aware of Julian and Gregorian calendars), reversed ranges, and age or elapsed-time errors.
- `scripts/check_sources.py`: validates ISBN, ISSN, arXiv, and DOI formats offline. With `--online`, looks up sources and flags retractions, mismatched metadata, and dead links.
- `scripts/extract_claims.py`: lists checkable claims by priority.
- `scripts/dojo_check.py`: runs everything, keeps reviews across re-runs, and rejects any `verified` status that has no recorded evidence.

### Fixed
- Step 4 no longer assumes that a search tool exists. Without one, claims stay `unchecked`.
- Corrected the stale version and repository layout in the docs.

## v1.3.0 — 2026-06-21
- **Project Boundary Protocol:** Added controls to keep research output separate from drafting in long-form projects.

## v1.2.0 — 2026-06-21
- **Synergistic Integration (TrueDraft):** Integrated modular cross-referencing capabilities with the companion `TrueDraft` skill.
  - Added the TrueDraft companion documentation to `README.md`.
  - Added a Production Hand-off section at the end of the research pipeline (Step 7) in `SKILL.md` to direct users to export and feed Dojo findings directly into TrueDraft to write academic reports.

## v1.1.0 — 2026-06-21
- **Copyright Completeness:** Updated the copyright owner name to "Shubhanshu Shukla" for legal compliance in the LICENSE and README.md.
- **Smart Perspective Substitution:** Updated Step 2 in the skill definition to allow the agent to dynamically swap up to two default perspectives for specialized ones (e.g., Ethicist, Mathematician) on niche topics.
- **Active Search Grounding:** Introduced a mandatory web search grounding step to Step 4 (Evidence Audit) to ensure confidence ratings and evidence evaluations are backed by real-time sources.
- **Clearer Phase Gating:** Refined the execution modes to encourage Phase 1 and Phase 2 gating during interactive execution.

## v1.0.0 — 2026-06-20
- **Initial Release:** Complete implementation of the 7-step Research Adversary and Synthesis Partner pipeline.
- **Interactive and One-Shot Modes:** Added support for stage-gated interactive execution to avoid token limits, and high-density one-shot tables.
- **Repository Scaffold:** Added complete documentation, usage examples, test suites, and packaging tools.
