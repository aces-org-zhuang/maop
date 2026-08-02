# Configuration Readiness Gate

Use this gate before POC, formal implementation, real scripts/builds/tests, external service access, submodule writes, MCP/CLI/tool usage, deployment, packaging, verification, or any workflow that would otherwise ask for configuration piecemeal during execution.

## Core Rule

All required configuration must be discovered, classified, and confirmed before execution starts. Do not begin POC or implementation and then repeatedly ask the user for configuration in the middle of the run.

## What Counts As Configuration

| Type | Examples |
| --- | --- |
| Project/path | project root, artifact root, output directory, temp directory, submodule path |
| Runtime/toolchain | language version, package manager, build tool, browser, native toolchain, codegen, MCP server |
| Commands | install, dev, test, lint, build, package, verifier, smoke test |
| Dependency/source | package, SDK, framework, repo URL, target ref, license/security policy |
| External service | API endpoint, cloud account, Git host, Weixin/GitHub/search platform, browser session |
| Credential boundary | env var name, credential helper, local login/session, SSH agent; never ask for secret values |
| Validation | expected signal, artifact path, log marker, screenshot, report, status command |
| Authorization | file writes, Git index writes, submodule writes, network access, external side effects |

## Readiness Table

Use a table like this in the plan, artifact, or handoff:

| Item | Type | Required? | Source | Status | Confirmation | Fallback/Stop |
| --- | --- | --- | --- | --- | --- | --- |
| Project root | path | yes | user/repo | confirmed | yes | stop |
| Test command | command | yes | package.json/docs | confirmed | yes | skip with risk |
| API key env var | credential boundary | yes | `.env.example`/docs | available/missing/unknown | no secret shown | mock/stop |
| External service | service | optional | user | missing | no | disable feature |

## Steps

1. Auto-discover first: read project config, docs, package scripts, `.env.example`, existing code, `.gitmodules`, lockfiles, CI, or workflow files before asking the user.
2. Classify each item as `required`, `optional`, `assumed`, `unknown`, or `not needed`.
3. Confirm required and unknown items together in one readiness checkpoint.
4. Never ask the user to paste secrets. Confirm only secret handling mode: env var, credential helper, local login, SSH agent, system keychain, or intentionally unavailable.
5. If required config is missing, stop before POC/implementation/build/external call and provide fallback options.
6. Record confirmed configuration in the current plan, design, README, checklist, operation record, or delivery artifact.
7. During execution, do not ask for new configuration unless a new requirement appears; if that happens, pause and rerun the gate.

## Blocking Rule

```text
If required configuration is missing or unconfirmed:
  -> stop before POC / implementation / build / external call / submodule write
  -> output missing config list and fallback options
  -> do not proceed by asking piecemeal during execution
```

## Anti-Patterns

- Starting implementation and asking for env vars, paths, commands, credentials, or service endpoints midway.
- Treating missing config as a code bug before the readiness gate is complete.
- Asking for secrets directly instead of checking credential boundaries.
- Re-asking for config that can be parsed from files or previous confirmed artifacts.
- Proceeding with a POC whose validation command or success signal is unknown.
