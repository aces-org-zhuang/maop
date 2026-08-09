# Delegation Quality Gate

Delegation Quality Gate makes subagent use safe by default. The primary path is preventive: decide before dispatch, isolate context, define a return contract, and synthesize after return. The fallback remediation path keeps the main agent responsible when delegation is unsafe or the result is not usable.

## When To Use

- Use before any subagent Task, background agent, parallel exploration, independent review, or bounded research slice.
- Use when a task may read broad context, touch files, inspect a submodule, compare options, or produce evidence for a downstream decision.
- Do not use subagents to outsource final responsibility. The main agent owns final synthesis, user-facing claims, and write decisions.

## Primary Delegation Path

1. Delegation Decision: decide `must-delegate`, `may-delegate`, or `do-not-delegate` before work starts. Use `templates/delegation-decision.md`.
2. Context Isolation: send only the needed paths, facts, constraints, and forbidden areas. Use `templates/context-isolation-packet.md`.
3. Worktree/Submodule Isolation: state allowed write scope, dirty-worktree rule, and submodule rule. Use `templates/worktree-submodule-isolation.md` when files, git state, or submodules are involved.
4. Return Contract: require concrete files, evidence, confidence, blockers, and changed-scope notes. Use `templates/subagent-return-contract.md`.
5. Synthesis Gate: verify the returned output before merging it into the main reasoning path. Use `templates/synthesis-gate.md`.

## Decision Classes

Use exactly one decision class:

- `must-delegate`: the task is complex, cross-domain, evidence-heavy, high-risk, or too broad for one safe main-context pass.
- `may-delegate`: delegation can improve evidence or review quality, but the main agent can still proceed safely without it.
- `do-not-delegate`: delegation would add noise, leak responsibility, violate user constraints, or outsource a decision owned by the main agent.

## Fallback Remediation Path

Fallback remediation is not the default implementation path. Use it only when a primary gate, return contract, synthesis check, review, verification, PR merge, or external dependency fails. Fallback to the main agent when any condition below is true:

- The task boundary cannot be stated in one short packet.
- Required paths, permissions, config, credentials, network access, or write scope are missing.
- The worktree or submodule state creates risk that cannot be isolated.
- The subagent returns without file references, evidence, verification status, or residual risks.
- The result conflicts with project rules, user instructions, allowed scope, or observed code.
- The result is stale, speculative, over-broad, or mixes unrelated context.

Fallback actions:

- Narrow the task and handle it in the main context.
- Ask one focused user question only if a required decision or permission is missing.
- Re-dispatch only after creating a smaller isolation packet and stricter return contract.
- Do not pass a failed delegation result downstream as confirmed fact.

## Acceptance Rules

- A delegated result is accepted only after Synthesis Gate passes.
- Evidence must name exact files, commands, outputs, URLs, or artifacts used.
- Claims without fresh evidence stay as assumptions or risks.
- File edits from a subagent are acceptable only if they match the allowed file scope and do not modify unrelated dirty changes.
- Submodule edits are acceptable only when explicitly authorized and handled under the project submodule rules.

## Minimal Record

Record the following in the main agent notes or final handoff when delegation affects decisions:

- Why delegation was used.
- What context was sent.
- What was accepted, rejected, or retried.
- What evidence supports the accepted result.
- Which fallback action was taken, if any.
