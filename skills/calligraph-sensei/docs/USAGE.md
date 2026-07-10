# Calligraph Sensei — Usage Guide

This guide shows you how to interact with Calligraph Sensei, how its automatic intent routing operates, and what the output formats look like.

---

## Quick Start

You do not need to memorize commands. Just speak naturally:
```text
"Polish this paragraph and make it more engaging: [paste]"
```
Calligraph Sensei will automatically identify the intent, select the appropriate mode, and return the formatted output.

---

## Execution Workflows

Calligraph Sensei operates through three core workflows:

### Workflow A: Style Diagnosis (Audit Mode)
Analyzes a draft's sentence cadence (burstiness), vocabulary repetition (perplexity), AI cliché density, and active/passive voice ratio. It outputs a score table with specific recommendations.

### Workflow B: Style Forge & Refactoring (Rewrite Mode)
Applies targeted refactoring based on one of four style profiles (Creative, Academic-Formal, General, Conversational). Enforces sentence length variation, synonym substitution, and syntax pivots to eliminate AI patterns.

### Workflow C: Proofreading & Correction (Correction Mode)
Performs a conservative error-correction pass. Corrects typos, spelling errors, punctuation, and syntax while strictly disabling burstiness, perplexity shifts, and vocabulary changes, leaving the author's original voice intact.

---

## Automatic Intent Routing (Dispatcher)

When you submit a text, Calligraph Sensei inspects your prompt and automatically routes it:

1. **Proofreading Routing:** If the prompt contains error-correction keywords (e.g., *proofread, check grammar, fix spelling, typo, correct*), it runs **Workflow C**.
2. **Style Diagnosis Routing:** If the prompt contains audit keywords (e.g., *audit, diagnose, review style, check metrics*), it runs **Workflow A**.
3. **Explicit Style Routing:** If you name a specific style (e.g., *creative, formal, casual, academic*), it runs **Workflow B** using that profile.
4. **Default Routing:** If the prompt is generic (e.g., *humanise, make sound human, polish*), it runs a quick style scan and executes **Workflow B** under the **General/Non-fiction** profile.

---

## Full Output Examples

### 1. Style Diagnosis Example (Workflow A)

**Prompt:** `"Diagnose my writing: [paste text]"`

**Output:**
```text
### Calligraph Sensei: Writing Style Diagnosis

| Diagnostic Metric | Score / Finding | AI Risk Level | Observations |
|---|---|---|---|
| **Sentence Cadence** | SD = 1.4 | High | All sentences are between 12-14 words. Monotonous rhythm. |
| **AI Cliché Density** | 4 buzzwords found | High | Found overused terms: *delve, testament, tapestry*. |
| **Transition Style** | Formulaic | High | Paragraphs start with repetitive transitions: *Furthermore, Moreover*. |
| **Passive Voice Ratio**| 25% of sentences | Medium | Passive structures slow down the argument. |

#### Recommendations:
- Apply Creative/Fiction mode to vary sentence lengths and inject sensory detail.
- Run Academic-Formal to eliminate clichés while preserving rigorous structure.
```

### 2. Style Refactoring Example (Workflow B)

**Prompt:** `"Humanise this draft: It is important to note that the algorithm is efficient."`

**Output:**
```text
### Calligraph Sensei Review

**Style Mode Applied:** Non-fiction / General

#### Key Stylistic Adjustments:
| Paragraph | Original Sentence | Revised Sentence | Optimization Technique |
|---|---|---|---|
| 1 | "It is important to note that the algorithm is efficient." | "The algorithm runs fast — and it does so without memory overhead." | Cut filler opener and applied burstiness variation |

#### Polished Draft:
The algorithm runs fast — and it does so without memory overhead.
```

### 3. Proofreading Example (Workflow C)

**Prompt:** `"Proofread this paragraph: We has went to the store yesterday and buyed some apple's. It was a very importent task."`

**Output:**
```text
### Calligraph Sensei Proofread

**Style Mode Applied:** Proofreading / Correction

#### Grammar & Spelling Corrections:
| Paragraph / Section | Original Phrase | Corrected Phrase | Type of Issue Fixed | Explanation |
|---|---|---|---|---|
| 1 | "We has went to the store yesterday" | "We went to the store yesterday" | Grammar | Fixed auxiliary verb usage |
| 1 | "buyed" | "bought" | Grammar | Corrected irregular verb conjugation |
| 1 | "apple's" | "apples" | Punctuation | Removed errant possessive apostrophe from plural |
| 1 | "importent" | "important" | Spelling | Fixed typographical spelling error |

#### Corrected Draft:
We went to the store yesterday and bought some apples. It was a very important task.
```
