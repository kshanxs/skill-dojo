# Changelog

All notable changes to the `calligraph-sensei` skill will be documented in this file.

## v2.0.0 — 2026-11-22

### Breaking
- **Repositioned around voice-preserving editing.** Removed the "bypass AI detectors" and "de-risk" triggers and all claims about beating detectors. The skill makes no authorship claims and will not help conceal AI use where disclosure is required.
- **Replaced "perplexity tuning".** The old guidance told the editor to swap plain words for rarer ones, including words its own catalog banned. `references/style_randomization.md` is now `references/rhythm.md`.
- **Removed project-specific integrations.** The skill now works with any project through generic conventions.

### Added
- `scripts/prose_lint.py`: Markdown-aware linter for high-confidence errors and overused patterns, with per-project settings in `.calligraph.json`.
- `scripts/preserve_check.py`: compares an edit with its original for changed numbers, citations, links, quotations, code, headings, names, negation, and hedges.
- `scripts/voice_profile.py`: measures an edit's drift from its original's writing habits.
- `scripts/snapshot.py`: saves a verified copy before a file is edited.
- `references/tools.md`: tool options, settings, and limits.

### Fixed
- Proofreading mode no longer strips the author's em dashes.
- Worked examples no longer invent facts. One had added "without memory overhead" to a sentence, which broke the skill's own preservation rule.
- The voice pass no longer tells the editor to add opinions, feelings, or first-person statements the author did not write.
- Code-comment examples no longer invent reasons or complexity claims.
- Removed unsupported "AI risk" ratings and fixed sentence-length thresholds.

## v1.1.0 — 2026-07-01
- **AI Signature Detection Catalog (Section 4 of humanise.md):** Pulled from the Wikipedia "Signs of AI writing" community guide. Adds explicit detection patterns that were missing: em dash overuse (max 2 per paragraph), rule of three, negative parallelisms, inflated symbolism, promotional adjectives, vague attributions, sycophantic openings, generic filler openers, superficial -ing analyses.
- **Personality & Soul Section (Section 5 of humanise.md):** New guidance on adding voice, not just removing slop. Prevents rewrites from becoming sterile technical exercises.
- **Workflow Discipline Section (Section 6 of humanise.md):** Added the "would a skeptical reader say this was written by a person?" meta-check, plus explicit "When NOT to humanize" guidance.
- **Check 6 in audit_checklist.md:** New audit stage for voice/personality, not just pattern removal.
- **Trimmed SKILL.md frontmatter:** Reduced trigger description to under 200 words for better loading accuracy. Replaced em dash overuse in the body itself with prose alternatives.
- **Source attribution:** Added explicit credit to the `biostartechnology/humanizer` skill (clawhub) as inspiration for the detection patterns and personality guidance.
- **Repository Reorganization:** Relocated the `evals` folder (`evals/evals.json`) inside the core `calligraph-sensei/` skill directory to standardize repository layout and ensure self-contained distribution when installing the skill.

## v1.0.0 — 2026-06-22
- **Initial Release:** Complete implementation of the Calligraph Sensei writing style polisher, humanizer, and AI detection mitigation assistant.
- **Five Specialized Modes:** Added support for Creative/Fiction, Academic-Formal, Non-fiction/General, Conversational/Casual, and conservative Proofreading/Correction styles.
- **Automatic Intent Routing:** Integrated a dispatcher to automatically select the correct mode based on prompt keywords (e.g., proofread vs. humanise).
- **Originality & Readability Engine:** Enforced statistical perplexity tuning, sentence type rotation, burstiness length variation, and semantic preservation audits.
- **Synergy & Boundaries:** Established integration guidelines and boundaries for companion skills.
- **Documentation Scaffold:** Organized documentation files with a root LICENSE and a `docs/` folder containing FEATURES.md and USAGE.md.
