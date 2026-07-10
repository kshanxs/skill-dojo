# Changelog

All notable changes to the `calligraph-sensei` skill will be documented in this file.

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
- **Synergy & Boundaries:** Established integration guidelines and boundaries for TrueDraft and Book Writer companion skills.
- **Documentation Scaffold:** Organized documentation files with a root LICENSE and a `docs/` folder containing FEATURES.md and USAGE.md.
