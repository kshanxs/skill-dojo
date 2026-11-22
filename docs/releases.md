# Release Policy

## Independent Package Versions

Each skill has its own semantic version and changelog:

| Skill | Version | Changelog |
|---|---|---|
| [Calligraph Sensei](../skills/calligraph-sensei/README.md) | 2.0.0 | [CHANGELOG.md](../skills/calligraph-sensei/CHANGELOG.md) |
| [TrueDraft](../skills/truedraft/README.md) | 1.3.0 | [CHANGELOG.md](../skills/truedraft/CHANGELOG.md) |
| [Research Dojo](../skills/research-dojo/README.md) | 2.0.0 | [CHANGELOG.md](../skills/research-dojo/CHANGELOG.md) |

The version lives in each `SKILL.md` under `metadata.version` and must match the newest changelog entry. `scripts/validate-structure` checks this.

Use semantic versioning:

- `PATCH` for corrections that preserve documented behavior.
- `MINOR` for backward-compatible features or workflow additions.
- `MAJOR` for breaking trigger, interface, behavior, or compatibility changes.

## Changelogs

Keep package releases in `skills/<skill>/CHANGELOG.md`. The root [CHANGELOG.md](../CHANGELOG.md) is reserved for:

- Shared validation or governance changes
- Cross-skill handoff contracts
- Coordinated package releases
- Repository-wide compatibility or security fixes

## Before a Release

```bash
python3 scripts/validate-structure
python3 -m unittest discover -s tests
```

## Git Tags

Create a root Git tag only for a suite milestone or coordinated release. For independently released packages, use namespaced tags such as `truedraft-v1.3.0` or `calligraph-sensei-v1.2.0`.

## Related Documentation

- [Architecture and skill handoffs](architecture.md): skill boundaries and interfaces
- [Installation guide](installation.md): per-skill installation and updates
- [Suite changelog](../CHANGELOG.md): suite-level history
- [Root README](../README.md): overview and quick start
