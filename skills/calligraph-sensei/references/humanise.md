# Humanise Reference & Style Diagnosis Guide

Make text feel natural, engaging, and easy to read — as if crafted by a thoughtful human writer. Avoid over-engineering, robotic structures, and predictable transitions.

> **Note:** This reference is structured to mirror the Wikipedia "Signs of AI writing" pattern catalog. Section 1 covers detection metrics, Section 2 covers readability rules, Section 3 covers style modes, and Section 4 covers detection patterns you should check against your rewrite before delivery. Always run Section 4 against your output before declaring it done.

---

## 1. Standalone Power: Style Diagnosis Metrics

When conducting an independent style audit (`"Audit my writing"` or `"Diagnose this draft"`), Calligraph Sensei evaluates text against four statistical indices of human writing:

### A. Sentence Cadence (Burstiness Score)
- **What it measures:** The variation in sentence lengths within a paragraph.
- **AI Profile:** Extremely low variance (all sentences between 12-18 words; standard deviation < 2.0).
- **Human Profile:** High variance (mix of 3-word sentences and 30-word sentences; standard deviation > 8.0).
- **Diagnostic Rating:**
  - `Monotone (High AI Risk)`: Standard deviation of lengths is < 3.0.
  - `Balanced`: Standard deviation is between 3.0 and 7.0.
  - `Dynamic (Human-like)`: Standard deviation is > 7.0.

### B. AI Cliché Density
- **What it measures:** The presence of overused vocabulary and metaphors.
- **Banned/High-Risk AI Words:** *delve, tapestry, testament, beacon, navigate, showcase, paradigm, comprehensive, multifaceted, furthermore, moreover, it is important to note*.
- **Diagnostic Rating:**
  - `High Cliché Density`: 3 or more occurrences per 250 words.
  - `Clean`: 0 to 1 occurrences per 250 words.

### C. Transition Predictability
- **What it measures:** The placement and mechanical repetition of sentence starters.
- **AI Profile:** Relying heavily on beginning-of-sentence transitions (*Furthermore, Additionally, Consequently, Ultimately*).
- **Human Profile:** Relying on embedded mid-sentence transitions or simple conjunctions (*But, Also, And*).
- **Diagnostic Rating:**
  - `Formulaic`: Paragraph begins with repetitive transitions.
  - `Integrated`: Transitions are woven into the clauses.

### D. Passive Voice Ratio
- **What it measures:** Passive sentence structures where active subject-verb sequences would be punchier.
- **Diagnostic Rating:**
  - `Weak`: Passive structures exceed 20% of total sentences.
  - `Active`: Passive structures represent under 10% of total sentences.

---

## 2. General Readability Rules

Regardless of the writing mode, apply these core rules to clean up robotic AI habits:

### Rule A: Remove Filler Openers & Weak Connectors
Robotic writing relies on meta-discourse (talking about the writing). Cut them completely or start directly:
- "It is important to note that..." → (Remove)
- "It is worth mentioning that..." → "Worth noting:" or (Remove)
- "In order to..." → "To"
- "Due to the fact that..." → "Because"
- "As previously stated..." → (Remove)

### Rule B: Activate Key Sentences
Convert passive structures to active voice when the actor is clear. Active voice creates a sense of human agency:
- [Incorrect] "A narrative decision was made by the author to slow the pace."
- [Correct] "The author decided to slow the pace."

### Rule C: Ground Abstract Concepts
Replace abstract noun chains with concrete, relatable descriptions and analogies:
- [Incorrect] "The implementation of character development strategies yielded enhanced audience engagement."
- [Correct] "Developing characters with deep, secret flaws kept readers turning pages."

### Rule D: Let Punctuation Create Cadence
Humans use punctuation (dashes, colons, semicolons) to control breathing and emphasis. AI rarely does:
- "The scene was set — but the tension was missing."
- "She had one goal: escape."

> **Watch out:** One or two em dashes per paragraph is fine. **Three or more is the AI tell.** See Section 4.5.

---

## 3. Style-Specific Modes

Dynamically adjust style metrics depending on the requested mode:

