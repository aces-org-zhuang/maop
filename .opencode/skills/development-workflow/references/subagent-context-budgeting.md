# Subagent Context Budgeting

Use subagent Task delegation to isolate low-value exploration context while keeping responsibility for intent, reasoning, convergence, review, and final decisions in the main agent.

## Core Rule

```text
Main agent owns:
  intent -> scope -> reasoning-map -> delegation plan -> synthesis -> decision gate -> final handoff

Subagent owns:
  bounded search/exploration/review/extraction -> structured evidence return
```

Subagents reduce context load; they must not replace the main agent's reasoning-map, user-facing tradeoff, design decision, or final approval responsibility.

## When To Delegate

- Broad retrieval: sources, links, trends, learning resources, knowledge bases, Weixin leads, tool/skill discovery.
- Code or document exploration: find entry points, call chains, config owners, existing patterns, duplicate implementations, tests.
- Candidate expansion: research repo candidates, technical-design dependency candidates, market/product examples.
- Independent review: checklist-based review, evidence completeness review, design risk review, output quality review.
- Mechanical extraction: convert source material into tables, source indexes, candidate matrices, evidence maps, IPO tables.
- Parallel option analysis: one bounded option, dependency, module, repo, or source family per subagent.

## When Not To Delegate

- Final product scope, architecture, technical route, or primary dependency selection.
- User preference and tradeoff interpretation.
- Cross-subagent synthesis or conflict resolution.
- Writing final governance rules, design approval, implementation completion claims, or release-readiness claims.
- Tasks that require one continuous source of truth, unless the subagent receives a precise slice and return contract.

## Delegation Gate

Before spawning a subagent:

1. Run or update a lightweight reasoning-map for the task boundary.
2. Define exactly one bounded question or artifact per subagent.
3. Provide minimal context, relevant paths, stopping condition, and forbidden scope.
4. Define a return contract.
5. Record what was delegated so the main agent does not repeat the same broad exploration.

## Return Contract

Every subagent must return concise structured output:

| Field | Required content |
| --- | --- |
| Finding | Direct answer to the bounded question. |
| Evidence | File paths, URLs, commands, source excerpts, or artifact references. |
| Confidence | High/medium/low or numeric score with reason. |
| RED points | Missing evidence, conflicts, risks, blockers, or assumptions. |
| Excluded scope | What the subagent intentionally did not inspect. |
| Next step | Expand, converge, verify, reject, or escalate to main decision. |

## Anti-Over-Isolation Rules

- Do not split one tightly coupled design decision across multiple subagents without a main-agent synthesis step.
- Do not let different subagents choose competing final architectures or dependencies independently.
- Do not ask subagents to write production changes unless the implementation slice is narrow, reviewed, and has an explicit verification plan.
- Do not delegate just to avoid reading critical evidence; the main agent should spot-check decisive evidence before final decisions.
- If subagent outputs conflict, return to reasoning-map and resolve at the main-agent level.

## Completion Gate

After subagents return:

1. Summarize only decision-relevant findings into the main context.
2. Run a convergence pass: keep, reject, or request another bounded subagent round.
3. Spot-check decisive evidence before finalizing.
4. Preserve RED points in the final artifact or handoff.
5. Make the final decision in the main agent, not inside a subagent transcript.
