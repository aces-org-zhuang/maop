# SOP: Full-Link Skill Quality

Use this SOP when creating or substantially revising a workflow-heavy, governance, research, technical-design, implementation, project initialization, submodule, documentation, or multi-stage skill.

## Goal

Preserve quality across the full skill lifecycle: intent intake, reasoning-map, SOP routing, artifact design, dense expression, validation, evals, and feedback-loop updates.

## Quality Chain

```text
[Intake]
  -> [Reasoning Map]
      -> [SOP Router]
          -> [Artifacts/Templates/Checklists]
              -> [Validation + Evals]
                  -> [Feedback Loop + Final Handoff]
```

## Steps

1. Intake: capture the skill goal, trigger phrases, should-trigger contexts, should-not-trigger near misses, expected outputs, required tools, artifact locations, and user success criteria.
2. Reasoning-map: map the workflow scope, stage boundaries, producer -> artifact -> validator -> consumer chains, risks, RED points, and confidence gaps before writing large changes.
3. Routing design: if the workflow has multiple phases, create or preserve a short `SKILL.md` router with first steps, Stage Router, resource index, recommended full order, and delivery standards.
4. SOP design: put phase-level steps in `references/sop-*.md`; each SOP should own one phase, list inputs, outputs, write boundaries, validation checks, and common RED points.
5. Dense artifacts: use Markdown tables, ASCII maps, Mermaid diagrams, templates, and checklists when they make the skill easier to execute or review. Keep diagrams clean and place detailed IPO, interaction logic, evidence, and acceptance criteria in tables.
6. Configuration readiness: when a workflow performs POC, implementation, writes, external calls, tool/MCP/CLI usage, build, package, or verification, add a Configuration Readiness Gate using `development-workflow/references/configuration-readiness-gate.md`; do not ask for required config piecemeal during execution.
7. Todo preflight: for complex skill creation/revision, evals, review, benchmark, or parallel child-agent delegation, update todo before starting; each child-agent delegation, eval batch, review, and benchmark action should have a corresponding todo. Simple one-step wording edits may skip this.
8. Child-agent delegation: when a workflow requires broad search, code/document exploration, candidate expansion, evidence extraction, or independent review, add bounded child-agent delegation guidance using `development-workflow/references/subagent-context-budgeting.md`; do not split final decisions or user-facing tradeoffs into child agents.
9. Auto-remediation: when trigger quality, SOP routing, evals, checklist coverage, output density, review score, or confidence falls short, use `development-workflow/references/auto-remediation-gate-loop.md` to revise and rerun up to 7 rounds before asking the user.
10. Validation: before final delivery, check trigger quality, execution completeness, output quality, resource routing, eval coverage, artifact/index synchronization, restart/package guidance, and unresolved RED points.
11. Evals: for objectively verifiable workflows, add or update `evals/evals.json`; for confidence targets, use `self-test-confidence.md` and do not claim readiness below the requested threshold. Production-readiness defaults to >=90% confidence.
12. Feedback loop: after the edit, run a second reasoning-map pass to verify the original RED points are closed or explicitly bounded, then update templates, checklists, SOP references, and final handoff notes as needed.

## Child-Agent Delegation

Delegate child agents to isolate exploration context, not responsibility. Add this pattern only when it improves signal-to-context ratio:

| Delegate to child agents | Keep in main agent |
| --- | --- |
| Broad retrieval, code/document exploration, candidate expansion, extraction, independent review | Intent, reasoning-map, scope, convergence, final decision, user-facing conclusion |

Each delegated task needs one bounded question, minimal context, forbidden scope, stopping condition, and a return contract covering findings, evidence, confidence, RED points, excluded scope, and next step.

## Dense Output Patterns

Use these patterns to improve information quality and density:

| Need | Preferred format | Why |
| --- | --- | --- |
| Stage routing | ASCII map or compact table | Shows the next file to read without long prose. |
| Trigger design | Markdown table | Makes should-trigger and should-not-trigger cases comparable. |
| Workflow lifecycle | ASCII or Mermaid graph | Shows phase order, branches, and feedback loops. |
| Component or artifact chain | ASCII map plus IPO table | Keeps the graph readable while preserving detailed logic. |
| Acceptance criteria | Markdown table or checklist | Makes pass/fail verification explicit. |
| Reusable output shape | Template file | Prevents future invocations from inventing inconsistent formats. |

## Validation Checklist

- [ ] The skill has a clear trigger-focused `description`.
- [ ] Complex or multi-stage changes used `reasoning-map` before drafting.
- [ ] The execution path is routed through `SKILL.md` and SOP files instead of one long unstructured body.
- [ ] Each SOP has clear inputs, outputs, validation checks, and common RED points.
- [ ] Output quality is improved with tables, ASCII maps, Mermaid diagrams, templates, or checklists where useful.
- [ ] Diagrams are not overloaded; detailed interaction logic and IPO live in adjacent tables.
- [ ] If the workflow needs config before execution, it defines a Configuration Readiness Gate and blocks POC/implementation/build/external calls until required config is confirmed.
- [ ] Complex creation/revision, evals, review, benchmark, and parallel child-agent delegation have corresponding todo entries; simple one-step edits may skip this.
- [ ] If child-agent delegation is useful, the skill defines bounded delegation rules and keeps final decisions in the main agent.
- [ ] If a gate fails, the skill defines auto-remediation behavior with up to 7 rounds and a no-progress stop condition.
- [ ] Evals or self-test confidence gates exist when the workflow can be objectively verified or the user asked for a confidence target.
- [ ] Final delivery names unresolved RED points, validation results, restart/package guidance, and any required follow-up.

## Common RED Points

- The skill contains a Stage Router but no validation or feedback loop.
- The skill writes SOP files but `SKILL.md` does not tell the agent when to read them.
- The output is long prose where a table, ASCII map, Mermaid diagram, template, or checklist would be clearer.
- The skill optimizes trigger wording but never verifies execution completeness.
- The skill claims readiness without evals, reviewer feedback, or a stated confidence result.
- The edit creates resources but does not update the resource index or reference list.
- The skill delegates broad work to child agents without a return contract, or lets child agents make final architecture, selection, scope, or completion decisions.
- The skill starts POC, implementation, writes, builds, external calls, or verification before required configuration is discovered and confirmed.
- The skill treats review/confidence/preview/verification failure as a user pause instead of auto-remediating first.
