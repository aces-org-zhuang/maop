# maop OpenCode

This directory is the maop-owned OpenCode surface.

Project repositories may reference this directory from their own `.opencode/opencode.json`, but should not copy or overwrite these files. Project-specific configuration belongs in the project repository `.opencode/` directory.

## Layout

- `skills/`: maop-owned skills exposed to host projects.

## Boundary

- maop owns files under `vendor/ai/maop/.opencode/` when used as a submodule.
- Host projects own their own `.opencode/` directories.
- Host projects should pin maop through Git submodule commits and update intentionally.
- Host project bridge configs should include `../vendor/ai/maop/.opencode/skills` in `skills.paths` and register a `maop-opencode` reference to `../vendor/ai/maop/.opencode`.
- This repository is the maop source repository, so its local `.opencode/opencode.json` points at `./skills` and records `maop-opencode` as the current `.opencode` directory rather than adding a nested `vendor/ai/maop` submodule.
