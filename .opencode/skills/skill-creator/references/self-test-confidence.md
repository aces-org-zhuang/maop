# Skill Self-Test and Confidence Gate

Use this SOP when creating or improving a skill and the user needs confidence that the skill triggers, executes completely, and produces high-quality results.

## Goal

Run a repeatable self-test loop using `opencode run` prompts, qualitative/quantitative evaluation, and a `reasoning-map` review. Do not mark the skill ready unless final confidence is at least 90%.

## What To Measure

Evaluate four dimensions:

- Trigger rate: the skill is invoked for prompts that should use it, and not invoked for near-miss prompts.
- Execution completeness: the skill follows its intended stages, reads the right SOP/reference files, performs required validation, and does not stop halfway.
- Output quality: outputs meet the user's success criteria, use the right format, and avoid overfitting or unnecessary verbosity.
- Operational safety: the skill respects file boundaries, avoids destructive actions unless authorized, handles secrets safely, and explains blockers clearly.

## Test Set

Create at least 10 prompts before claiming 90% confidence:

- 4 should-trigger prompts covering the main workflow.
- 2 should-trigger prompts covering edge cases or ambiguous wording.
- 2 should-not-trigger near misses.
- 2 execution-completeness prompts that require multi-stage behavior, validation, or SOP routing.

For complex skills, use 15-20 prompts with a 60/40 split between train and held-out prompts.

## opencode run Trigger Tests

Use `opencode run` to verify real triggering behavior. Keep prompts small and stop as soon as the target signal is visible.

Target signals:

- Output includes `Skill "<skill-name>"`, or clearly states it is using the target skill.
- For SOP-routed skills, output reads or names the expected `references/sop-*.md` file.
- For negative prompts, output should not include the target skill signal.

Example:

```bash
opencode run "<test prompt>"
```

If available, use existing trigger optimization scripts for repeated runs:

```bash
python -m scripts.run_eval \
  --eval-set <trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id> \
  --runs 3 \
  --trigger-threshold 0.67
```

Raise the threshold for release readiness. A skill intended to be reliable should pass held-out trigger tests at 90% or better.

## Execution Completeness Tests

For each should-trigger workflow prompt, inspect whether the run completed the intended path:

- Did it read the right SOP/reference file after `SKILL.md`?
- Did it follow the staged order instead of jumping directly to an answer?
- Did it use templates/checklists only when needed?
- Did it perform validation before final output?
- Did it report unresolved blockers or RED points?

For each run, assign one of these scores:

```text
1.0  complete: all required stages and validation happened
0.7  mostly complete: minor missing validation or weak final reporting
0.4  partial: skill triggered but missed key stages or SOP routing
0.0  failed: did not trigger, ignored the workflow, or produced unsafe output
```

## Quality Tests

Use the normal skill-creator benchmark loop for output quality when outputs are substantial:

- Create `evals/evals.json` prompts.
- Run with-skill and baseline/old-skill comparisons.
- Grade assertions with `agents/grader.md`.
- Aggregate with `scripts.aggregate_benchmark`.
- Use `agents/analyzer.md` to inspect false positives, weak assertions, high variance, and token/time tradeoffs.

For small skills, a lighter review is acceptable, but still record pass/fail evidence and reasons.

## reasoning-map Confidence Review

After tests, run a `reasoning-map` review before declaring readiness. The map must cover:

```text
[Trigger Layer]
   -> should-trigger coverage
   -> should-not-trigger near misses

[Execution Layer]
   -> SOP routing or main workflow stages
   -> validation and delivery requirements

[Quality Layer]
   -> output correctness
   -> format adherence
   -> user success criteria

[Risk Layer]
   -> destructive action boundaries
   -> secrets and permissions
   -> over-triggering or under-triggering

[Evidence Layer]
   -> opencode run logs
   -> benchmark/assertion results
   -> human review or sample output inspection
```

Any broad or unverified RED node lowers confidence until it has a test, a fix, or a bounded follow-up.

## Confidence Formula

Compute confidence from observable evidence rather than intuition:

```text
trigger_score = passed_trigger_cases / total_trigger_cases
completeness_score = average execution completeness score
quality_score = passed_quality_assertions / total_quality_assertions
safety_score = passed_safety_checks / total_safety_checks

confidence =
  0.30 * trigger_score +
  0.30 * completeness_score +
  0.25 * quality_score +
  0.15 * safety_score
```

If a dimension is not applicable, redistribute its weight to the remaining dimensions and explain why.

## Release Gate

Do not call the skill ready unless:

- Confidence is `>= 0.90`.
- Held-out trigger prompts pass at `>= 0.90` when a held-out set exists.
- No critical RED remains in the reasoning-map review.
- The skill has at least one validation path documented in `SKILL.md`, an SOP, or a checklist.

If confidence is below 90%, iterate:

1. Identify the weakest dimension.
2. Update description, `SKILL.md`, SOP routing, templates, or checklists.
3. Rerun the affected test set.
4. Recompute confidence.
5. Repeat until confidence is at least 90% or explain the blocker.

## Reporting Format

Use a short final report:

```text
Skill: <name>
Trigger score: <n>/<n> = <score>
Completeness score: <score>
Quality score: <score>
Safety score: <score>
Final confidence: <score>
Gate: PASS | FAIL
Evidence: <opencode run prompts, benchmark paths, review files>
Remaining RED: <none or bounded follow-up>
```

Keep raw logs in the workspace. Do not paste long `opencode run` transcripts into the final answer; summarize the target signals and link or record the files when available.
