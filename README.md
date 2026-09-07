# maop

`maop` is the AI engine and OpenCode capability repository for ACES projects. Its primary development surface is LLM capability work: `.opencode/skills/`, OpenCode configuration, agent workflows, references, and governance documents.

This repository is initialized as a long-lived, LLM-maintainable codebase. Stable project knowledge belongs in `docs/`; non-research engineering notes belong in `guides/`; research work, papers, repository comparisons, and evidence packages belong in `vendor/research/aces-research/`.

## Quick Links

| Goal | Path |
| --- | --- |
| Project rules for agents | `AGENTS.md` |
| Stable documentation entry | `docs/README.md` |
| Development notes and commands | `docs/02-development/README.md` |
| OpenCode boundary | `.opencode/README.md` |
| Research workspace plan | `vendor/research/README.md` |
| Submodule governance | `docs/02-development/submodules-index.md` |

## Top-Level Responsibilities

- `.opencode/`: maop-owned OpenCode skills, dependencies, and engine-side configuration surface.
- `docs/`: stable project knowledge, governance rules, indexes, and reusable records.
- `guides/`: non-research engineering process notes and temporary implementation records.
- `vendor/`: external repositories, research workspace, and long-lived third-party source references managed by Git submodule where applicable.
- `scripts/`: repeatable setup, validation, generation, migration, release, or diagnostic scripts. The maintained `scripts/mcps/graphiti_mcp/` package is a first-class maop asset.
- `tests/`: cross-capability tests. Status: planned; concrete layout depends on confirmed OpenCode capability validation needs.

## Graphiti MCP Asset

`scripts/mcps/graphiti_mcp/` is maop's standalone MCP deployment boundary. It owns the package metadata, stdio MCP server, local smoke and health scripts, container files, and package tests. It is independent of Aces Desktop and must not read or depend on host-project runtime configuration.

The package currently exposes an in-process `memory` fallback only. It is not a Graphiti SDK integration, does not provide persistence or historical Graphiti compatibility, and must not be described as a real Graphiti provider until one is explicitly implemented and registered behind the package's provider interface.

Run and test instructions are maintained in `scripts/mcps/graphiti_mcp/README.md`.

## Sparse-Checkout Maintenance

The host checkout normally includes only `/.opencode/` and `/README.md`. To work on the Graphiti MCP asset, temporarily include `/scripts/mcps/graphiti_mcp/` in the maop sparse-checkout definition, then restore the normal patterns when finished. Keep the package's source, tests, and deployment files in that directory; do not copy them into the host project. Changes to the sparse-checkout patterns are checkout-local maintenance and are not committed as maop source files.

## Common Commands

This project is not a conventional application stack. Commands are tied to OpenCode capability development and the package metadata under `.opencode/`.

| Task | Command |
| --- | --- |
| Install OpenCode capability dependencies | `npm install --prefix .opencode` |
| Validate project OpenCode JSON | `node -e "JSON.parse(require('fs').readFileSync('.opencode/opencode.json','utf8')); console.log('ok')"` |
| List skills | `Get-ChildItem -Recurse -Filter SKILL.md .opencode/skills` |
| Run automated tests | `待补充` |

## Research Workspace

The locked research workspace is `vendor/research/aces-research` and points to `https://github.com/aces-org-zhuang/aces-research.git` as a submodule. Research materials are intentionally excluded from the default project documentation flow.

## AI Engine Boundary

This repository is itself the locked maop AI engine source (`https://github.com/aces-org-zhuang/maop.git`). Host projects should consume it as `vendor/ai/maop` with sparse-checkout for `.opencode/` and `README.md`; this repository should not add itself back as a nested `vendor/ai/maop` submodule.
