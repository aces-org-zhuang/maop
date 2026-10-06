# maop Agent Rules

## Language

Use the user's language for explanations. Keep code, commands, paths, and identifiers exact.

## Project Positioning

This repository is the maop AI engine and OpenCode capability surface for ACES projects. Development is centered on LLM capability enhancement: `.opencode/skills/`, OpenCode configuration, agent workflows, references, and governance documents. Host projects should consume maop through a Git submodule at `vendor/ai/maop` and bridge to maop-owned OpenCode assets instead of copying them.

## Development Rules

- Read the existing repository shape before changing files.
- Prefer the smallest correct change that preserves current ownership boundaries.
- Treat OpenCode skills and LLM capability files as first-class source, not auxiliary project metadata.
- Do not invent validation commands. Unknown commands must be recorded as `待补充` until confirmed by project configuration or the user.
- Do not place build outputs, caches, downloaded packages, or credentials in source-controlled paths.

## Reasoning First

Use `reasoning-map` before complex problem diagnosis, architecture changes, docs system changes, research workspace changes, submodule changes, or `.opencode` boundary changes.

## Architecture Modeling Rules

`architecture-design` owns architecture-as-code modeling with LikeC4. Its syntax is verified against a pinned LikeC4 version, not the latest official docs.

- LikeC4 is a **version-sensitive** tool. DSL features differ across releases. Before writing `.c4`, confirm the target version and read `architecture-design/references/03-dynamic-views.md` for the verified feature table.
- **Never write unverified syntax.** Features described in official docs may be unavailable in the pinned version; writing them makes `likec4 validate` fail.
- After any `.c4` change, run `likec4 validate`. Do not report completion on a non-zero exit code.
- When validation cannot run, report the reason, degraded evidence, and residual risk instead of claiming success.
- Pin the LikeC4 version exactly (no `^` ranges). Cross-version DSL behavior changes make CI non-reproducible.
- Host projects using `architecture-design` must configure the LikeC4 MCP server so agents can query the model instead of reading raw `.c4` text.

## Documentation Rules

- `docs/` stores stable project knowledge only.
- `guides/` stores non-research engineering process notes.
- Research process, papers, open source comparison, candidate materials, and evidence packages belong in `vendor/research/aces-research/`.
- New docs files must update the matching README or index.
- Reusable failure modes go under `docs/failure-modes/`.
- Complex debugging records go under `docs/debugs/`.
- Requirement-to-implementation evidence goes under `docs/evidences/`.

## Directory Responsibilities

- `.opencode/`: maop-owned OpenCode skills, package metadata, and engine-side capability files. This is a primary development surface.
- `docs/`: stable documentation, rules, indexes, decisions, and reusable records.
- `guides/`: short-lived or stage-specific non-research engineering notes.
- `vendor/`: external repositories and submodules, including the locked research workspace.
- `scripts/`: repeatable automation. Status: planned.
- `tests/`: cross-module tests. Status: planned.

## Common Commands

| Task | Command |
| --- | --- |
| Install OpenCode capability dependencies | `npm install --prefix .opencode` |
| Validate project OpenCode JSON | `node -e "JSON.parse(require('fs').readFileSync('.opencode/opencode.json','utf8')); console.log('ok')"` |
| List skills | `Get-ChildItem -Recurse -Filter SKILL.md .opencode/skills` |
| Validate LikeC4 models | `likec4 validate` (requires Node per pinned version) |
| Check LikeC4 formatting | `likec4 format --check` |
| Run automated tests | `待补充` |

## OpenCode Boundary

This repository owns maop's `.opencode/` capability surface. Project repositories that consume maop should create their own `.opencode/opencode.json` bridge to `../vendor/ai/maop/.opencode/skills` and register a `maop-opencode` reference. This repository must not copy maop assets into a separate host-project `.opencode` tree or add itself as `vendor/ai/maop`.
