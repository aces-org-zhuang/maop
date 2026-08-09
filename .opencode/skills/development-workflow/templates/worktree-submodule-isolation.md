# Worktree And Submodule Isolation

Use this when delegated work may inspect git state, edit files, or touch submodules.

```text
Repository root:

Allowed file set:

Forbidden file set:

Existing dirty changes to preserve:

Generated files allowed:

Commands allowed:

Commands forbidden:

Submodule paths involved:

Submodule action allowed:

Submodule action forbidden:

Required documentation/index sync:

Return required before writing:
```

Rules:

- Never revert or overwrite unrelated dirty changes.
- Never move a submodule pointer unless explicitly authorized.
- Never commit, amend, push, or create PRs unless explicitly requested.
- Stop if the allowed file set is unclear.