### Mode 1: Creative / Fiction
Designed for novels, short stories, and narrative prose. Focuses on immersive, atmospheric, and character-driven language.
- **Sensory Detail:** Ground descriptions in the five senses (sight, sound, smell, taste, touch) rather than flat adjectives.
  - [Incorrect] "The weather was very cold and dark."
  - [Correct] "Frost patterns crawled up the windowpane, blocking out the gray afternoon light."
- **Show, Don't Tell:** Avoid summarising emotions. Show them through physical reaction and environmental detail.
  - [Incorrect] "He was extremely angry at the news."
  - [Correct] "He slammed the folder shut, the metal clips biting into his palm."
- **Narrative Cadence:** Rotate sentence length to match the action. Use short, sharp fragments for tension, and long, sensory clauses for reflection.
- **Diction:** Avoid repetitive AI verbs.

### Mode 2: Academic-Formal
Designed for essays, reports, and academic manuscripts. Focuses on rigorous, objective, and analytical expression without sounding robotic.
- **Strictly No Contractions:** Never use *don't, it's, can't, won't* etc.
- **Analytical Openings:** Avoid generic dictionary definitions or dramatic historical statements. Start with a precise problem formulation or academic context.
- **Objectivity & Hedging:** Express claims with appropriate qualification (*suggests, indicates, potentially, likely*) without weakening the thesis.
- **Sophisticated Flow:** Use embedded transitions rather than robotic, repeating block-connectors.

### Mode 3: Non-fiction / General (Default)
Designed for articles, blog posts, documentation, and essays. Focuses on clarity, impact, and engaging explanation.
- **The Analogy Rule:** Explain complex ideas using a single, clear analogy to ground the explanation.
- **Action-Oriented Verbs:** Keep verbs active and sentences direct.
- **Visual Scaffolding:** Emphasize logical structure with bullet lists, bold emphasis, and clear headings.

### Mode 4: Conversational / Casual
Designed for emails, Slack messages, social copy, and conversational blogging.
- **Permissive Contractions:** Use contractions freely to establish a warm, approachable tone.
- **Warmer Diction:** Use conversational transitions (*So, actually, look, in short, to be honest*).
- **Rhythmic Play:** Allow sentence fragments, conversational asides, and dashes to simulate natural speech patterns.

### Mode 5: Proofreading / Correction
Designed for final drafts where you want to fix all grammatical, spelling, and punctuation errors while strictly retaining the original author's voice, sentence structures, and vocabulary.
- **Zero Stylistic Alteration:** Explicitly disable burstiness rotation, sentence type rotation, and vocabulary perplexity substitutions. Keep the original words and sentence lengths exactly as they are.
- **Objective Error Correction:** Correct typos, spelling mistakes, punctuation errors (e.g. missing commas, incorrect apostrophes), and objective grammar issues (e.g. subject-verb agreement, incorrect verb tenses, dangling modifiers, incomplete fragments that are unintentional).
- **Explain and Diff:** Track and compile a list of all changes made to display in the final table (Original vs. Corrected, issue category, and brief explanation).

---

## 4. AI Signature Pattern Catalog (Detection Patterns)

**This section is the new addition (v1.1).** Inspired by the Wikipedia "Signs of AI writing" community guide, this is the explicit checklist you run against your output before delivery. If any pattern appears more than once per 250 words, fix it.

### 4.1 Inflated Symbolism
The "It's more than just X" construction. Common in marketing/essay writing.
- [Incorrect] "It's not just a button. It's a statement about accessibility."
- [Incorrect] "More than just a tool, it represents a paradigm shift."
- [Incorrect] "In a world where data drives decisions, this matters."
- **Fix:** Remove the symbolic framing. State what the thing does.

### 4.2 Promotional Language
List-bait adjectives that pad the prose. Either remove them or replace with concrete description.
- **Banned:** bustling, vibrant, thriving, groundbreaking, revolutionary, stunning, breathtaking, luminous, intricate, bold, imposing, dynamic, prominent, stark, vital, enduring.
- **Fix:** If you find yourself reaching for these, the sentence probably needs a fact instead of an adjective.

### 4.3 Superficial -ing Analyses
The "ensuring..., highlighting..., reflecting..." pattern, often paired with vague "broader trends".
- [Incorrect] "The new policy emphasizes transparency, ensuring stakeholder buy-in and showcasing the organization's commitment to broader industry trends."
- **Fix:** Cut the gerund chain. "The new policy requires quarterly transparency reports."

