# Style Randomization Framework

Bypass mechanical AI signatures and pattern detectors by introducing statistical variety: **Perplexity** (vocabulary unpredictability) and **Burstiness** (sentence length variation).

---

## 1. Sentence Type Rotation

AI text tends to stick to a single sentence type (usually analytical or descriptive). Humans naturally rotate between diverse structural forms. 

Rotate among these five sentence structures across every paragraph:

| Sentence Type | Functional Purpose | Example |
|---|---|---|
| **Analytical** | Explains mechanism, logic, or reason. | *The system processes parameters sequentially to prevent collision.* |
| **Causal** | Links a cause to an effect directly. | *As workload increases, execution latency spikes proportionally.* |
| **Comparative** | Contrasts two elements or systems. | *Unlike traditional rule engines, neural models infer patterns dynamically.* |
| **Hypothetical** | Explores conditional or "what-if" scenarios. | *Were training data perfectly clean, prediction bias would drop.* |
| **Observational** | Details empirical trends or raw observations. | *Empirical testing consistently highlights a bottle-neck in I/O operations.* |
| **Narrative/Active** | Drives action or subjective perspective. | *We tested the compiler limits and hit a memory wall.* |

**Rotation Rule:** Every paragraph must feature **at least two** different sentence structures. Never place three analytical or observational sentences back-to-back.

---

## 2. Burstiness Simulation (Length Variation)

AI writes in monotonously medium-length sentences (~12 to 18 words). Human writing is highly variable (bursty): a massive, clause-rich sentence followed immediately by a short punchy fragment.

### The 10-30-5 Rule
In every major paragraph of prose, ensure you include:
1. At least one sentence **under 10 words** (for impact).
2. At least one sentence **over 25 words** (for complex logic or descriptive atmosphere).
3. A middle sentence of standard length (12-18 words).

**Example Comparison:**
- [Incorrect] **Low Burstiness (Robotic):**
  > "Neural network training requires high compute resources. GPUs process matrix multiplications very fast. This speed is necessary for large parameter weights. Optimizers then update weights to reduce losses."
  *(Lengths: 7 words, 7 words, 7 words, 7 words. Extremely flat rhythm.)*
- [Correct] **High Burstiness (Human-like):**
  > "Training neural networks is computationally expensive. Because large-scale models feature billions of parameter weights, matrix multiplications must be processed in parallel across thousands of GPU cores — a resource-heavy pipeline that has made hardware scaling a primary bottleneck in modern AI research. But it works."
  *(Lengths: 6 words, 34 words, 3 words. Bursty, dynamic cadence.)*

---

## 3. Perplexity Tuning (Vocabulary Unpredictability)

AI models choose the most statistically probable token. To humanize text, we must introduce selective, precise, low-probability synonyms and structures.

### Lexical Substitution
Replace common AI transition words and overused adjectives with precise, lower-frequency synonyms:

| [Incorrect] High-Probability AI Word | [Correct] Precise Human Synonym |
|---|---|
| *important / crucial* | *consequential, non-trivial, pivotal, salient* |
| *shows / highlights* | *surfaces, illustrates, underscores, maps* |
| *problem / issue* | *constraint, tension, pathology, friction* |
| *use / utilize* | *deploy, leverage, execute, harness* |
| *different / diverse* | *dissimilar, divergent, distinct, variable* |
| *testament to* | *evidence of, reflects, mirrors* |
| *tapestry / beacon* | (Remove entirely or rewrite the metaphor) |

### Mid-Sentence Pivots
Break predictable linear syntax by injecting a qualifying clause or dash in the middle of a sentence:
- [Incorrect] "The parser extracts text from the document and puts it into markdown."
- [Correct] "The parser extracts the document text — regardless of formatting errors — before structuring it as markdown."
