# SOP - Consolidating Workflow Skills

Use this SOP when a user wants to merge many repeated, overlapping, or project-specific skills into a smaller set of high-cohesion workflow skills.

## Goal

Create fewer, clearer skills without losing the useful operating knowledge that accumulated in the original skills.

## Classification

Separate source material into four buckets before writing anything:

1. General capability: reusable across projects, suitable for `SKILL.md`, SOPs, templates, or checklists.
2. Project-specific constraint: useful only for one repository, team, directory layout, workflow tool, naming scheme, or runtime. Move to a reference pattern or project docs, not hard rules.
3. Runtime/tool side effect: any state change outside the repository, asynchronous service state, external observability, resume state owned by a service, or write operation against an external service. Document as adapter behavior; do not let a static skill claim it can perform the side effect unless the current environment exposes a real tool and the user authorizes it.
4. Existing maop capability: if an existing skill already owns the domain, reference or lightly extend it instead of creating a parallel skill.

## Consolidation Steps

1. Inventory existing skills and map their trigger descriptions, outputs, required tools, and hidden assumptions.
2. Identify the smallest number of workflow-level domains that are meaningful to users. Prefer 2-4 workflow skills over one giant skill or many atomic skills.
3. Check maop first: if `research`, `expression-delivery`, `project-init-manager`, `submodule-manager`, or another existing skill owns a domain, keep that boundary.
4. Write each new `SKILL.md` as a short router: first steps, Stage Router, resource index, delivery standards, and explicit non-goals.
5. Move phase-level instructions into numbered `references/sop-NN-<feature>.md` files.
6. Move project-specific source-system behavior into `references/pattern-*.md` or `references/adapter-*.md`.
7. Add evals that test routing boundaries, especially adjacent cases that should trigger existing maop skills instead.

## Design Checks

- A new skill must have a crisp user-facing job, not just a former agent name.
- Do not hard-code source project directory names, score thresholds, stage counts, agent names, or plugin tools unless the skill is explicitly for that source project.
- Do not weaken existing maop skills by duplicating their domain inside a new workflow skill.
- If the user asks for 90%+ confidence, use `references/self-test-confidence.md` after the draft exists.

## Output

Deliver a consolidation map:

```text
新增技能:
- <skill>: owns <domain>

扩展既有技能:
- <skill>: add <reference/bridge>

复用不改:
- <skill>: called when <condition>

降级为 pattern/adapter:
- <source behavior>: why not hard rule
```
