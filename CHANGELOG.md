# Changelog

This file records suite-level changes that affect multiple skill packages, repository policy, or cross-skill compatibility.

Package-specific history belongs in each skill's own changelog:
- [Calligraph Sensei changelog](skills/calligraph-sensei/CHANGELOG.md)
- [TrueDraft changelog](skills/truedraft/CHANGELOG.md)
- [Research Dojo changelog](skills/research-dojo/CHANGELOG.md)

## v1.0.0 — 2026-07-10

### Added

- Established the Skill Dojo repository as the central home for all writing skills.
- Imported [Calligraph Sensei v1.1.0](skills/calligraph-sensei/README.md) — full source tree including SKILL.md, pipeline, references, evals, and documentation.
- Imported [TrueDraft v1.2.0](skills/truedraft/README.md) — full source tree including SKILL.md, pipeline, references, examples, assets, and documentation.
- Added [Research Dojo v1.3.0](skills/research-dojo/README.md) — full source tree including SKILL.md, evals, and documentation.
- Created suite-level documentation: [architecture](docs/architecture.md), [installation](docs/installation.md), and [release policy](docs/releases.md).
- Added repository structure validation script (`scripts/validate-structure`).
- All skill installation commands point to `kshanxs/skill-dojo` as the single source.
