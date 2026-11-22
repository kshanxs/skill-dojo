<div align="center">

# 🥋 Skill Dojo

**Small, independent AI skills for research, drafting, and editing.**

[![License: MIT](https://img.shields.io/badge/License-MIT-2ea043)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/tools-Python_3.9+-3776ab)](docs/installation.md#requirements)
[![No dependencies](https://img.shields.io/badge/dependencies-none-8957e5)](docs/architecture.md#independence-rules)

</div>

## The Skills

| | Skill | What it does |
|---|---|---|
| 🔬 | **[Research Dojo](skills/research-dojo/README.md)** | Checks facts, dates, and sources in non-fiction |
| 🖋️ | **[Calligraph Sensei](skills/calligraph-sensei/README.md)** | Polishes and proofreads prose while keeping your voice |
| 📝 | **[TrueDraft](skills/truedraft/README.md)** | Plans and drafts academic work, with honest citations |

Install only what you need. No skill depends on another.

## Install

```bash
npx skills add https://github.com/kshanxs/skill-dojo --skill research-dojo
npx skills add https://github.com/kshanxs/skill-dojo --skill calligraph-sensei
npx skills add https://github.com/kshanxs/skill-dojo --skill truedraft
```

Then just ask:

```text
Fact-check this draft: chapter-3.md
Proofread this, but don't change my style
Help me plan an essay on climate adaptation
```

## What You Can Count On

- ✅ **Nothing is called verified unless a source was actually checked.**
- 🔒 **Your text is safe.** Checks are read-only, and edits to a file start with a snapshot.
- 🎙️ **Your voice stays.** Your style guide and notes outrank the skill's defaults.
- 🪶 **No setup.** The helper tools need only Python, and the skills still work without it.

## Works With Your Workflow

Use one skill or chain them. Everything passes through plain Markdown and predictable report files, so the skills fit any long-form writing setup.

```text
🔬 Research  →  📝 Draft  →  🖋️ Polish
```

## Docs

[Architecture](docs/architecture.md) · [Installation](docs/installation.md) · [Releases](docs/releases.md) · [Changelog](CHANGELOG.md) · [Third-party notices](THIRD_PARTY_NOTICES.md)

## License

[MIT](LICENSE) © 2026 [Shubhanshu Shukla](https://github.com/kshanxs)
