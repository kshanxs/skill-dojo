# research-dojo — Features & Reference

**v1.1** · *Complete feature list, command reference, and skill architecture*

---

## The 7-Step Analytical Pipeline

The research-dojo skill guides the agent through seven distinct quality gates to evaluate any topic, claim, or plan:

### 1. Build the Map
Maps the domain topography by defining the core question, foundational concepts, common beginner misconceptions, key active debates, and critical unasked questions/blind spots.

### 2. Multi-Perspective Analysis
Evaluates the topic from six critical angles (by default: *Practitioner, Academic Researcher, Skeptic, Historian, Economist, Systems Thinker*).
* **Smart Substitution**: If the topic is highly specialized (e.g., pure mathematics, ethics, creative arts), the agent may dynamically swap up to two default perspectives for domain-specific ones (e.g., *Mathematician*, *Ethicist*, *Aesthetic Designer*, *Legal Expert*) to ensure a more relevant and rigorous analysis.

For each perspective, the agent details its main claim, strongest evidence, weakest assumption, and unique insights.

### 3. Contradiction Analysis
Identifies exactly where viewpoints collide, why they collide, and isolates whether these collisions stem from evidence conflicts or divergent values/incentives.

### 4. Evidence Audit & Grounding
Rigorously reviews claims by categorizing them into established facts, strong theories, and speculation. 
* **Active Grounding**: The agent performs targeted web searches to retrieve up-to-date peer reviews, conflicting datasets, or replication studies before auditing claims, ensuring confidence levels are backed by real-time evidence.
* Evaluates each claim's confidence level, supporting evidence, counter-evidence, and its falsifiability threshold.

### 5. Synthesis
Compiles a dual-depth summary: a 200-word beginner explanation, a 500-word expert analysis, a conceptual mental model, and outlines historical, practical, and future implications.

### 6. Stress Test
Adopts the persona of a hostile critic to challenge assumptions, expose weak evidence, and offer alternative explanations for the data.

### 7. Final Judgment
Renders the verdict on what is most likely true, what remains uncertain, common misunderstandings, practical takeaways, and prompts three high-value follow-up questions.

---

## Command Reference

| Command Phrase | What happens |
|---|---|
| `"I want to understand the topic: [TOPIC]"` | Initializes the 7-step analysis on the chosen topic |
| `"Run in interactive mode"` | Splices execution, pausing after Step 3 for user course-corrections |
| `"Run in one-shot mode"` | Executes all 7 steps in a single dense markdown response |
| `"Challenge the synthesis"` | Directly runs Step 6 (Stress Test) on an existing summary |
| `"Audit this claim: [CLAIM]"` | Evaluates a single specific claim using Step 4 guidelines |

---

## Repository Architecture

```
ResearchDojoProject/
│
├── README.md                    ← Main installation page
├── CHANGELOG.md                 ← Version release notes
├── LICENSE                      ← MIT License
│
├── docs/                        ← Repository documentation
│   ├── USAGE.md                 ← Usage examples and workflows
│   └── FEATURES.md              ← This file
│
└── research-dojo/               ← The core skill folder
    ├── SKILL.md                 ← Core agent instructions
    └── evals/
        └── evals.json           ← Test prompts for verification
```
