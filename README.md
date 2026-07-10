<div align="center">

<br>

# ✦ Skill Dojo ✦

### *The Central Hub for Research, Drafting, and Writing Skills*

*Composable AI skills · Independent versioning · Interlinked documentation · One install source*

<br>

[![License](https://img.shields.io/badge/License-MIT-2ea043?style=for-the-badge&labelColor=161b22)](./LICENSE)
[![Docs](https://img.shields.io/badge/Docs-Architecture-f78166?style=for-the-badge&labelColor=161b22)](./docs/architecture.md)
[![Install](https://img.shields.io/badge/Install-npx_skills_add-0d1117?style=for-the-badge&labelColor=161b22)](./docs/installation.md)

<br>

*Skill Dojo is a version-controlled repository housing independent, composable AI writing skills.*
*Each skill can be installed and used standalone, but they are designed to work together seamlessly.*

</div>

---

## The Suite

| Skill | Focus |
|---|---|
| [Calligraph Sensei](skills/calligraph-sensei/README.md) | Writing refinement, proofreading, readability, and AI detection mitigation |
| [TrueDraft](skills/truedraft/README.md) | Structured academic drafting, citation-aware workflows, and originality rewriting |
| [Research Dojo](skills/research-dojo/README.md) | Adversarial claim review, debate mapping, evidence auditing, and research synthesis |

Each skill has its own [SKILL.md](skills/calligraph-sensei/SKILL.md), [changelog](skills/truedraft/CHANGELOG.md), [documentation](skills/truedraft/docs/FEATURES.md), and semantic version. They release independently.

---

## Installation

Install any skill directly from this repository:

```bash
# Calligraph Sensei — style polishing and proofreading
npx skills add https://github.com/kshanxs/skill-dojo --skill calligraph-sensei

# TrueDraft — academic drafting and originality
npx skills add https://github.com/kshanxs/skill-dojo --skill truedraft

# Research Dojo — adversarial research and synthesis
npx skills add https://github.com/kshanxs/skill-dojo --skill research-dojo
```

**→ [Full installation guide](docs/installation.md)**

---

## The Three-Phase Pipeline

The skills are designed to operate independently, but they connect as a sequential pipeline when all three are installed:

```text
Phase 0                    Phase 1                    Phase 2
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│ Research Dojo│    →     │  TrueDraft   │    →     │  Calligraph  │
│              │          │              │          │    Sensei     │
│ Stress-test  │          │ Structure    │          │ Polish style │
│ claims, map  │          │ the draft,   │          │ and readabi- │
│ debates, and │          │ manage cita- │          │ lity, run    │
│ audit sources│          │ tions, and   │          │ proofreading │
│              │          │ rewrite for  │          │ or humanise  │
│              │          │ originality  │          │ the prose    │
└──────────────┘          └──────────────┘          └──────────────┘
     Evidence                 Manuscript               Polished output
     & synthesis              & audit log              & correction log
```

Each handoff is optional. Every skill operates independently when its input is supplied directly by the user.

**→ [Architecture and skill boundaries](docs/architecture.md)**

---

## Documentation

| Document | Scope |
|---|---|
| [Architecture and skill handoffs](docs/architecture.md) | Skill boundaries, the three-phase pipeline, and handoff contracts |
| [Installation guide](docs/installation.md) | Per-skill installation, updates, and suite-wide setup |
| [Release and versioning policy](docs/releases.md) | Independent versioning, changelog conventions, and Git tag policy |
| [Suite changelog](CHANGELOG.md) | Cross-skill and suite-level history |

### Per-Skill Documentation

| Skill | README | Features | Usage | Changelog |
|---|---|---|---|---|
| Calligraph Sensei | [README](skills/calligraph-sensei/README.md) | [Features](skills/calligraph-sensei/docs/FEATURES.md) | [Usage](skills/calligraph-sensei/docs/USAGE.md) | [Changelog](skills/calligraph-sensei/CHANGELOG.md) |
| TrueDraft | [README](skills/truedraft/README.md) | [Features](skills/truedraft/docs/FEATURES.md) | [Usage](skills/truedraft/docs/USAGE.md) | [Changelog](skills/truedraft/CHANGELOG.md) |
| Research Dojo | [README](skills/research-dojo/README.md) | [Features](skills/research-dojo/docs/FEATURES.md) | [Usage](skills/research-dojo/docs/USAGE.md) | [Changelog](skills/research-dojo/CHANGELOG.md) |

---

## License

This project is licensed under the [MIT License](LICENSE).

Copyright © 2026 [Shubhanshu Shukla](https://github.com/kshanxs). All rights reserved.

---

<p align="center">
  <sub>MIT License &nbsp;•&nbsp; Permission to Modify & Distribute &nbsp;•&nbsp; No Warranty or Liability</sub><br>
  <sub>Independent skills, one repository. Research, draft, and polish with confidence.</sub>
</p>
