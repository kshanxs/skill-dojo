# Changelog

This file records suite-level changes that affect multiple skill packages, repository policy, or cross-skill compatibility.

Package-specific history belongs in each skill's own changelog:
- [Calligraph Sensei changelog](skills/calligraph-sensei/CHANGELOG.md)
- [TrueDraft changelog](skills/truedraft/CHANGELOG.md)
- [Research Dojo changelog](skills/research-dojo/CHANGELOG.md)

## v2.0.0 — 2026-11-22

Coordinated release: [Research Dojo v2.0.0](skills/research-dojo/CHANGELOG.md), [Calligraph Sensei v2.0.0](skills/calligraph-sensei/CHANGELOG.md), and [TrueDraft v1.3.0](skills/truedraft/CHANGELOG.md).

### Changed

- **Breaking:** Removed project-specific integrations. Skills now connect through [generic interfaces](docs/architecture.md#generic-interfaces).
- **Breaking:** Removed AI-detector evasion triggers and claims across the suite.
- Rewrote the README and refreshed all documentation.

### Added

- Dependency-free fact-checking and prose tools, with a test suite calibrated on public-domain text.
- `scripts/validate-structure` now checks frontmatter, versions, links, file references, skill independence, and standard-library-only imports.
- [Third-party notices](THIRD_PARTY_NOTICES.md).

## v1.0.0 — 2026-07-10

### Added

- Established the Skill Dojo repository as the central home for all writing skills.
- Imported [Calligraph Sensei v1.1.0](skills/calligraph-sensei/README.md) — full source tree including SKILL.md, pipeline, references, evals, and documentation.
- Imported [TrueDraft v1.2.0](skills/truedraft/README.md) — full source tree including SKILL.md, pipeline, references, examples, assets, and documentation.
- Added [Research Dojo v1.3.0](skills/research-dojo/README.md) — full source tree including SKILL.md, evals, and documentation.
- Created suite-level documentation: [architecture](docs/architecture.md), [installation](docs/installation.md), and [release policy](docs/releases.md).
- Added repository structure validation script (`scripts/validate-structure`).
- All skill installation commands point to `kshanxs/skill-dojo` as the single source.
