# Research Dojo — Usage Guide

> You do not need to memorize any commands. Just talk naturally. This guide shows you what is possible and exactly what the conversation looks like.

---

## Quick Start

```
"I want to understand the topic: [TOPIC]"
```

When you query a topic, the agent activates the Research Dojo pipeline.

---

## Execution Modes

To prevent output token limits and keep the analysis deep, the dojo offers two execution modes:

### 1. Interactive Mode (Recommended)
The agent executes the process in stages. It generates Steps 1–3 (Map, Perspectives, and Contradictions), then pauses for your review. This lets you refine the map and correct any errors before the agent builds the synthesis and stress-tests it.

### 2. One-Shot Mode
The agent generates all 7 steps in a single response. To fit within token budgets, the output will be formatted highly densely (using bullet points and tables).

---

## Full Example — Interactive Mode

### Phase 1: Mapping & Landscaping (Steps 1–3)

**You:** `"I want to understand the topic: Universal Basic Income (UBI). Let's run in interactive mode."`

**AI:**
```markdown
# Research Dojo: Universal Basic Income (UBI)

## STEP 1 — BUILD THE MAP
* Core Question: Can a state guarantee a lifetime financial floor to all citizens unconditionally without triggering inflation or labor collapse?
* Important Concepts: Means-testing, Net Transfer, Marginal Tax Rate, Labor Elasticity, Monetary Velocity.
* Misconceptions: "Free money for all" (it is a net redistribution scheme; higher earners pay it back in taxes).
* Key Debates: Funding mechanisms (VAT vs. Income Tax) and UBI vs. Universal Basic Services (UBS).
* Blind Spots: Real-world scaling. Most pilots are temporary, preventing general equilibrium observations.

## STEP 2 — MULTI-PERSPECTIVE ANALYSIS
| Perspective | Main Claim | Strongest Evidence | Weakest Assumption | Unique Insight |
|---|---|---|---|---|
| Practitioner | overhead is reduced | Alaska Permanent Fund admin | baseline systems can be fully dismantled | marginal tax trap reduction |
| Academic | cash improves agency | GiveDirectly data | short-term behavior matches long-term | cognitive bandwidth gains |
| Skeptic | fiscally impossible | national cost math | standard debt taxes are only option | market rent increases absorb cash |
...

## STEP 3 — CONTRADICTION ANALYSIS
* Friction Areas: Viability (Skeptics vs. Systems Thinkers) and Labor drops (Academics vs. Economists).
* Root Causes: Static accounting vs. dynamic modeling.
* Value Conflicts: Efficiency/incentives vs. equity/stability.

---
I have mapped the landscape and contradictions. Shall we proceed to the Evidence Audit and Synthesis (Steps 4–5), or do you want to adjust any parts of the map first?
```

**You:** `"The map looks good. Let's proceed, but make sure to address housing supply elasticity in the evidence audit."`

**AI:**
```markdown
## STEP 4 — EVIDENCE AUDIT
* Established Facts: Means-testing creates marginal tax traps. Cash transfers improve wellness.
* Strong Theories: UBI reduces labor supply slightly, mostly for secondary earners.
* Speculation: A national UBI would cause hyper-inflation.

* Claim: UBI is captured by landlords.
  * Confidence: Medium.
  * Support: Basic supply-demand curves in highly inelastic housing markets.
  * Counter: Rent controls or construction deregulation can mitigate captures.
  * Falsifiability: Real-world rent indexes post-UBI showing no anomalous rise.

## STEP 5 — SYNTHESIS
* Beginner Explanation: (200 words summarizing cash, funding, and debates...)
* Expert Explanation: (500 words detailing NIT equivalence, marginal tax rates, and macroeconomics...)
* Mental Model: The Trampoline (baseline bounce that remains beneath you, unlike a tangled safety net).
...
```

---

## Tips

* **Be Specific with the Topic:** Instead of "AI," ask about "The impact of generative AI on software engineering employment."
* **Challenge the Critique:** If the Step 6 Stress Test attacks a conclusion you think is solid, argue back. The dojo will audit your counter-arguments.
* **Combine with Data:** You can upload PDFs or text notes and say: `"I want to understand this topic: [Topic]. Here is a research paper to audit: [Path]"`
