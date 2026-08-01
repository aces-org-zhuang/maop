# maop OpenCode

This directory is the maop-owned OpenCode surface.

Project repositories may reference this directory from their own `.opencode/opencode.json`, but should not copy or overwrite these files. Project-specific configuration belongs in the project repository `.opencode/` directory.

## Layout

- `skills/`: maop-owned skills exposed to host projects.

## Boundary

- maop owns files under `vendor/ai/maop/.opencode/` when used as a submodule.
- Host projects own their own `.opencode/` directories.
- Host projects should pin maop through Git submodule commits and update intentionally.
