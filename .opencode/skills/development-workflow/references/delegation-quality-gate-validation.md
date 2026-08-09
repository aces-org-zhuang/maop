# Delegation Quality Gate Validation

This reference defines read-only CLI replay checks for validating delegation quality gate behavior across development workflow stages. The checks are intentionally non-mutating and non-invasive: they must not read source files, inspect repository content, edit files, create artifacts, run tests, run builds, run installs, start services, or invoke any command beyond the outer `git status --short` acceptance harness.

## Read-Only Contract

Every replay command must satisfy all of these constraints:

- Include `--pure` so no persistent session or provider state is reused.
- Include `--dir <repo_root>` so execution is scoped to an explicit repository path.
- Instruct the agent to validate skill behavior from the prompt only.
- Instruct the agent not to read source files, not to inspect repository content, not to edit files, and not to write to the repository.
- Instruct the agent not to run tests, builds, installs, formatters, generators, services, or shell commands.
- Capture `git status --short` before and after the replay from the same repository root.
- Pass only when the before and after `git status --short` outputs are byte-for-byte identical.

Use PowerShell examples from the repository root. Replace `E:\aces_desktop\BeautyCustomerService\vendor\ai\maop` with the target maop checkout path when needed.

## Common Acceptance Harness

Run this wrapper pattern around each replay prompt:

```powershell
$repo = "E:\aces_desktop\BeautyCustomerService\vendor\ai\maop"
$before = git -C $repo status --short
opencode run --pure --dir $repo "<READ_ONLY_BEHAVIOR_VALIDATION_PROMPT>"
$after = git -C $repo status --short
if (($before -join "`n") -ne ($after -join "`n")) { throw "git status --short changed during read-only replay" }
```

Acceptance criteria:

- The replay command includes `--pure` and `--dir $repo`.
- The replay prompt explicitly says read-only behavior validation only, validate from the prompt only, no source reads, no repository inspection, no edits, no file writes, no tests, no builds, no installs, no services, and no shell commands.
- The replay output is limited to delegation-gate behavior: todo preflight judgment, whether child-agent delegation is required, whether delegation should be parallel, compact output boundaries, and why the full packet should not be expanded.
- The final `git status --short` is identical to the initial `git status --short`.
- Any proposed changes are described as recommendations, not applied.

## Product Definition Replay

Validate that product-definition delegation performs the required preflight and delegation checks without reading source or modifying the repository.

```powershell
$repo = "E:\aces_desktop\BeautyCustomerService\vendor\ai\maop"
$before = git -C $repo status --short
opencode run --pure --dir $repo "Read-only behavior validation for product-definition delegation quality gate. Validate from this prompt only. Do not read source files or inspect repository content. Do not edit files, write files, create artifacts, run shell commands, run tests, run builds, run installs, start services, format, or generate files. For a product-definition request, report only whether the response should: perform todo preflight before stage work, decide whether a child agent must be delegated, decide whether delegation should be parallel, keep output compact, and explain why the full packet should not be expanded."
$after = git -C $repo status --short
if (($before -join "`n") -ne ($after -join "`n")) { throw "git status --short changed during product-definition replay" }
```

Acceptance criteria:

- Output identifies that todo preflight must happen before product-definition stage work.
- Output states whether product-definition should be delegated to a child agent and why.
- Output states whether delegation should be parallel or sequential and why.
- Output keeps the answer compact and does not expand the full product-definition packet.
- Output explains why the full packet should not be expanded during this validation.
- `git status --short` before and after is unchanged.

## Technical Design Replay

Validate that technical-design delegation performs the required preflight and delegation checks without reading source or modifying the repository.

```powershell
$repo = "E:\aces_desktop\BeautyCustomerService\vendor\ai\maop"
$before = git -C $repo status --short
opencode run --pure --dir $repo "Read-only behavior validation for technical-design delegation quality gate. Validate from this prompt only. Do not read source files or inspect repository content. Do not edit files, write files, create artifacts, run shell commands, run tests, run builds, run installs, start services, format, or generate files. For a technical-design request, report only whether the response should: perform todo preflight before stage work, decide whether a child agent must be delegated, decide whether delegation should be parallel, keep output compact, and explain why the full packet should not be expanded."
$after = git -C $repo status --short
if (($before -join "`n") -ne ($after -join "`n")) { throw "git status --short changed during technical-design replay" }
```

