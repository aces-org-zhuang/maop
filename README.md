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
| Delegation quality gate validation | `.opencode/skills/development-workflow/references/delegation-quality-gate-validation.md` |
| Research workspace plan | `vendor/research/README.md` |
| Submodule governance | `docs/02-development/submodules-index.md` |

## Top-Level Responsibilities

- `.opencode/`: maop-owned OpenCode skills, dependencies, and engine-side configuration surface.
- `docs/`: stable project knowledge, governance rules, indexes, and reusable records.
- `guides/`: non-research engineering process notes and temporary implementation records.
- `vendor/`: external repositories, research workspace, and long-lived third-party source references managed by Git submodule where applicable.
- `scripts/`: repeatable setup, validation, generation, migration, release, or diagnostic scripts. Status: planned.
- `tests/`: cross-capability tests. Status: planned; concrete layout depends on confirmed OpenCode capability validation needs.

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
