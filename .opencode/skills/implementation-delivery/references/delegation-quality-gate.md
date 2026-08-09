# Delegation Quality Gate

Implementation delivery uses Delegation Quality Gate as a pre-code error-prevention path. Delegate only when it improves evidence quality, context coverage, or independent review without losing main-agent ownership of edits and final claims.

## Main Path Before Code

1. Classify the slice: decide whether the work needs broad read-only exploration, test surface discovery, independent diff/risk review, conflict resolution, or evidence extraction.
2. Isolate context: name allowed paths, forbidden paths, dirty-worktree facts, submodule boundaries, expected inputs, and output format.
3. Define the return contract: require exact files, line references when useful, commands/checks, risk notes, blockers, and confidence level.
4. Synthesize before editing: accept only evidence-backed results and fold them into Interrupted Slice Guard and Pre-Code Acceptance Contract.
5. Keep ownership: the main agent makes write decisions, applies final patches, runs or reports verification, and writes Delivery Evidence Packet.

## Implementation Must Delegate Triggers

Delegate before code when any condition is true and the boundary can be isolated:

- Read-only exploration spans many directories, large generated files, submodules, or unknown test conventions.
- Test Surface discovery needs independent mapping of impacted tests, smoke paths, fixtures, snapshots, or manual checks.
- Diff/Risk review is required for high-risk behavior, security, data migration, shared API, compatibility, or user-visible workflow changes.
- Conflict Resolution needs separation of user/other-agent changes from the current slice before editing.
- Evidence Extraction needs a neutral pass over logs, outputs, traces, artifacts, screenshots, or prior handoff packets.

## Implementation May Delegate Triggers

Delegate when useful, but keep the slice in the main agent if the overhead is higher than the risk:

- Narrow code search with multiple plausible entry points.
- Independent review of a completed small patch.
- Summarizing fresh verification output into claim-to-evidence rows.
- Comparing nearby implementation patterns before selecting the minimal change.

## Implementation Do-Not Delegate Triggers

Do not delegate when any condition is true:

- The task requires final product, architecture, or external-operation decisions that the main agent must own.
- The needed boundary, allowed files, credentials, permissions, or verification signal cannot be stated.
- The task would ask a subagent to edit outside the authorized scope, rewrite unrelated work, commit, push, or mutate submodules without explicit authorization.
- The result would be speculative because required project files or runtime evidence are unavailable.
- The work is a tiny deterministic patch where delegation adds no safety signal.

## Delegation Lenses

- Read-Only Code Exploration: ask for candidate files, relevant functions, observed patterns, forbidden assumptions, and unknowns. No edits.
- Test Surface: ask for impacted automated tests, missing tests, manual checks, fixture/snapshot risks, and the smallest fresh verification set.
- Diff/Risk Review: ask for findings-first review, regression risk, security/data/API compatibility impact, and score if used by the workflow.
- Conflict Resolution: ask for dirty-worktree inventory, ownership uncertainty, safe next action, and files that must not be touched.
- Evidence Extraction: ask for claim-to-evidence mapping with exact commands, outputs, artifacts, timestamps when available, and residual gaps.

## Worktree/Submodule Isolation

- Before dispatch, record current slice state in Interrupted Slice Guard: existing changes, unknown ownership, submodule status, and the next minimal safe action.
- In Pre-Code Acceptance Contract, state allowed files/areas, forbidden files/areas, whether submodules are read-only or writable, and what conflicts stop the work.
- In Delivery Evidence Packet, report any delegated result used, accepted/rejected evidence, worktree/submodule isolation outcome, and unresolved ownership risks.

## Fallback Path

Fallback is only a safety net. If delegation cannot be bounded or returned evidence is weak, keep the work in the main context, narrow the slice, ask one focused question only when required, or stop on a hard permission/configuration blocker. Do not treat fallback as permission to skip pre-code risk checks.