Acceptance criteria:

- Output identifies that todo preflight must happen before technical-design stage work.
- Output states whether technical-design should be delegated to a child agent and why.
- Output states whether delegation should be parallel or sequential and why.
- Output keeps the answer compact and does not expand the full technical-design packet.
- Output explains why the full packet should not be expanded during this validation.
- `git status --short` before and after is unchanged.

## Implementation Delivery Replay

Validate that implementation-delivery delegation performs the required preflight and delegation checks without reading source, running tests, or modifying the repository.

```powershell
$repo = "E:\aces_desktop\BeautyCustomerService\vendor\ai\maop"
$before = git -C $repo status --short
opencode run --pure --dir $repo "Read-only behavior validation for implementation-delivery delegation quality gate. Validate from this prompt only. Do not read source files or inspect repository content. Do not edit files, write files, create artifacts, run shell commands, run tests, run builds, run installs, start services, format, or generate files. For an implementation-delivery request, report only whether the response should: perform todo preflight before implementation work, decide whether a child agent must be delegated, decide whether delegation should be parallel, keep output compact, and explain why the full packet should not be expanded."
$after = git -C $repo status --short
if (($before -join "`n") -ne ($after -join "`n")) { throw "git status --short changed during implementation-delivery replay" }
```

Acceptance criteria:

- Output identifies that todo preflight must happen before implementation-delivery work.
- Output states whether implementation-delivery should be delegated to a child agent and why.
- Output states whether delegation should be parallel or sequential and why.
- Output keeps the answer compact and does not expand the full implementation-delivery packet.
- Output explains why the full packet should not be expanded during this validation.
- Output does not claim tests, builds, or verification commands were run.
- `git status --short` before and after is unchanged.

## Cross-Stage Conflict And PR Replay

Validate that mixed-stage and PR/review delegation performs the required preflight and delegation checks without reading source or modifying the repository.

```powershell
$repo = "E:\aces_desktop\BeautyCustomerService\vendor\ai\maop"
$before = git -C $repo status --short
opencode run --pure --dir $repo "Read-only behavior validation for cross-stage conflict and PR delegation quality gate. Validate from this prompt only. Do not read source files or inspect repository content. Do not edit files, write files, create artifacts, run shell commands, run tests, run builds, run installs, start services, format, or generate files. For a mixed request involving PR review, requirements clarification, technical design concerns, and possible implementation fixes, report only whether the response should: perform todo preflight before stage work, decide whether child agents must be delegated, decide whether delegation should be parallel, keep output compact, and explain why the full packet should not be expanded."
$after = git -C $repo status --short
if (($before -join "`n") -ne ($after -join "`n")) { throw "git status --short changed during cross-stage PR replay" }
```

Acceptance criteria:

- Output identifies that todo preflight must happen before cross-stage or PR review work.
- Output states whether child agents should be delegated for distinct stage concerns and why.
- Output states whether delegation should be parallel for independent stage concerns and why.
- Output keeps the answer compact and does not expand the full review, product, design, or implementation packets.
- Output explains why full packets should not be expanded during this validation.
- Output does not apply fixes during review replay.
- `git status --short` before and after is unchanged.

## Failure Conditions

A replay fails the quality gate if any of the following occurs:

- The command omits `--pure` or `--dir`.
- The prompt permits source reads, repository inspection, editing, formatting, generation, installs, test execution, build execution, server startup, commits, or any shell command inside the replay.
- The agent reads source files, inspects repository content, edits files, creates artifacts, changes configuration, stages files, or changes submodule state.
- `git status --short` differs before and after the replay.
- The response skips todo preflight judgment.
- The response omits whether child-agent delegation is required.
- The response omits whether delegation should be parallel.
- The response expands full stage packets instead of keeping validation output compact.
- The response omits why full packets should not be expanded during validation.
- The response claims tests, builds, services, or verification commands were run.
