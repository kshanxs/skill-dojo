# Calligraph Sensei

*The Universal Stylistic Refactoring & Readability Assistant*

Five custom modes · Burstiness and perplexity tuning · Semantic preservation checks · Zero conflict coexistence with TrueDraft

---

## Installation

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill calligraph-sensei
```

### Update

```bash
npx skills update calligraph-sensei
```

---

## Quick Start

Say this to initiate the process:
```text
"Humanise this draft: [paste text]"
```
The AI will automatically scan the writing cadence, select the appropriate mode, and refactor the prose.

**→ [Full usage guide with templates and examples](docs/USAGE.md)**

---

## Highlights

| | |
|---|---|
| **Five Output Modes** | Creative, Academic-Formal, Non-fiction/General, Conversational/Casual, and conservative Proofreading |
| **Cadence Control** | Simulates human burstiness by varying sentence structures and lengths using the 10-30-5 rule |
| **Perplexity Tuning** | Disrupts AI detectors by replacing high-probability words with low-frequency human synonyms |
| **Automatic Routing** | Automatically detects and dispatches your request to proofreading or specific style refactoring |
| **Audit Checks** | Enforces a strict semantic preservation checklist to protect proper nouns and code block executability |

**→ [See all features and commands](docs/FEATURES.md)**

---

## Command Reference

| Command Phrase | What happens |
|---|---|
| `"Humanise this: [paste]"` | Runs the polisher using the default General style |
| `"Polish this novel draft: [paste]"` | Activates Creative/Fiction mode |
| `"De-risk this essay: [paste]"` | Activates Academic-Formal mode |
| `"Make this more conversational: [paste]"` | Activates Conversational/Casual mode |
| `"Proofread this: [paste]"` | Activates Proofreading/Correction mode |
| `"Refactor the comments in this code: [paste]"` | Polishes code comments while protecting code blocks |

---

## Package Structure

```text
skills/calligraph-sensei/
├── SKILL.md                 ← Agent instructions and workflow rules
├── evals/
│   └── evals.json           ← Test prompts for verification
├── pipeline/
│   └── rewrite.md           ← Dispatching and templates
├── references/
│   ├── audit_checklist.md   ← Semantic checks
│   ├── code_styling.md      ← Comments polishing
│   ├── humanise.md          ← Style profiles and AI detection catalog
│   └── style_randomization.md ← Perplexity and burstiness
└── docs/
    ├── USAGE.md              ← Detailed user examples and templates
    └── FEATURES.md           ← Comprehensive feature reference
```

---

## Companion Skills

Calligraph Sensei operates in harmony with the other skills in this suite:

1. **[TrueDraft](../truedraft/README.md):** Structures assignments, enforces outline checkpoints, and manages citations. Calligraph Sensei handles pure style polishing of the drafts under Academic-Formal mode.
2. **[Research Dojo](../research-dojo/README.md):** Stress-tests claims and maps academic debates. Calligraph Sensei refines the final prose output after Research Dojo's evidence audit.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version release details.
