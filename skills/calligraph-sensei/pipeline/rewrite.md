# Rewrite & Diagnosis Pipeline Workflow

This pipeline executes stylistic refactoring, performs writing style audits (Style Diagnosis), and validates semantic preservation.

---

## Standalone Workflows

### Intent Routing (Dispatcher)
Before executing a workflow, analyze the user's prompt or target input:
1. **Proofreading Routing:** If the prompt matches proofreading keywords (*proofread, grammar, spelling, typo, correct, errors*), route to **Workflow C: Proofreading & Correction**.
2. **Style Diagnosis Routing:** If the prompt matches audit keywords (*audit, diagnose, review, check style*), route to **Workflow A: Style Diagnosis**.
3. **Explicit Style Routing:** If a specific tone or style is named (*creative, fiction, academic, casual, conversational*), route to **Workflow B: Style Forge & Refactoring** with that style mode.
4. **Default Routing:** If the prompt is generic (*humanise, make sound human, polish*), run a style scan and default to **Workflow B** using the **Non-fiction/General** mode.

---

### Workflow A: Style Diagnosis (Audit Mode)
When the user asks to "audit", "diagnose", or "check" a draft:
1. **Analyze:** Parse the text and calculate the metrics from `references/humanise.md` (Cadence standard deviation, AI Cliché frequency, Transition style, Passive ratio).
2. **Report:** Output the **Writing Audit Report** using the template below.
3. **Propose:** Recommend the specific style modes (e.g. Creative, Academic) that would resolve the flagged weaknesses.

---

### Workflow B: Style Forge & Refactoring (Rewrite Mode)
When rewriting a draft to apply style transformations:
1. **Calibrate:** Determine constraints (Medium, Intensity, Terminology Protection).
2. **Rewrite:** Apply style randomization (burstiness/perplexity) and humanize rules paragraph-by-paragraph.
3. **Audit:** Verify that code block syntax, proper nouns, citations, and annotations are preserved.
4. **Deliver:** Present the before/after comparisons and the polished manuscript.

---

### Workflow C: Proofreading & Correction (Correction Mode)
When correcting errors without modifying voice or style:
1. **Disable Style Shifts:** Set style randomization parameters (burstiness, perplexity tuning, sentence type rotation, vocabulary substitution) to **disabled**.
2. **Error Correction Scan:** Review each sentence of the draft to identify and fix typos, spelling errors, punctuation mistakes, and objective grammatical errors. Maintain original vocabulary and phrasing.
3. **Compile Correction Logs:** Maintain a record of every change made (original phrase, corrected phrase, issue type, and explanation).
4. **Audit:** Run `references/audit_checklist.md` to ensure proper noun protection, markdown consistency, and citation integration.
5. **Deliver:** Present the output using the **Proofreading Output Template**.

---

## Output Formats

### 1. Style Diagnosis Output Template
```text
### Calligraph Sensei: Writing Style Diagnosis

| Diagnostic Metric | Score / Finding | AI Risk Level | Observations |
|---|---|---|---|
| **Sentence Cadence** | SD = [X.X] | [High | Medium | Low] | Sentences are too uniform in length. |
| **AI Cliché Density** | [X] buzzwords found | [High | Medium | Low] | Found terms: *delve, tapestry*. |
| **Transition Style** | [Formulaic | Integrated] | [High | Medium | Low] | Relies heavily on sentence-starter blocks. |
| **Passive Voice Ratio**| [XX]% of sentences | [High | Medium | Low] | Excess passive verbs slow down the argument. |

#### Recommendations:
- Apply Creative/Fiction mode to vary cadence and inject sensory language.
- Run Academic-Formal to eliminate clichés while preserving rigorous structure.
```

### 2. Rewrite Output Template
```text
### Calligraph Sensei Review

**Style Mode Applied:** [Creative/Fiction | Academic-Formal | Non-fiction/General | Conversational/Casual]

#### Key Stylistic Adjustments:
| Paragraph | Original Sentence | Revised Sentence | Optimization Technique |
|---|---|---|---|
| 1 | "It is important to note that the algorithm is efficient." | "The algorithm runs fast — and it does so without memory overhead." | Cut filler opener & burstiness tuning |

#### Polished Draft:
[Insert the fully audited and revised draft here]
```

### 3. Proofreading Output Template
```text
### Calligraph Sensei Proofread

**Style Mode Applied:** Proofreading / Correction

#### Grammar & Spelling Corrections:
| Paragraph / Section | Original Phrase | Corrected Phrase | Type of Issue Fixed | Explanation |
|---|---|---|---|---|
| 1 | "We has checked the data." | "We have checked the data." | Grammar | Fixed subject-verb agreement |

#### Corrected Draft:
[Insert the cleaned, corrected draft here]
```
