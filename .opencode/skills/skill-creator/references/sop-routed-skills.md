# SOP-Routed Skill Structure

Use this pattern for workflow skills, repository governance skills, multi-stage implementation skills, and any skill whose real behavior spans several phases or decision branches.

## Goal

Keep `SKILL.md` as a routing and orientation layer. Put concrete execution steps in SOP or reference files, then make the skill progressively guide the model to read only the next relevant file.

This avoids skills becoming confusing all-in-one documents and makes the execution path easier for an LLM to follow.

## Recommended Layout

```text
skill-name/
  SKILL.md
  references/
    sop-00-intake.md
    sop-01-<stage>.md
    sop-02-<stage>.md
    sop-03-validation.md
  templates/
    <artifact>.md.template
  checklists/
    <readiness>.md
    <completeness>.md
  evals/
    evals.json
```

Use names that make the execution order obvious. For ordered workflows, prefer `sop-00-*`, `sop-01-*`, and so on.

## SKILL.md Responsibilities

`SKILL.md` should contain:

- Frontmatter with precise `name` and trigger-focused `description`.
- One short paragraph explaining what the skill is for.
- A short “triggered first steps” section.
- A Stage Router that maps user situations to SOP files.
- A recommended full execution order for complete workflows.
- A resource index listing references, templates, and checklists.
- Delivery standards and validation expectations.

`SKILL.md` should not contain:

- Full implementation details for every stage.
- Long templates, long examples, or full schemas.
- Multiple unrelated workflows interleaved in one large body.
- Repeated content that already lives in SOP files.

## SOP File Responsibilities

Each SOP file should own one coherent phase:

- Goal and scope.
- Pre-read requirements.
- Step-by-step execution.
- Files or artifacts it may create or update.
- Validation for that phase.
- Common RED points or failure modes.

Keep each SOP independently useful. A model should be able to read `SKILL.md`, select one SOP, and execute that phase without loading the whole skill directory.

## Progressive Execution Rules

- Read `SKILL.md` first.
- Read the intake or planning SOP next.
- Read only the SOPs needed for the current user request.
- After finishing a phase, return to the Stage Router to decide the next SOP.
- Load templates and checklists only when a SOP calls for them.
- Use validation SOPs or completeness checklists before final delivery.

## When To Use This Pattern

Use SOP-routed structure when the skill:

- Initializes projects or repositories.
- Manages docs, governance, submodules, agents, or runtime workflows.
- Has more than one execution mode.
- Needs staged validation or rollback.
- Would exceed roughly 300-500 lines if implemented only in `SKILL.md`.

For tiny skills with one narrow behavior, a single concise `SKILL.md` may still be enough.

## Anti-Patterns

- Putting all rules, SOPs, templates, and examples into one large `SKILL.md`.
- A Stage Router that lists SOPs but does not say when to read each one.
- SOP files that repeat the full skill overview instead of owning a concrete phase.
- Templates embedded directly in `SKILL.md` when they can live under `templates/`.
- Checklists that are mentioned but not used during validation.

## Example Stage Router

```text
Any request
  -> Stage 0 Intake: references/sop-00-intake.md

Need repository foundation
  -> Stage 1 Repo Foundation: references/sop-01-repo-foundation.md

Need OpenCode configuration
  -> Stage 2 OpenCode Config: references/sop-02-opencode-config.md

After writing files
  -> Stage 3 Validation: references/sop-03-validation.md
```

The router is a decision map, not a table of contents. It should tell the model where to go next.
