# Delegation Quality Gate Validation

This reference defines read-only CLI replay checks for validating delegation quality gates across development workflow stages. The checks are intentionally non-mutating: they must not edit files, create artifacts, run formatters, run tests with write side effects, install dependencies, start servers, or invoke any command that writes to the repository.

## Read-Only Contract

Every replay command must satisfy all of these constraints:

- Include `--pure` so no persistent session or provider state is reused.
- Include `--dir <repo_root>` so execution is scoped to an explicit repository path.
- Instruct the agent to run in read-only mode.
- Instruct the agent not to edit files, not to call write tools, and not to run shell commands that write to disk.
- Capture `git status --short` before and after the replay from the same repository root.
- Pass only when the before and after `git status --short` outputs are byte-for-byte identical.

Use PowerShell examples from the repository root. Replace `E:\aces_desktop\BeautyCustomerService\vendor\ai\maop` with the target maop checkout path when needed.

## Common Acceptance Harness

Run this wrapper pattern around each replay prompt:

```powershell
$repo = "E:\aces_desktop\BeautyCustomerService\vendor\ai\maop"
$before = git -C $repo status --short
opencode run --pure --dir $repo "<READ_ONLY_REPLAY_PROMPT>"
$after = git -C $repo status --short
if (($before -join "`n") -ne ($after -join "`n")) { throw "git status --short changed during read-only replay" }
```

Acceptance criteria:

- The replay command includes `--pure` and `--dir $repo`.
- The replay prompt explicitly says read-only, no edits, no file writes, no formatting, no tests or commands that write outputs.
- The replay may inspect files and report findings only.
- The final `git status --short` is identical to the initial `git status --short`.
- Any proposed changes are described as recommendations, not applied.

## Product Definition Replay

Validate that product-definition delegation asks for requirements, scope, users, scenarios, acceptance criteria, and open questions without modifying the repository.

```powershell
$repo = "E:\aces_desktop\BeautyCustomerService\vendor\ai\maop"
$before = git -C $repo status --short
opencode run --pure --dir $repo "Read-only replay for product-definition delegation quality gate. Do not edit files, do not call write tools, do not run formatters, tests, generators, installs, or any shell command that writes to disk. Inspect only the relevant skill guidance and report whether a product-definition request would capture problem, users, scope, user scenarios, acceptance criteria, assumptions, and open questions before implementation."
$after = git -C $repo status --short
if (($before -join "`n") -ne ($after -join "`n")) { throw "git status --short changed during product-definition replay" }
```

Acceptance criteria:

- Output identifies the request as product-definition work, not implementation or technical design.
- Output checks that acceptance criteria are concrete and testable.
- Output flags missing users, scope boundaries, or unresolved assumptions.
- `git status --short` before and after is unchanged.

## Technical Design Replay

Validate that technical-design delegation checks architecture impact, interfaces, state, dependencies, risks, compatibility, and verification strategy without applying design changes.

```powershell
$repo = "E:\aces_desktop\BeautyCustomerService\vendor\ai\maop"
$before = git -C $repo status --short
opencode run --pure --dir $repo "Read-only replay for technical-design delegation quality gate. Do not edit files, do not call write tools, do not run formatters, tests, generators, installs, or any shell command that writes to disk. Inspect only the relevant skill guidance and report whether a technical-design request would define architecture impact, interfaces, data or state, dependency choices, compatibility risks, rollout boundaries, and verification strategy before implementation."
$after = git -C $repo status --short
if (($before -join "`n") -ne ($after -join "`n")) { throw "git status --short changed during technical-design replay" }
```

Acceptance criteria:

- Output identifies the request as technical-design work and keeps code changes out of scope.
- Output checks interface, state, dependency, compatibility, and rollout boundaries.
- Output includes verification strategy expectations without running verification commands.
- `git status --short` before and after is unchanged.

## Implementation Delivery Replay

Validate that implementation-delivery delegation requires confirmed inputs, minimal change boundaries, verification evidence, review, and truthful delivery reporting without changing files.

```powershell
$repo = "E:\aces_desktop\BeautyCustomerService\vendor\ai\maop"
$before = git -C $repo status --short
opencode run --pure --dir $repo "Read-only replay for implementation-delivery delegation quality gate. Do not edit files, do not call write tools, do not run formatters, tests, generators, installs, or any shell command that writes to disk. Inspect only the relevant skill guidance and report whether an implementation request would confirm inputs, define minimal change scope, require fresh verification evidence, perform review before completion, and clearly report any unrun verification."
$after = git -C $repo status --short
if (($before -join "`n") -ne ($after -join "`n")) { throw "git status --short changed during implementation-delivery replay" }
```

Acceptance criteria:

- Output identifies implementation-delivery as the correct route for code changes, bugfixes, verification, or delivery summaries.
- Output checks that implementation must not start from missing product or design inputs.
- Output requires fresh verification evidence and review before completion claims.
- Output reports unrun verification as unrun, not passed.
- `git status --short` before and after is unchanged.

## Cross-Stage Conflict And PR Replay

Validate that delegation detects conflicting stage signals and PR/review scenarios, routes to the safest stage, and avoids mutating the repository while reviewing.

```powershell
$repo = "E:\aces_desktop\BeautyCustomerService\vendor\ai\maop"
$before = git -C $repo status --short
opencode run --pure --dir $repo "Read-only replay for cross-stage conflict and PR delegation quality gate. Do not edit files, do not call write tools, do not run formatters, tests, generators, installs, or any shell command that writes to disk. Inspect only the relevant skill guidance and report how to handle a mixed request that asks for PR review, requirements clarification, technical design concerns, and possible implementation fixes. Resolve stage conflicts safely, identify when to stop for clarification, and state that review findings must be reported without applying changes."
$after = git -C $repo status --short
if (($before -join "`n") -ne ($after -join "`n")) { throw "git status --short changed during cross-stage PR replay" }
```

Acceptance criteria:

- Output treats PR review as review-first and findings-first, not automatic implementation.
- Output separates product-definition gaps, technical-design gaps, and implementation-delivery risks.
- Output identifies conflicts that require clarification before code changes.
- Output does not apply fixes during review replay.
- `git status --short` before and after is unchanged.

## Failure Conditions

A replay fails the quality gate if any of the following occurs:

- The command omits `--pure` or `--dir`.
- The prompt permits editing, formatting, generation, installs, test execution with write outputs, server startup, commits, or any write command.
- The agent edits files, creates artifacts, changes configuration, stages files, or changes submodule state.
- `git status --short` differs before and after the replay.
- The response routes directly to implementation when product or technical design prerequisites are missing.
- The response claims verification passed without fresh evidence from an explicitly allowed verification command.
