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
- After any `.c4` change, run `likec4 validate` when a CLI is available. Do not report completion on a non-zero exit code.
- When validation cannot run, report the reason, degraded evidence, and residual risk instead of claiming success.
- Pin the LikeC4 version exactly (no `^` ranges) **when a CLI is used**. Cross-version DSL behavior changes make CI non-reproducible.
- Host projects using `architecture-design` must configure the LikeC4 MCP server so agents can query the model instead of reading raw `.c4` text.

## Architecture Language Rules

Architecture diagrams are read by people doing review, not by compilers. **Default to Chinese for all human-facing text.**

- Chinese: element display names, view titles, `description`, relationship labels, deployment node names.
- English: identifiers only (element id, view id). These become export filenames and share URL paths, so renaming them breaks existing links.
- Keep as-is: technical proper nouns such as `RAGFlow`, `LLM Wiki`, `Node.js`, `HTTP`, `JSON`, `API`, file paths, and ports. Translating them lowers readability.
- A project-level design repo needs **no** `likec4.config.ts`; LikeC4 scans `src/` directly. Only aggregation layers need one, to scope sources explicitly and avoid merging multiple projects' specification kinds and top-level element names.

## Environment Adaptation Rules

`architecture-design/references/04b-environment-and-sync.md` governs capability probing and degradation. The core rule: **a missing local likec4 install is never a reason to stop delivery.**

- `@likec4/mcp` bundles its own LikeC4 kernel and runs via `npx` with zero installation and no host Node version constraint. Model queries, dependency lookups, and impact analysis therefore work in any environment.
- Only `validate`, `build`, `serve`, and `export` need a local CLI. Probe in order: MCP -> local CLI -> `npx` on demand -> read-only degradation.
- In read-only degradation, still deliver the model files. State plainly that `likec4 validate` did not run, why, and what unvalidated syntax risk remains. Never fabricate a passing validation.
- **Distinguish environment failures from model defects.** `EBADENGINE`, `ERR_MODULE_NOT_FOUND`, and network errors are environment problems; `Invalid` with a line number is a model problem. Never report one as the other.
- For synchronized review: MCP watch reloads model changes without a restart, and `likec4 serve` gives a hot-reloading browser preview. Changing `opencode.json` still requires restarting opencode; changing model files does not.

## Design Repo Rules

Host project initialization provisions architecture-as-code through a design repo, coordinated by `project-init-manager/references/sop-10-design-workspace.md`.

- Design repo is **conditionally required**, not unconditional. Required when the project has external system integrations, deployment topology, or multiple collaborating modules. Skipped for single-module scripts and one-off tools.
- **One repo per project.** Never let multiple projects reference the same design repo: the gitlink records the sub-repo HEAD commit, so every design commit forces an unrelated PR in every referencing repo.
- **Do not sparse-checkout a design repo.** Unlike `vendor/ai/maop`, a design repo needs a full working tree for `likec4 validate` and `build`; partial checkout breaks cross-file `include` resolution.
- `build_entry` is `none`. The host repo never builds the design repo; that runs in the design repo's own CI.
- Content that must land in the same PR as code stays in the host repo `docs/`. A design repo carries architecture assets that outlive any single PR.
- A global aggregation repo may publish cross-project views, but no host repo references it via submodule.

## Architecture Handoff Rules

`architecture-design` hands architecture to implementation via `architecture-design/references/06-architecture-handoff.md`. The positioning matters and must not drift:

- **Architecture does not derive code.** A model answers *what exists, where it lives, how it connects*. Implementation answers *how it behaves, whether it is correct*. Business rules, boundary conditions, and interface signatures cannot be inferred from topology, so the skill produces **no executable code** and makes no "architecture is development" claim.
- **The value is removing duplicate analysis.** Implementation should not have to re-derive components, dependency direction, and deployment constraints. That is what the handoff spec eliminates.
- **The handoff spec is a subset, not a replacement.** It fills the architecture-facing part of `technical-design`'s Handoff Mini-Spec. Interface contracts, data structures, and business rules remain `technical-design`'s responsibility.
- **Facts come from the model, not memory.** Query via MCP (`read-project-summary`, `subgraph-summary`, `query-incomers-graph`, `query-outgoers-graph`, `read-deployment`). Every spec entry must cite a model element id or view id; entries without a citable basis are marked `待补充`, never invented.
- **Confidence must be justified.** Below 90% on any key architectural conclusion blocks a ready declaration and requires listing the gap and the verification action.
- **A stale model means a stale handoff.** After a model change, the design repo must ship and the host repo's submodule pointer must be updated before the spec is handed off.

## Handoff Consumption Rules

A produced spec that nobody reads is not a handoff. These rules make the consumer side explicit.

- **The spec lives in the design repo** at `handoff/current.md`, never in the host repo's `docs/`. It is a derivative of the model and must ship in the same commit; splitting them allows a spec describing one architecture to be read against a model describing another. Host `docs/` carries rules and indexes.
- **`technical-design` reuses, never re-derives.** Before architecture confirmation, read the spec and take component boundaries and dependency direction from it. Fill only interfaces, data structures, business rules, and state machines.
- **`implementation-delivery` treats the spec as a constraint.** When code disagrees with it, stop and report. Do not bend code to match reality, and do not edit the spec.
- **Both consumers treat a missing spec as normal.** It means no architecture reuse is available, not an error. It must not block pure implementation work.
- **Both consumers check staleness.** If the model commit recorded in the spec differs from the host repo's pinned gitlink, the spec is expired and must not be used to justify new architecture.
- **`development-workflow` triggers the architecture node on conditions, not judgement.** New component, dependency direction change, deployment change, or an undefined integration/data boundary routes to `architecture-design` before `technical-design`. Expressing a diagram alone stays with `expression-delivery`.
- **The chain is verified end to end, not half.** A change to this flow is not done until a real spec has been produced from a real model and discovered at the documented path.

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
