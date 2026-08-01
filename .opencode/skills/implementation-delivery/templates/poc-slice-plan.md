# POC Slice Plan

```text
POC Slice
  Goal
    -> <smallest observable behavior to prove>

  Target Files
    -> <generic file/module category, or explicit unknown>

  Vertical Path
    -> input -> core change -> observable output

  Validation Signal
    -> <test/build/typecheck/manual check>

  Rollback / Risk
    -> <how to back out or contain risk>

  Stop Condition
    -> <what failure means pause or redesign>
```

Do not insert project-specific paths, product names, runtime systems, gateways, or toolchain names unless the user input explicitly provides them. If the design is missing, mark targets as `unknown until design is provided` instead of guessing from the current repository.
