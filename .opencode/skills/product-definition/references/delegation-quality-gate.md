# Product Delegation Quality Gate

This gate adapts `development-workflow/references/delegation-quality-gate.md` for product-definition work. The main path is preventive: decide whether to delegate before dispatch, isolate product context, define a product return contract, then synthesize through product lenses. Fallback is only a safety net; it must not replace the preventive gate.

## Main Path

1. Decide whether delegation is useful, safe, and bounded before using any subagent, background task, parallel exploration, external scan, or independent review.
2. Send only the needed product context: original input, current assumptions, allowed files or materials, forbidden areas, expected lens, and output format.
3. Define a return contract with exact evidence, affected roles, Use Cases, acceptance signals, risks, alternatives, scope changes, assumptions, and blockers.
4. Run Synthesis Gate in the main agent before accepting delegated output into PRD, product brief, review result, or Product Handoff Packet.
5. Record accepted, rejected, retried, and fallback results when delegated output changes product decisions.

## Product Delegate Triggers

Must delegate when:

- A product decision depends on bounded market, competitor, alternative, user-segment, or evidence discovery that would otherwise crowd out the main product reasoning.
- An existing PRD, requirement set, or handoff packet needs independent completeness review before entering `technical-design`.
- Multiple plausible scopes or alternatives need parallel comparison and the comparison can be constrained to a clear return contract.

May delegate when:

- A narrow User/Use Case slice needs scenario expansion, edge-case discovery, or acceptance-signal refinement.
- A lightweight market or alternative scan can be bounded by named categories, products, sources, or timebox.
- A checklist pass can independently identify missing role, Use Case, acceptance, risk, or scope fields.

Do not delegate when:

- The user is giving a small clarification, direct revision, or single acceptance criterion that the main agent can handle cheaply.
- Product intent, user, success standard, or allowed scope is too ambiguous to express in one short packet.
- The result would decide technical architecture, implementation details, long-term research conclusions, or final user-facing claims without main-agent synthesis.
- Delegation is only being used as fallback after skipping intake, role/use-case mapping, Preview Gate, or Review Gate.

## Product Synthesis Lenses

- User/Use Case lens: every accepted claim must identify the role, trigger, goal, main path, and affected Use Case.
- Acceptance/Risk lens: every accepted requirement must include observable acceptance signals plus risks, dependencies, fallback signals, or open blockers.
- Market/Alternative lens: market claims must name alternatives, source or evidence type, decision impact, and whether the claim is evidence, assumption, or out of scope.
- Scope/Revision lens: every accepted change must state in-scope, out-of-scope, deferred, revised, or rejected status and the reason.

## Product Handoff Packet Absorption Rules

Absorb delegated output field by field. Do not paste a delegated report wholesale into downstream handoff.

- `original_input_summary`: accept only if it preserves the user's wording, goal, pain, constraint, and examples without adding hidden interpretation.
- `users_and_roles`: accept only roles with named segment, goal, trigger, exclusion or priority, and evidence or assumption status.
- `use_cases`: accept only Use Cases with actor, trigger, precondition, goal, main path, branch or edge case, and acceptance signal.
- `scope`: accept only items marked in-scope, out-of-scope, deferred, or rejected with rationale and source.
- `requirements`: accept only requirements mapped to role, Use Case, priority, source, and acceptance criterion.
- `acceptance_criteria`: accept only observable, testable signals with success threshold, negative case, or fallback verification when external dependency exists.
- `risks_and_dependencies`: accept only risks with impact, likelihood or confidence, mitigation, owner or next validation task, and blocking status.
- `market_alternatives`: accept only alternatives with comparison dimension, relevance, evidence type, and implication for scope or differentiation.
- `assumptions`: accept only assumptions with validation path, expiry or review trigger, and downstream impact.
- `open_questions`: accept only questions that block scope, acceptance, risk, or design handoff; otherwise convert to assumption or backlog note.
- `reuse_ledger`: accept only entries with path/source, reused insight, rejected duplicate path, and remaining RED point.
- `handoff_readiness`: accept only after Review Gate score, unresolved blockers, and next-stage conditions are explicit.

## Fallback Rules

- Fallback to the main agent when boundary, evidence, write scope, or return contract is missing, stale, conflicting, speculative, or over-broad.
- Fallback actions are to narrow the task, synthesize manually, ask one focused question only for required decisions, or re-dispatch with a smaller packet.
- Fallback must never be used to skip the pre-delegation decision, context isolation, return contract, or Synthesis Gate.
- Failed delegated output must remain an assumption or risk; it cannot enter PRD, review score, or Product Handoff Packet as confirmed fact.
