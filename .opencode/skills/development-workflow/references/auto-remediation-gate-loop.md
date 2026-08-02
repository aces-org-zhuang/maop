# Auto-Remediation Gate Loop

Use this loop when Review Gate, Confidence Gate, Preview Gate, POC Gate, Verification Gate, selection convergence, research evidence quality, or implementation validation fails.

## Core Rule

Gate failure does not mean stop by default. Gate failure means auto-remediate, rerun the gate, and continue until pass or hard blocker.

```text
Gate fails
  -> classify failure
  -> auto-remediate if safe
  -> rerun gate
  -> repeat up to 7 rounds
  -> stop only on hard blocker or no-progress condition
```

## Defaults

- `max_auto_remediation_rounds = 7`
- Stop early if 2 consecutive rounds make no new progress.
- Each round must have a new action, new evidence, a narrowed scope, or a changed failure classification.
- Do not repeat the same failed action without new information.

## Round Record

Record remediation rounds in the working artifact, final handoff, or internal notes:

| Round | Failed gate | Failure evidence | Remediation action | Rerun signal | Progress? | Remaining RED |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  | yes/no |  |

## Auto-Remediate By Default

| Failure type | Default remediation |
| --- | --- |
| Review score <80 | Add missing scope, risk, boundary, evidence, validation, or structure; rerun review. |
| Confidence <90% | Add evidence, retrieval, comparison, counterexample analysis, or verification; recompute confidence. |
| Preview quality issue | Revise structure, diagram, layout, density, wording, style, or interaction; regenerate preview. |
| POC failure | Inspect failure, shrink slice, fix controllable issue, add mock/fallback, rerun minimal proof. |
| Test/lint/build/typecheck failure | Read failure output, fix code/config/test/docs, rerun fresh verification. |
| Research evidence gap | Expand retrieval, improve source quality, add counterexamples, update source index, reconverge. |
| Selection not converged | Expand/reduce candidates, enforce top-down levels, primary uniqueness, deployment-first, and build map. |
| Design governance issue | Update reasoning-map, ownership, source of truth, dependency uniqueness, runtime/build boundary, rollback. |
| Initialization completeness gap | Add missing index, README, AGENTS, docs link, `.opencode` bridge, validation record, or feedback loop. |
| Skill quality gap | Improve trigger, SOP routing, evals, checklist, templates, examples, and should-not-trigger cases. |

## Hard Blockers

Stop and ask the user only when a blocker remains after auto-discovery and safe remediation:

- User explicitly asked to confirm before proceeding.
- Required configuration is missing or unconfirmed.
- Write/destructive/external-side-effect authorization is missing.
- Secret, credential, browser session, external service, network, or permission boundary is unavailable.
- A tradeoff requires user preference and cannot be inferred safely.
- Remediation would change confirmed scope, product intent, architecture direction, or external state.
- Two consecutive remediation rounds have no new progress.
- Seven remediation rounds are exhausted.

## Gate-Specific Notes

- Configuration Readiness Gate is special: auto-discover and provide acquisition paths first; stop only for missing required config or authorization.
- Reasoning Gate should continue reasoning until RED nodes are resolved or bounded; do not ask just because the first map found uncertainty.
- Subagent Context Gate should not stop; delegate bounded exploration when useful, then synthesize in the main agent.
- Verification Gate must use fresh evidence before completion claims.

## Completion Rule

When remediation passes, continue to the next stage. When it stops, output the hard blocker, attempted rounds, evidence, and the minimal user decision needed.
