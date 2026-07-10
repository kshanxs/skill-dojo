# Research Dojo

*The Adversarial Research & Synthesis Partner*

Structured mapping · Multi-perspective audits · Contradiction discovery · Rigorous synthesis · Stress testing

---

## Installation

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill research-dojo
```

### Update

```bash
npx skills update research-dojo
```

---

## Quick Start

Say this to initiate the process:
```text
"I want to understand the topic: [TOPIC]"
```

The AI will guide you through the analytical pipeline, mapping the concepts before synthesizing and challenging the findings.

**→ [Full usage guide with examples](docs/USAGE.md)**

---

## Highlights

| | |
|---|---|
| **Step-by-Step Scaffolding** | A disciplined 7-step analysis pipeline from initial map to final judgment |
| **High-Density Mapping** | Compact concepts, common misconceptions, and active debates |
| **Multi-Perspective Table** | Evaluates claims, evidence, and blind spots across 6 distinct domains |
| **Contradiction Auditing** | Identifies root causes of disagreements (data-driven vs. value-driven) |
| **Falsifiability Gating** | Audits evidence and defines what specific data would change the conclusion |
| **Dual-Depth Synthesis** | Generates both 200-word beginner and 500-word expert explanations |
| **Adversarial Stress Test** | A dedicated, hostile critique phase to actively dismantle the synthesis |

**→ [See all features and commands](docs/FEATURES.md)**

---

## Command Reference

| Command Phrase | What happens |
|---|---|
| `"I want to understand the topic: [TOPIC]"` | Initializes the 7-step analysis on the chosen topic |
| `"Run in interactive mode"` | Pauses after Step 3 for user course-corrections |
| `"Run in one-shot mode"` | Executes all 7 steps in a single dense response |
| `"Challenge the synthesis"` | Directly runs Step 6 (Stress Test) on an existing summary |
| `"Audit this claim: [CLAIM]"` | Evaluates a single specific claim using Step 4 guidelines |

---

## Package Structure

```text
skills/research-dojo/
├── SKILL.md                 ← Agent instructions and workflow rules
├── evals/
│   └── evals.json           ← Test prompts for verification
└── docs/
    ├── USAGE.md              ← Detailed user examples and workflows
    └── FEATURES.md           ← Comprehensive feature reference
```

---

## Companion Skills

Research Dojo is Phase 0 of the three-skill pipeline:

1. **Research Dojo (Phase 0):** Stress-test claims, map debates, audit evidence, and produce verified synthesis notes.
2. **[TrueDraft](../truedraft/README.md) (Phase 1):** Feed Research Dojo's audited output into TrueDraft's `notes_first` mode for structured, polished drafting.
3. **[Calligraph Sensei](../calligraph-sensei/README.md) (Phase 2):** Apply final style refinement or conservative proofreading to the completed manuscript.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version release details.
