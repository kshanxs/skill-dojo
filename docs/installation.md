# Installation

All skills are installed from this repository using the `npx skills` CLI.

## Per-Skill Installation

### Calligraph Sensei

Proofreading and voice-preserving polish.

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill calligraph-sensei
```

- [Skill README](../skills/calligraph-sensei/README.md)
- [Features reference](../skills/calligraph-sensei/docs/FEATURES.md)
- [Usage guide](../skills/calligraph-sensei/docs/USAGE.md)

### TrueDraft

Structured academic drafting and citation-aware workflows.

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill truedraft
```

- [Skill README](../skills/truedraft/README.md)
- [Features reference](../skills/truedraft/docs/FEATURES.md)
- [Usage guide](../skills/truedraft/docs/USAGE.md)

### Research Dojo

Fact, date, and source checking, plus adversarial research synthesis.

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill research-dojo
```

- [Skill README](../skills/research-dojo/README.md)
- [Features reference](../skills/research-dojo/docs/FEATURES.md)
- [Usage guide](../skills/research-dojo/docs/USAGE.md)

## Install All Skills

Each skill is independent. To install all three:

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

## Requirements

The skills work as plain instructions in any agent that supports Agent Skills. The optional helper scripts in Research Dojo and Calligraph Sensei need Python 3.9 or newer and no packages. On Windows, run them with `python` or `py` in place of `python3`.

## Related Documentation

- [Architecture and skill handoffs](architecture.md): skill boundaries and interfaces
- [Release and versioning policy](releases.md): how versions and changelogs work
- [Suite changelog](../CHANGELOG.md): suite-level history
- [Root README](../README.md): overview and quick start
