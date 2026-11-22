# Style Randomization Framework

## Purpose

Keep sentence patterns varied so the argument reads clearly. This framework defines the five sentence types and how to rotate them.

---

## The Five Sentence Types

### 1. Analytical
Explains reasoning, causality, or mechanism.
> "The performance of a neural network scales with both the quantity and diversity of its training data."

### 2. Causal
Shows a cause-and-effect relationship.
> "As the number of model parameters increases, the risk of overfitting to the training set also grows proportionally."

### 3. Comparative
Contrasts two approaches, systems, or concepts.
> "Unlike traditional rule-based classifiers, which rely on hand-crafted conditions, neural approaches derive their own decision boundaries from data."

### 4. Hypothetical
Explores a conditional or possible scenario.
> "Were training data perfectly balanced across all classes, the resulting model would likely produce more equitable predictions."

### 5. Observational
Describes a pattern, trend, or finding.
> "Empirical studies consistently demonstrate that ensemble methods outperform single-model approaches in classification benchmarks."

---

## Rotation Rule

Every paragraph must include **at least two different sentence types**.

**Bad (monotone):**
> "X is a process that does Y. X also does Z. X is important because of W."
> *(All analytical — repetitive to read)*

**Good (varied):**
> "X operates by doing Y [analytical]. As Y scales, Z becomes more prominent [causal]. Unlike traditional approaches, X does not require W [comparative]."

---

## Rhythm and Word Choice

Vary rhythm because it helps the reader. Do not aim at any detector score, and do not swap in rarer words for their own sake.

### Rule 1: Length Variation
When a paragraph's sentences all run the same length, join or split one where the logic allows.

**Bad (flat rhythm):**
> "Machine learning systems process large amounts of data efficiently. They identify patterns across many training examples. These patterns are then generalised to new inputs."
> *(All about the same length)*

**Better:**
> "Machine learning works by pattern recognition. Rather than encoding explicit rules, these systems derive their own decision logic from exposure to thousands of labelled examples — a process that makes them extraordinarily adaptable but equally dependent on the quality and diversity of the data they were trained on. This matters."
> *(Short. Very long. Short again.)*

### Rule 2: Precise Vocabulary
Use the plainest accurate word. Change a word only when the new one is more exact:
- "important" -> say what depends on it
- "utilize", "leverage" -> "use"
- "shows" stays "shows" unless "proves", "suggests", or "implies" is more accurate
- "problem" -> name the specific constraint or failure

### Rule 3: Qualifications Where They Belong
Place a real qualification where it limits the claim:
> "The algorithm, though efficient in most cases, degrades significantly when input distributions shift — a limitation that standard benchmarks rarely capture."

---

## Practical Application

When reviewing a paragraph:
1. Label each sentence by type
2. If 3+ consecutive sentences share a type → rewrite one using a different type
3. Check sentence length variation — if lengths are similar, break the longest into two or combine the shortest with its neighbour
4. Replace vague words with more exact ones, only where needed
5. Prefer embedded transitions — avoid "Furthermore", "Moreover", "In addition"
