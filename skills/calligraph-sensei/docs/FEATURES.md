# Calligraph Sensei — Features & Reference

**v1.1** · *Complete feature list, command reference, and style architecture*

---

## The Five Specialized Modes

Calligraph Sensei adapts its styling logic based on the requested writing mode:

### 1. Creative / Fiction
Designed for novels, short stories, and narrative prose. Focuses on immersive, sensory-rich language.
* **Sensory Detail:** Grounds descriptions in the five senses rather than relying on abstract adjectives.
* **Show, Don't Tell:** Exposes emotions through physical actions, body language, and environmental details rather than flat statements.
* **Narrative Pacing:** Rotates sentence structures to match narrative action (short sentences for tension, flowing clauses for reflection).

### 2. Academic-Formal
Designed for essays, reports, research papers, and manuscripts. Focuses on analytical rigor and objective tone.
* **No Contractions:** Strictly avoids informal contractions.
* **Hedging & Objectivity:** Evaluates claims with appropriate academic qualifications (e.g., *suggests, indicates, potentially, likely*).
* **Sophisticated Cadence:** Embeds clause transitions rather than repeating mechanical block starters.

### 3. Non-fiction / General (Default)
Designed for articles, documentation, blogs, and marketing copy. Focuses on clarity, impact, and audience engagement.
* **Analogy Integration:** Explains complex technical topics using concrete, real-world analogies.
* **Active Verb Density:** Converts passive structures into active voice to drive energy and directness.
* **Visual Scaffolding:** Organizes logic with clean heading hierarchies and bullet formats.

### 4. Conversational / Casual
Designed for emails, Slack messages, social copy, and blog commentary. Focuses on a warm, approachable voice.
* **Permissive Contractions:** Integrates contractions freely to mirror natural human speech.
* **Warm Transitions:** Employs friendly, spoken transitions (e.g., *so, actually, look, in short, to be honest*).
* **Speech Cadence:** Integrates conversational asides, fragments, and dashes to simulate spoken rhythms.

### 5. Proofreading / Correction
Designed for final drafts where you want to fix errors without altering the writer's style or vocabulary.
* **Zero Style Shifts:** Disables all perplexity, burstiness, and word substitution rules.
* **Objective Correction:** Scans for and corrects spelling mistakes, typos, punctuation errors, and clear grammatical slips (e.g., subject-verb agreement, incorrect verb conjugations).
* **Correction Log:** Compiles a table detailing every fix, complete with the original snippet, the corrected version, and the explanation.

---

## Anti-AI Detection Engine (Originality metrics)

The skill optimizes prose against the statistical thresholds that detectors (e.g., Turnitin, Copyleaks, GPTZero) classify as "robotic":

### 1. Perplexity Tuning (Vocabulary Unpredictability)
AI models choose the most statistically probable next token. Calligraph Sensei breaks this by injecting precise, low-probability synonyms and structures:
* **Lexical Substitution:** Replaces overused AI words (e.g., *important, crucial, delve, showcase, testament*) with precise, lower-frequency human synonyms (e.g., *salient, pivotal, examine, illustrate, evidence of*).
* **Mid-Sentence Pivots:** Inserts qualifying clauses or dashes in the middle of sentences to disrupt linear syntax.

### 2. Burstiness Simulation (Length Variation)
AI writes in a flat rhythm (sentence lengths between 12-18 words). Calligraph Sensei enforces the **10-30-5 Rule**:
* Ensure each major paragraph contains at least one sentence under 10 words, one sentence over 25 words, and a middle sentence of standard length (12-18 words).

### 3. Sentence Type Rotation
Prevents consecutive sentences from sharing the same grammatical form. The engine rotates among **Analytical, Causal, Comparative, Hypothetical, Observational, and Active/Narrative** sentence types.

### 4. Semantic Preservation Audit
Runs a final checklist (`references/audit_checklist.md`) to verify that no semantic drift, factual change, or proper noun modification occurred during refactoring.

---

## v1.1 Additions: Detection Catalog + Personality Pass

### 5. AI Signature Detection Catalog (new in v1.1)
An explicit pattern checklist you can audit your rewrite against before delivery. Covers the 14 AI writing tells documented on Wikipedia's "Signs of AI writing" page:

* **Em dash overuse** — max 2 per paragraph in style modes, 0 in proofreading
* **Rule of three** — vary list structures (pairs, singles, fours)
* **Negative parallelisms** — "It's not just X. It's Y."
* **Inflated symbolism** — "More than just a tool, it represents..."
* **Promotional language** — bustling, vibrant, groundbreaking, etc.
* **Vague attributions** — "Experts say...", "Industry reports suggest..."
* **Superficial -ing analyses** — ensuring, highlighting, showcasing
* **Sycophantic openings** — "Great question!", "Certainly!"
* **Generic filler** — "At its core", "Ultimately", "Fundamentally"
* And more — see `references/humanise.md` Section 4 for the full list

### 6. Personality & Soul Pass (new in v1.1)
Removing AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop. v1.1 adds explicit guidance on adding voice, opinions, varied rhythm, specific feelings, and first-person perspective where appropriate. See `references/humanise.md` Section 5.

### 7. Workflow Discipline (new in v1.1)
The final meta-check before delivery: would a skeptical reader say "this was written by a person"? Plus an explicit list of cases where you should NOT humanize (technical docs, legal language, API references, etc).

---

## Command Reference

| Command Phrase | What happens |
|---|---|
| `"Humanise this: [paste]"` / `"Make this sound human"` | Runs the polisher using the default General style. |
| `"Polish this novel draft / story: [paste]"` | Activates the Creative/Fiction mode to enhance pacing. |
| `"De-risk this essay: [paste]"` | Activates the Academic-Formal mode (retains formal tone). |
| `"Make this draft more conversational: [paste]"` | Activates the Conversational/Casual mode. |
| `"Refactor the comments in this code: [paste]"` | Polishes code comments while protecting code blocks. |
| `"Proofread this: [paste]"` / `"Check for grammar/spelling errors: [paste]"` | Activates Proofreading/Correction mode to fix objective errors while keeping your precise voice. |
