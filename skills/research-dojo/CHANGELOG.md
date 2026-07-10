# Changelog

All notable changes to the `research-dojo` skill will be documented in this file.

## v1.3.0 — 2026-06-21
- **Book-Writer Integration & Boundary Protocol:** Added boundary controls to prevent prompt-clash and persona contamination during book manuscript projects.
  - Added a Boundary Protocol restricting research-dojo to fact/analogy/argument audits (no narrative drafting) when a `book-memory-bank` is detected in the workspace.
  - Expanded the Production Hand-off in `SKILL.md` with explicit templates and workflows for export to `book-writer` non-fiction projects.

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
