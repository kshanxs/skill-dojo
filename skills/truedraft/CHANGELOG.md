# Changelog

All notable changes to the `truedraft` skill will be documented in this file.

## v1.3.0 — 2026-11-22
- **Removed detector-oriented advice:** The rewrite guidance no longer cites AI detectors or tells the writer to inject rare synonyms. It previously recommended words such as "leverage" and "underscores", which read as formulaic.
- **Sentence variety without quotas:** Replaced fixed per-paragraph length targets with guidance based on what helps the argument.
- **Version metadata:** Added the version to `SKILL.md`.

## v1.2.0 — 2026-06-22
- **Calligraph Sensei Proofreader Synergy:** Expanded synergy boundaries to support Calligraph Sensei's new conservative **Proofreading / Correction** mode, allowing users to run spelling and syntax audits without affecting scholarly tone or citations.
- **Emoji Cleanup:** Cleaned up documentation and skill markdown templates to maintain standard emoji-free instructions.

## v1.1.0 — 2026-06-21
- **Synergistic Integration (Research Dojo):** Integrated modular cross-referencing capabilities with the companion `Research Dojo` skill.
  - Added the Research Dojo workflow integration documentation to `README.md`.
  - Added conditional checks inside `open_generation` and `notes_first` pipelines in `SKILL.md` and `plan.md` to leverage Dojo's stress-tested arguments, and pre-populate onboarding details.

## v1.0.0 — 2026-06-21
- **TrueDraft Rebranding & Baselining:** Re-baselined the skill from `assignment-writer-skill` to `truedraft`. Reorganized the entire project structure and renamed paths to align with the core originality-first positioning.
- **Interactive Onboarding (The Forge):** Standardized a 9-question setup mapping institutional guidelines, word budget, and rubrics directly to project context.
- **Five-Stage Writing Pipeline:** Restructured the core flow into distinct stages: `plan`, `outline`, `draft`, `rewrite` (incorporating originality and readability passes), and `audit`.
- **Search-First Citation Engine:** Strict policy to search real scholarly databases/web using host tools, and default entirely to placeholders on search failure to prevent hallucinated references.
- **Originality & Readability Rewriter:** Implemented style-randomization and the `Humanise` readability passes (Light, Standard, Conversational) to remove robotic, predictable writing patterns.
- **CS/Data Science Stage:** Calibrated programming and report workflow supporting modular design, computational complexity mapping, and algorithm variety.
