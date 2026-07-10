# Semantic Preservation & Style Audit Checklist

Before delivering the rewritten prose, run a strict checklist to verify that style enhancements did not compromise the accuracy, truth, or technical integrity of the text.

---

## The Six-Stage Audit

### Check 1: Zero Semantic Drift (Factual Preservation)
Compare the original paragraph with the rewritten paragraph.
- **Assertion:** Did the rewrite add any new claims, assumptions, or evidence? Did it drop any critical details?
- **Action:** If the rewrite introduced minor logical shifts or expanded the scope of a claim, revert the sentence and rephrase it closer to the original argument.

### Check 2: Technical & Proper Noun Integrity
Verify that all domain-specific vocabulary is preserved.
- **Assertion:** Are proper nouns, brand names, product titles, equations, variables, database fields, and math operators unchanged?
- **Action:** Ensure synonyms were not applied to specialized terms (e.g., do not rewrite "Random Forest" to "Arbitrary Woods").

### Check 3: Markdown & Structural Elements
Verify that layout syntax is intact.
- **Assertion:** Are all headers (`#`, `##`), bold tags (`**`), bullet formatting, table columns, and hyper-links preserved?
- **Action:** Restore any formatting tags that were stripped or restructured during writing.

### Check 4: AI Signature Elimination
Audit the output paragraph for mechanical patterns. Run the detection checklist from `references/humanise.md` Section 4.
- **Assertion:** Are there any repeating sentence starters? Are sentence lengths too uniform? Are there overused transitions?
- **Action:** If three consecutive sentences are of similar length, split one or combine two. Remove remaining robotic transitions (*Furthermore, Moreover, Additionally*). Check specifically for: em dash overuse (max 2 per paragraph), rule of three patterns, negative parallelisms, promotional adjectives, vague attributions, and sycophantic openings.

### Check 5: Companion Skill Annotations Protection
Verify compatibility with other skills.
- **Assertion:** Are TrueDraft inline notations (`💡 Learning note:`, `[CITE: ...]`, standard APA/IEEE references) and Book Writer structures preserved verbatim?
- **Action:** Re-inject any citation data or learning callouts that were modified.

### Check 6: Personality & Soul (v1.1)
Verify the rewrite doesn't read as sterile, voiceless prose.
- **Assertion:** Does the rewrite have opinions, varied rhythm, specific feelings, or first-person where appropriate? Or does it read like a press release?
- **Action:** If the rewrite is technically "clean" but has no voice, run a second pass against `references/humanise.md` Section 5 (Personality & Soul). Add the human details that make the prose feel lived-in.

---

## Output Requirement

Every rewrite delivery must include:

1. The Style Diagnosis table (if audit was requested).
2. The Before/After comparison table with technique used.
3. The polished draft.
4. **A note on any detection patterns fixed** (which AI tells were caught and removed).

The note on detection patterns makes the audit transparent and teaches the user what to watch for in their own writing.