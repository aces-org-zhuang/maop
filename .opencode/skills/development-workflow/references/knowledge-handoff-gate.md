# Knowledge and Handoff Gate

This gate controls what each development pipeline reads, archives, revises, and hands off. It prevents repeated research, repeated upstream analysis, and stale documentation drift.

## Core Rule

```text
Read minimum stable context -> produce stage artifact -> review -> archive or revise stable knowledge -> hand off one packet to the next stage.
```

Project-specific documentation and tracker rules take priority. If the project has no explicit rule, use this gate.

## Read Gate

Run at pipeline intake and before major review.

1. Read the smallest relevant context first: root `AGENTS.md`, `docs/README.md`, and `docs/07-llm/llm-reading-order.md` when `docs/` exists.
2. Read the current directory `README.md` or index before editing any `docs/` file.
3. Prefer upstream handoff packets over repeating upstream analysis.
4. Product work reads existing PRD, roadmap, user feedback, overview, and prior research references only when relevant.
5. Technical design reads product handoff, architecture, contracts, development rules, and source directory structure.
6. Implementation reads technical handoff, related source, tests, verification rules, and evidence index.
7. Do not read the whole `docs/` tree by default; add more documents only when the current RED point requires them.

## Archive Gate

Run after Review Gate and before final handoff when the stage creates durable knowledge.

Archive to `docs/` only when all conditions hold:

1. The knowledge is stable beyond the current task.
2. It affects requirements, architecture, contracts, runtime, validation workflow, LLM workflow, reusable failure modes, debug knowledge, or requirement-to-implementation evidence.
3. It has passed the relevant Review Gate or has fresh verification evidence.
4. The target directory and index are known.

Use these destinations:

- `docs/`: stable project knowledge, governance rules, decisions, reusable records, and evidence indexes.
- `guides/`: non-research stage notes, temporary engineering process notes, and task-local implementation records.
- `vendor/research/aces-research/`: research process, papers, open source comparison, candidate materials, external sources, and evidence packages.

Do not archive unverified assumptions as stable facts. If a partial rule must be recorded, mark it `状态：暂定` and list the evidence needed to make it stable.

## Revision Gate

Run whenever current source facts, verified behavior, or stage artifacts conflict with existing documentation.

1. Mark the conflict as a RED point until resolved or explicitly deferred.
2. If the current task depends on the stale document, revise it before downstream handoff.
3. If the document is stale but outside the current scope, record `Docs stale` in the handoff packet with owner or follow-up.
4. New `docs/` files must update the matching `README.md` or index.
5. Durable architecture decisions go under `docs/06-decisions/` and update its README.
6. Requirement-to-implementation evidence goes under `docs/evidences/` and updates its index.
7. Reusable failure modes go under `docs/failure-modes/` and update its index.
8. Complex debug records go under `docs/debugs/` and update its index.

## Reuse Ledger

Maintain a concise ledger in stage outputs and handoff packets:

- `Read`: docs, handoff packets, source paths, tests, research materials, or external sources consumed.
- `Reused`: conclusions inherited without re-analysis.
- `Spot-checked`: decisive evidence checked by the main agent.
- `Delegated`: bounded subagent tasks and their returned artifact references.
- `Rejected`: options, candidates, or duplicate research paths already ruled out.
- `Open RED`: assumptions, missing evidence, stale docs, or follow-up work.

Downstream stages must consume the ledger before doing new exploration. Repeat broad research only when the ledger is missing, stale, contradicted by source facts, or insufficient for a current RED point.

## Product Handoff Packet

Produce when product scope, PRD, MVP, or requirements are handed to technical design.

- Original input summary.
- Confirmed roles.
- Core Use Cases.
- In scope, out of scope, and deferred scope.
- Functional and non-functional requirements.
- Acceptance signals.
- Assumptions and open questions.
- Read and reused docs or research references.
- Rejected product options or duplicate research paths.
- Archive or revision actions taken, skipped, or still RED.

## Technical Handoff Packet

Produce when technical design is handed to implementation.

- Requirement trace mapping.
- Source directory structure and relevant entry points.
- Module owners and change boundaries.
- Interface, data, state, permission, config, and migration impact.
- Recommended option and rejected options.
- Risks, high-risk assumptions, and validation strategy.
- Implementation slices with target file categories and verification signals.
- Read, reused, spot-checked, delegated, and rejected exploration.
- Archive or revision actions taken, skipped, or still RED.

## Delivery Evidence Packet

Produce at implementation delivery.

- Actual changed files.
- Requirement and design mapping.
- Verification commands and fresh evidence.
- Tests or checks not run, with reason.
- User-visible behavior changes.
- Residual risks and rollback notes.
- Docs updated, docs stale, and docs not updated with reason.
- Evidence, ADR, failure-mode, or debug records created or deferred.

## Handoff Rules

1. A downstream stage reads the upstream packet before broad exploration.
2. A downstream stage may spot-check decisive evidence but should not recreate upstream research by default.
3. If the packet is missing required fields, mark the gap RED and either repair from available evidence or route back upstream.
4. If source facts contradict the packet, source facts win; revise the stale packet or docs when in scope.
5. Final delivery must state whether Archive Gate and Revision Gate were satisfied, skipped, or blocked.
