# TrueDraft

*The Originality-First Academic Writing Assistant*

Calibrated onboarding · Constraint-gated planning · Humanise readability · Search-first academic citations

---

## Installation

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill truedraft
```

### Update

```bash
npx skills update truedraft
```

---

## Quick Start

```text
"Start a new assignment on machine learning"
"Write a 1200-word draft on climate adaptation"
"Use these notes to write my literature review"
"Refine this draft so it sounds less formulaic"
"Solve this Python homework and analyze complexity"
"Explain as you go / Start learning mode"
```

The AI guides you through setup one question at a time. Every question is skippable.

**→ [Full usage guide with examples](docs/USAGE.md)**

---

## Highlights

| | |
|---|---|
| **The Assignment Forge** | 9-question interactive onboarding (rubrics, citation style, constraints) |
| **Originality-First Rewrite** | Sentence variety and precise wording to break formulaic phrasing |
| **Source Divergence Scan** | Pre-drafting check blacklisting canonical examples and stock analogies |
| **Search-First Citation Engine** | Uses host search tools to locate real papers; strictly defaults to placeholders on search fail |
| **Humanise Readability** | Three levels (Light / Standard / Conversational) with before/after sentence audits |
| **Inline Learning Mode** | Teaches academic structure as it writes using `💡 Learning note:` annotations |
| **CS & Data Science Discipline** | Calibrated hybrid prose-code workflows with Big-O complexity checks and algorithm diversity |
| **Project Memory Bank** | Auto-maintained profiles and audit logs in `project-memory/` |

**→ [See all features and specifications](docs/FEATURES.md)**

---

## Command Reference

| Say this | What happens |
|---|---|
| `"Start a new assignment"` | Launches the Assignment Forge onboarding |
| `"Write my assignment on [topic]"` | Onboarding → Plan → Outline Gate → Draft → Rewrite → Audit |
| `"Reduce similarity in this draft: [paste]"` | Executes the Originality pass and returns a comparison table |
| `"Humanise this"` / `"Make this easier to read"` | Readability pass with standard intensity level |
| `"Make this more conversational"` | Readability pass with high (Conversational) intensity level |
| `"Solve this programming task"` | Launches CS/Data Science hybrid prose-code workflow |
| `"Explain as you go"` / `"Learning mode"` | Activates inline teaching notes explaining structural and lexical choices |

---

## Package Structure

```text
skills/truedraft/
├── SKILL.md                 ← Agent instructions and workflow rules
├── assets/
│   └── templates/           ← Output templates
├── examples/                ← Reference outputs for each input mode
│   ├── open_generation_example.md
│   ├── notes_first_example.md
│   ├── draft_rewrite_example.md
│   ├── coding_assignment_example.md
│   └── ml_project_report_example.md
├── pipeline/                ← Stage-specific workflow instructions
│   ├── forge.md             ← Interactive onboarding
│   ├── plan.md              ← Thesis and argument planning
│   ├── outline.md           ← Structure and approval gate
│   ├── draft.md             ← First draft generation
│   ├── coding.md            ← CS/data-science workflows
│   ├── rewrite.md           ← Originality and readability
│   └── audit.md             ← Final citation and delivery audit
├── references/              ← Style, citation, and discipline guides
│   ├── academic_rules.md
│   ├── citation_guide.md
│   ├── citation_policy.md
│   ├── grammar.md
│   ├── humanise.md
│   ├── learning_mode.md
│   ├── review_checklist.md
│   ├── rubric_guide.md
│   ├── style_randomization.md
│   └── disciplines/         ← Subject-area calibrations
└── docs/
    ├── USAGE.md              ← Detailed user examples
    ├── FEATURES.md           ← Comprehensive feature reference
    └── superpowers/specs/    ← Design specifications
```

---

## Companion Skills

TrueDraft works seamlessly with the other skills in this suite:

1. **[Research Dojo](../research-dojo/README.md) (Phase 0):** Stress-test claims, map active academic debates, audit evidence, and build a high-density concept map before drafting.
2. **[Calligraph Sensei](../calligraph-sensei/README.md) (Phase 2):** Run writing audits, a voice-preserving polish, or a conservative Proofreading pass on the final manuscript.

---

## Limitations & Responsibility

- **No Plagiarism Measurement:** TrueDraft improves originality through process discipline. It does not check external databases or guarantee a similarity score.
- **Source Verification:** Always review citations in `audit_log.md` and resolve any `[CITE: ...]` placeholders before submitting.
- **Institutional Alignment:** Ensure your use aligns with the academic integrity policy of your institution.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for details on all versions and releases.
