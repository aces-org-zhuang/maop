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

| Item | Type | Required? | Source | How to obtain | Status | Confirmation | Fallback/Stop |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Project root | path | yes | user/repo | current workspace, user-provided path, or repo root detection | confirmed | yes | stop |
| Test command | command | yes | package.json/docs | read package scripts, Makefile, CI workflow, README, or ask user to choose one listed option | confirmed | yes | skip with risk |
| API key env var | credential boundary | yes | `.env.example`/docs | user creates provider token outside chat, stores it in env/keychain/credential helper, then confirms env var name only | available/missing/unknown | no secret shown | mock/stop |
| External service | service | optional | user/docs | service dashboard, local config, CLI login, browser session, or documented endpoint | missing | no | disable feature |

## How To Help Users Obtain Values

Always provide an acquisition path for missing required or unknown configuration. Do not only say "provide X".

| Config type | Preferred acquisition path | What to ask/confirm | What not to ask |
| --- | --- | --- | --- |
| Project/path | Detect current repo root, inspect known artifact folders, or propose a default path. | Confirm chosen path and whether writes are allowed. | Do not ask the user to design directory structure when the repo has a convention. |
| Commands | Read `package.json`, `Makefile`, `pyproject.toml`, CI workflows, README, docs, or existing scripts. | Ask user to choose from discovered commands if multiple are plausible. | Do not invent commands or ask before checking project files. |
| Environment variables | Read `.env.example`, docs, config schema, code references, CI variable names. | Ask user to confirm env var name and whether it is already available locally. | Do not ask for secret values in chat. |
| API tokens | Point user to the provider dashboard/docs and ask them to store the token in env/keychain/credential helper. | Confirm storage method and variable name. | Do not request token text, screenshots, cookies, or private keys. |
| Git credentials | Use local Git credential helper, SSH agent, existing remote access, or `git ls-remote` diagnostics. | Confirm access method: HTTPS credential helper, SSH key/agent, local repo, or unavailable. | Do not ask for passwords, PATs, or SSH private keys. |
| Browser/session | Use existing local browser/session only if allowed, otherwise stop or provide manual fallback. | Confirm whether browser automation and local session access are allowed. | Do not ask for cookies or login credentials. |
| External endpoints | Read config/docs, service dashboard, local env, or user-provided endpoint. | Confirm endpoint, environment name, and network access boundary. | Do not guess production endpoints. |
| Dependency versions | Read lockfiles, package manifests, release tags, docs, or selected design artifact. | Confirm target version/ref if multiple are viable. | Do not use latest by default for required dependencies without saying so. |
| Validation signals | Read tests, verifier docs, CI, package scripts, existing artifacts, or define a minimal success signal. | Confirm success signal and fallback if validation cannot run. | Do not claim completion without a verifiable signal. |

## Steps

1. Auto-discover first: read project config, docs, package scripts, `.env.example`, existing code, `.gitmodules`, lockfiles, CI, or workflow files before asking the user.
2. Classify each item as `required`, `optional`, `assumed`, `unknown`, or `not needed`.
3. For every missing required or unknown item, provide a concrete acquisition path before asking the user to confirm it.
4. Confirm required and unknown items together in one readiness checkpoint.
5. Never ask the user to paste secrets. Confirm only secret handling mode: env var, credential helper, local login, SSH agent, system keychain, or intentionally unavailable.
6. If required config is missing, stop before POC/implementation/build/external call and provide fallback options.
7. Record confirmed configuration and acquisition paths in the current plan, design, README, checklist, operation record, or delivery artifact.
8. During execution, do not ask for new configuration unless a new requirement appears; if that happens, pause and rerun the gate.

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
