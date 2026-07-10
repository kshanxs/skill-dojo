# Installation

All skills are installed from this repository using the `npx skills` CLI.

## Per-Skill Installation

### Calligraph Sensei

Style polishing, proofreading, readability, and AI detection mitigation.

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill calligraph-sensei
```

- [Skill README](../skills/calligraph-sensei/README.md)
- [Features reference](../skills/calligraph-sensei/docs/FEATURES.md)
- [Usage guide](../skills/calligraph-sensei/docs/USAGE.md)

### TrueDraft

Structured academic drafting, originality rewriting, and citation-aware workflows.

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill truedraft
```

- [Skill README](../skills/truedraft/README.md)
- [Features reference](../skills/truedraft/docs/FEATURES.md)
- [Usage guide](../skills/truedraft/docs/USAGE.md)

### Research Dojo

Adversarial claim review, debate mapping, evidence auditing, and research synthesis.

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill research-dojo
```

- [Skill README](../skills/research-dojo/README.md)
- [Features reference](../skills/research-dojo/docs/FEATURES.md)
- [Usage guide](../skills/research-dojo/docs/USAGE.md)

## Install All Skills

To install the full suite at once:

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill calligraph-sensei
npx skills add https://github.com/kshanxs/skill-dojo --skill truedraft
npx skills add https://github.com/kshanxs/skill-dojo --skill research-dojo
```

## Updating

Update any installed skill to its latest version:

```bash
npx skills update calligraph-sensei
npx skills update truedraft
npx skills update research-dojo
```

## Related Documentation

- [Architecture and skill handoffs](architecture.md) — skill boundaries and the three-phase pipeline
- [Release and versioning policy](releases.md) — how skill versions and changelogs work
- [Suite changelog](../CHANGELOG.md) — cross-skill and suite-level history
- [Root README](../README.md) — suite overview and quick start
