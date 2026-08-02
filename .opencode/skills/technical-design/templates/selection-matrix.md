# Selection Matrix

Use this template for dependency, framework, library, SDK, or repository selection.

## Context

- Goal:
- Constraints:
- Must-have capabilities:
- Nice-to-have capabilities:
- Disallowed options:
- Artifact root: `{selection_artifact_root}`

## Candidates

| Feature/Capability | Candidate | Source | Adoption form | Why not higher-priority deployment mode | Fit | Health | Maturity | Risk | Integration Cost | Role | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | service/API / package / SDK / CLI-binary / image / system-package / submodule / source-build / fork-patch / self-build |  |  |  |  |  |  | primary / fallback / alternative / rejected |  |

## Top-Down Candidate Space

| Level | Selection question | Candidate set | Add/remove rationale | Remaining RED points |
| --- | --- | --- | --- | --- |
| System architecture | Which solution shape covers the end-to-end capability without unnecessary self-build? |  |  |  |
| Subsystem/module | Which components cover each architecture capability block? |  |  |  |
| Implementation dependency | Which library/SDK/framework/repo should be adopted for the selected module boundary? |  |  |  |

## Expansion and Convergence Log

| Round | Reasoning-map focus | Added candidates | Removed candidates | Scope change | Convergence status |
| --- | --- | --- | --- | --- | --- |
| 1 | System architecture candidate space |  |  | expanded / narrowed |  |
| 2 | Subsystem/module coverage |  |  | expanded / narrowed |  |
| 3 | Implementation dependency fit |  |  | expanded / narrowed |  |

Convergence is reached only when key architecture capability blocks are covered, module boundaries are clear, wheel-rebuilding risk is bounded, candidate differences are compared, each feature/capability has exactly one primary dependency, and remaining RED points no longer block the design goal.

## Primary Uniqueness

| Feature/Capability | Primary dependency | Fallback/Alternative | Rejected same-purpose candidates | Why only one primary |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Recommendation

- Recommended option:
- Why this option:
- Adoption form:
- Why not higher-priority deployment mode:
- Tech pipeline directory plan:
- Rejected alternatives:
- Key risks:
- Validation plan:
- Handoff:

## Software Build Map

Required after dependency selection. Use ASCII or Mermaid and keep the boundary explicit. Put interaction logic and IPO details in tables after the diagram, not inside the diagram.

```text
[First-party component]
  -> [Third-party dependency: name@version, adoption form]
      -> [Build/test/package step]
```

- First-party components:
- Third-party open-source components:
- Adoption forms:
- Tech pipeline directories:
- Version lock locations:
- License/security checkpoints:
- Build/test verification:
- Fork/patch/source-copy risks, if any:

### Example

```text
Software Build Map: Desktop AI Coding Assistant

[First-party: renderer app]
  path: apps/frontend/src/renderer
  consumes:
    -> [Third-party: react@19.x]
       adoption form: package dependency
       lock: apps/frontend/package-lock.json
    -> [Third-party: zustand@x.y]
       adoption form: package dependency
       lock: apps/frontend/package-lock.json

[First-party: electron main]
  path: apps/frontend/src/main
  consumes:
    -> [Third-party: electron@40.x]
       adoption form: package dependency
       lock: apps/frontend/package-lock.json
    -> [Third-party: node-pty@x.y]
       adoption form: native package dependency
       lock: apps/frontend/package-lock.json

[First-party: runtime adapter]
  path: apps/frontend/src/main/runtime-adapter
  consumes:
    -> [Third-party/Open-source: engine submodule@commit]
       adoption form: git submodule or declared local reference
       lock: git submodule commit

[Build chain]
  npm install -> typecheck -> test -> build -> package

[Risk boundary]
  RED if fork/patch/source-copy is required, no stable version lock exists,
  or the dependency cannot pass build/test/package verification.
```

### Component Interaction Logic

| From | To | Interaction | Contract | Failure/Boundary |
| --- | --- | --- | --- | --- |
| renderer app | electron main | UI command invokes IPC/API bridge | typed IPC/preload contract | renderer never imports main-only dependency directly |
| electron main | runtime adapter | main process starts task and subscribes to feedback | task request/feedback event schema | adapter owns engine-specific translation |
| runtime adapter | engine submodule | adapter invokes engine command/API | declared submodule commit and runtime interface | no source copy; fork/patch requires RED risk |
| build chain | all dependencies | package manager installs locked dependency graph | lockfile + build scripts | build/test/package must verify selected dependency |

### Key IPO

| Component | Input | Processing | Output |
| --- | --- | --- | --- |
| renderer app | user action, project state | render workflow, collect command intent | IPC/API request to main process |
| electron main | IPC/API request | validate command, coordinate local services | task start, status, error or result event |
| runtime adapter | task start request, engine config | translate request, invoke engine, normalize feedback | structured feedback/artifacts |
| third-party dependency | declared package/submodule version | provide library/runtime capability | linked module, binary, service or API used by first-party code |
| build chain | source tree, lockfile, config | install, typecheck, test, build, package | verified application artifact |

### Deployment Integration Plan

| Capability | Adoption form | Directory owner in tech pipeline | Config source | Build/install command contract | Verify signal | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
|  | service/API / package / SDK / CLI-binary / image / system-package / submodule / source-build / fork-patch / self-build | existing project scripts/tools/infra/ops/build/docker/artifacts/config path or confirmed new path |  |  |  |  |

Do not default to `.aces/deploy` or copied script trees. Use the project's existing tech pipeline directories first; if none exist, propose a minimal directory plan and confirm it through Configuration Readiness Gate.
