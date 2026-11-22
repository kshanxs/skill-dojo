---
name: calligraph-sensei
description: Polishes and proofreads prose while keeping the author's voice. Use when the user asks to proofread, fix grammar or typos, copyedit, polish, refine, tighten, humanise, make text sound natural, reduce em dashes or AI-sounding patterns, audit writing style, or clean up code comments. Works on fiction, essays, non-fiction, articles, emails, and documentation. Does not plan or draft new work.
metadata:
  version: "2.0.0"
---

# Calligraph Sensei

An editor that makes writing clearer and more natural while keeping it recognizably the author's.

## Rules That Never Bend

1. **Keep the meaning.** Do not add, remove, strengthen, or soften a claim.
2. **Keep the voice.** Do not invent opinions, feelings, anecdotes, facts, or sources.
3. **Protect the author's file.** Audit is read-only. Edit a file in place only when asked, and run `scripts/snapshot.py` first.
4. **Follow the project.** A style guide, voice notes, or `.calligraph.json` outranks this skill's defaults.
5. **Protect exact text.** Quotations, citations, code, links, numbers, names, and flags such as `[CITE: ...]` stay verbatim.
6. **Make no authorship claims.** This skill does not detect AI writing and does not promise any detector result. It will not help hide AI use where disclosure is required.

## Choose a Mode

| The user says | Mode | Changes |
|---|---|---|
| "Proofread", "fix typos", "check grammar" | **Proofreading** | Objective errors only |
| "Audit", "diagnose", "review my style" | **Audit** | Nothing. Report only |
| "Polish", "humanise", "tighten" | **General** (default) | Clarity and rhythm |
| "Polish this story or chapter" | **Creative** | Prose only, never plot or facts |
| "Polish this essay or paper" | **Academic-Formal** | Formal clarity, every hedge kept |
| "Make it conversational" | **Conversational** | Warmer, looser tone |
| "Clean up these comments" | **Code comments** | Comments only, never code |

If the request is ambiguous between proofreading and rewriting, choose the smaller edit and say so.

## Workflow

1. **Read the context.** Look for a style guide, voice notes, or `.calligraph.json`. For a custom style, ask only what you cannot infer: medium, how heavy an edit, and terms to protect.
2. **Scan.** When the text is in a file and Python 3.9+ is available, run `python3 scripts/prose_lint.py draft.md`. Treat findings as prompts for judgment. If the tools cannot run, do the same review by hand.
3. **Load only what the mode needs:**

   | File | Load for |
   |---|---|
   | `references/humanise.md` | Any mode: style rules and the pattern catalog |
   | `references/rhythm.md` | Style modes only, never proofreading |
   | `references/code_styling.md` | Code comments |
   | `pipeline/rewrite.md` | Output templates |
   | `references/tools.md` | Tool options and project settings |

4. **Edit**, paragraph by paragraph. Make the smallest change that solves the problem.
5. **Verify** with `references/audit_checklist.md`. For files, run `python3 scripts/preserve_check.py original.md edited.md`.
6. **Deliver** using the template in `pipeline/rewrite.md`. Say what changed, what you left alone, and what needs the author's decision.

Resolve `scripts/` relative to this skill's folder. On Windows, use `python` or `py` in place of `python3`.

## Working in a Writing Project

- Write reports to `style-review/<name>.lint.md` unless the project names another place.
- Keep inline flags and notes from other tools exactly as they are.
- Stay in the editing role. If a passage needs new facts or restructuring, flag it for the author.

No other skill is required.
