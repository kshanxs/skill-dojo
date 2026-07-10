---
name: calligraph-sensei
description: |
  Polish, humanise, or proofread any pasted text, draft, or document. Triggers when the user asks to humanise, polish, refine, rewrite, de-risk, sound less like AI, remove AI signatures, bypass AI detectors, audit writing style, check prose, fix grammar/typos, or polish code comments and docstrings. Use for creative fiction, academic essays, non-fiction articles, conversational copy, or code comments. Five modes: Creative, Academic-Formal, Non-fiction/General, Conversational/Casual, Proofreading. Does NOT structure assignments or plan narratives (delegate those to TrueDraft or Book Writer).
---

# Calligraph Sensei

Universal writing style polisher, humanizer, and AI detection mitigation assistant. Transforms dry, robotic, or overly structured text into flowing, natural prose. Works as a companion to drafting tools and as a standalone writing diagnostics engine.

---

## Context Efficiency Rule (Lazy Loading)

**Read this before loading reference files.**

This skill contains specialized guides to avoid context window bloat. Do NOT pre-load all references. Use **lazy loading**. Only read a reference file when performing its specific workflow stage:

| Load this file... | When... |
| :--- | :--- |
| `references/humanise.md` | Selecting style modes, applying detection patterns, or running style diagnosis. |
| `references/style_randomization.md` | Executing burstiness and perplexity tuning to break repetitive AI patterns. |
| `references/code_styling.md` | Polishing prose inside code comments, docstrings, or programming documentation. |
| `references/audit_checklist.md` | Running the final semantic preservation audit. |
| `pipeline/rewrite.md` | Executing the rewrite pass, Style Forge, and outputting diagnostics. |

Never load more than 1–2 reference files at a time.

---

## Command Reference

| Say this... | What happens |
|---|---|
| `"Humanise this: [paste]"` / `"Make this sound human"` | Runs the polisher on the pasted text using the default General style. |
| `"Polish this novel draft / story: [paste]"` | Activates Creative/Fiction mode. Enhances description, pace, and sensory detail. |
| `"De-risk this essay: [paste]"` | Activates Academic-Formal mode. Retains formal tone, removes flags. |
| `"Make this draft more conversational: [paste]"` | Activates Conversational/Casual mode. Warmer tone, friendlier voice. |
| `"Refactor the comments in this code: [paste]"` | Polishes code comments and docstrings while protecting code blocks. |
| `"Proofread this: [paste]"` / `"Check for grammar/spelling errors: [paste]"` | Activates Proofreading/Correction mode. Fixes objective errors while keeping the original voice. |
| `"Audit my writing: [paste]"` / `"Diagnose this draft"` | Runs Style Diagnosis only. Outputs a Writing Audit Report without rewriting. |

---

## Standalone Power: Style Forge & Diagnosis

### A. The Style Diagnosis (On-Demand Writing Audit)
When the user asks to "audit", "diagnose", or "review" their text, analyze:
1. **Sentence Cadence (Burstiness):** Standard deviation of sentence lengths. Low variance means robotic.
2. **Lexical Uniformity (Perplexity):** Frequency of statistically overused words and robotic transitions.
3. **AI Signature Clichés:** Presence of telltale AI buzzwords (e.g., *delve, tapestry, testament, beacon, navigate*).
4. **Structural Monotony:** Check if consecutive sentences share identical structural forms.

### B. The Style Forge (Interactive Calibration)
If the user wants custom styling, run a quick 3-question calibration before rewriting:
1. *"What is the target medium (creative novel chapter, technical paper, marketing blog, code comments)?"*
2. *"What tone level do you want (Light, Standard, High/Conversational)?"*
3. *"Are there technical keywords or proper nouns we must protect from vocabulary optimization?"*

If the user pastes text and asks for an immediate rewrite, skip onboarding and run the rewrite using the default General style.

---

## Synergy & Boundaries with Companion Skills

To prevent overlapping instructions and resource contention in shared workspaces:

