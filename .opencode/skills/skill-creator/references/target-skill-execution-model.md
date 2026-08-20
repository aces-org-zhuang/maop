# Target Skill Execution Model Template

## Purpose

This template defines how a generated skill should describe its own execution model in its own `SKILL.md`.

## Required shape

- `SKILL.md` must contain only:
  - execution model
  - core contracts
  - resource index
- `SKILL.md` must make the model explicit before listing SOPs.
- SOPs must remain standard execution flows for user requests, not execution-model names.
- Generated skills should default to a SOP-routed structure; do not collapse a generated skill into a single-file `SKILL.md`.
- A generated skill must include a `references/` directory with at least intake/routing, execution, validation, and handoff coverage.

## Required model choices

Generated skills must choose one or more of these base models according to the user need. Do not include all four by default.

- `任务依赖树`: express sequential, parallel, and condition edges in one dependency structure.
- `round`: use for divergence and convergence across multiple passes.
- `loop`: use for bounded retry and exit conditions.
- `dialectical`: use for multi-view execution, adversarial comparison, and main-flow arbitration.

## Required behavior in generated skills

- The generated skill must tell the main LLM to dispatch bounded agents for SOP execution only under explicit node conditions such as parallel subviews, isolated evidence gathering, or adversarial comparison.
- The generated skill must tell the main LLM to update `todo/status` before and after actual execution.
- The generated skill must preserve goal continuity so no task is lost across rounds, loops, or merges.

## ASCII example

```text
Generated skill SKILL.md
  ├─ Execution model
  │   ├─ Selected base model(s): 任务依赖树 + loop
  │   ├─ Node map
  │   │   ├─ sop-00-intake-and-routing {main flow}
  │   │   ├─ sop-01-dispatch-execute {delegate only under explicit parallel / isolated-evidence conditions}
  │   │   ├─ sop-02-validate-and-handoff {main flow validation}
  │   │   └─ sop-03-handoff {main flow handoff}
  │   └─ Delegation policy
  │       ├─ delegate agents only when the node condition says so
  │       └─ do not delegate pure routing, final validation, or final handoff
  ├─ Core contracts
  │   ├─ todo/status updates before and after execution
  │   └─ bounded agent dispatch for each sop
  └─ Resource index
      ├─ sop-00-intake-and-routing.md
      ├─ sop-01-dispatch-execute.md
      ├─ sop-02-validate-and-handoff.md
      └─ sop-03-handoff.md

Generated skill references/
  ├─ sop-00-intake-and-routing.md
  ├─ sop-01-dispatch-execute.md
  ├─ sop-02-validate-and-handoff.md
  └─ sop-03-handoff.md
```

## Generation note

When `skill-creator` writes a new skill, it should read this template and then write the generated skill's own execution model section from it, rather than copying the template wholesale into the generator's own entry file.