### 4.4 Vague Attributions
Citing nobody in particular to sound authoritative.
- [Incorrect] "Experts say...", "Industry reports suggest...", "Observers note..."
- [Incorrect] "Some critics argue...", "Many believe..."
- **Fix:** Either cite a specific source or remove the attribution. Hedging without a referent is noise.

### 4.5 Em Dash Overuse (Critical Pattern)
The single most common AI writing tell. AI uses em dashes the way humans use commas.
- **Rule:** Maximum two em dashes per paragraph in Modes 1-4. Zero in Proofreading mode.
- [Incorrect] "The result was unexpected — completely outside the model — which forced a rethink — and the team pivoted."
- **Fix:** Reserve em dashes for genuine mid-thought asides. Use commas, periods, or rewrite as two sentences for everything else.

### 4.6 Rule of Three
The "X, Y, and Z" tricolon. Humans use it too, but AI uses it in every list.
- **Rule:** Vary your list structures. Mix pairs, singles, fours, and prose fragments.
- [Incorrect] "fast, reliable, and efficient" / "innovation, inspiration, and integration" / "scalable, secure, and sustainable"
- **Fix:** "fast and reliable" sometimes. "Efficient enough for most teams" sometimes. Break the pattern.

### 4.7 AI Vocabulary (Extended List)
Beyond the Cliché Density list (Section 1.B), these words also signal AI:
- **Also flag:** foster, leverage (figurative), streamline, elevate, harness, underscores, profound, vibrant, enduring, robust, seamless, navigate (figurative), landscape (figurative), realm, in essence, ultimately, fundamentally.
- **Fix:** Use a more precise verb or just delete the word.

### 4.8 Negative Parallelisms
The "Not only X, but Y" / "Beyond being X, it's Y" construction.
- [Incorrect] "It's not just a feature. It's a philosophy."
- [Incorrect] "Beyond being a tool, it's a partner."
- **Fix:** Pick one. Either describe it as a feature or as a philosophy, don't inflate.

### 4.9 Generic Filler Openers
- [Incorrect] "At its core...", "At the heart of...", "In essence..."
- [Incorrect] "Ultimately, what this represents is..." (overuse of "ultimately")
- **Fix:** Start with the actual point.

### 4.10 Sycophantic Openings
When *you* (the assistant) are the one producing text that contains these, you're using AI patterns in your own message.
- [Incorrect] "Great question!", "That's a really interesting point!", "Certainly!", "Of course!"
- **Fix:** Just answer. No preamble agreement.

---

## 5. Personality & Soul (Add Voice, Not Just Remove Slop)

Removing AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop.

### Signs of soulless writing (even if technically "clean"):

- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

### How to add voice:

- **Have opinions.** "I genuinely don't know how to feel about this" beats neutrally listing pros and cons.
- **Vary your rhythm.** Short punchy sentences. Then longer ones that take their time getting where they're going.
- **Acknowledge complexity.** "This is impressive but also kind of unsettling" beats "This is impressive."
- **Use "I" when it fits.** First person isn't unprofessional. It's honest.
- **Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, half-formed thoughts are human.
- **Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

---

## 6. Workflow Discipline (The Final Check)

Before delivering any rewrite:

1. **Read the rewrite aloud.** If it sounds like a press release, keep going.
2. **Run the Section 4 detection checklist.** Mark any AI pattern you spot. Fix them.
3. **Ask: would a skeptical reader say "this was written by a person"?** If no, revise. Specifically look for soulless writing (Section 5).
4. **Verify semantic preservation.** Run the audit checklist from `audit_checklist.md`. Don't let style changes distort facts.
5. **Match register to medium.** A Slack message shouldn't sound like a journal article. A novel shouldn't sound like a blog post.

### When NOT to humanize

- Technical documentation where consistency matters more than voice
- Legal/contractual language (precision > personality)
- API references, schema docs, regex patterns
- The user explicitly wants the AI patterns (satire, parody, AI-detector testing)

---

## Sources

- Wikipedia: "Signs of AI writing" (WikiProject AI Cleanup)
- Pattern catalog adapted from `biostartechnology/humanizer` (clawhub)
- Burstiness and perplexity tuning original to Calligraph Sensei