1. **TrueDraft Boundary:**
   TrueDraft is the owner of assignment structure, interactive onboarding, outline checkpoints, and scholarly citations.
   **Calligraph Sensei** is strictly a style, readability, and flag-mitigation layer.
   *Conflict Resolution:* If the user asks for layout structuring, rubric targeting, or citation lookup, call or recommend `truedraft`. If polishing academic text written by TrueDraft, preserve all citations, bibliography links, and inline annotations (e.g., `Learning note`).

2. **Book Writer Boundary:**
   Book Writer is the owner of novel chapters, narrative pacing, character briefs, and world-building.
   **Calligraph Sensei** only polishes drafted prose to enhance sensory detail or sentence flow.
   *Conflict Resolution:* If the user asks to restructure character arcs or write new chapters from scratch, recommend `book-writer-skill`.

3. **General Principle:**
   Calligraph Sensei supports five specialized modes, dynamically calibrated to match human writing profiles and editing needs:

| Mode | Style Description | Primary Purpose |
|---|---|---|
| Creative / Fiction | Sensory imagery, deep character/narrative voice, emotional beats, flowing varied sentence lengths. | Novels, stories, narrative non-fiction |
| Academic-Formal | Analytical precision, objective terminology, sophisticated sentence rhythms, zero informal contractions. | Essays, research, reports, submissions |
| Non-fiction / General | Active verbs, clear arguments, vivid explanatory analogies, engaging transitions. | Articles, documentation, general copy |
| Conversational / Casual | Natural contractions, warmer tone, friendly voice, short punchy cadences. | Slack, emails, blogs, personal messages |
| Proofreading / Correction | Objective grammatical correction, spelling/typo repairs, punctuation fixes, zero changes to voice or style. | Clean up draft mistakes while retaining the author's precise voice |

---

## Core Workflows

### 1. Ingestion & Analysis
Read the pasted text or target file. Perform a style scan (Sentence Cadence, AI Buzzwords, Passive Voice).

### 2. Mode Selection & Lazy Loading
Load `references/humanise.md` and select the appropriate mode (using **Automatic Intent Routing**):
- Creative/Fiction
- Academic-Formal
- Non-fiction/General (Default if unspecified)
- Conversational/Casual
- Proofreading/Correction

If in a style mode (Modes 1-4), load `references/style_randomization.md` for AI signature mitigation (perplexity/burstiness). If in Proofreading mode (Mode 5), DO NOT load style randomization. If polishing code, load `references/code_styling.md`.

### 3. Execution (The Style Pass)
Load `pipeline/rewrite.md`. Rewrite the target text by applying readability enhancements, rhythm variation, and lexical perplexity.

**Strict Terminology & Syntax Protection:** Protect all code backticks, HTML tags, equations, citations, and markdown header structures. Do not edit proper nouns or technical terms.

### 4. Semantic Preservation Audit
Load `references/audit_checklist.md`. Compare the original and rewritten sentences. Verify zero semantic drift or factual distortion. If any technical meaning was lost, revert that section and rewrite with a tighter alternative.

### 5. Personality & Voice Pass (v1.1)
Before delivery, re-read your rewrite against `references/humanise.md` Section 5 (Personality & Soul) and Section 4 (Detection Patterns). Ask: would a skeptical reader say this was written by a person? If not, revise.

### 6. Delivery
Output the style diagnosis, the Before/After comparison table, and the polished draft.

---

## What Changed in v1.1

- **Detection Patterns Section** in `references/humanise.md` (Section 4). Pulled from the Wikipedia "Signs of AI writing" community guide. Covers inflated symbolism, promotional language, em dash overuse, rule of three, negative parallelisms, sycophantic openings, and more.
- **Personality & Soul Section** (Section 5) so rewrites don't become sterile technical exercises.
- **Workflow Discipline** (Section 6) with explicit "When NOT to humanize" guidance.
- **Trimmed SKILL.md frontmatter** to a tighter trigger description (under 200 words) for better loading accuracy.
- **Reduced em dash density** in the SKILL.md body itself. (Yes, we were using the AI tell we sell the cure for.)