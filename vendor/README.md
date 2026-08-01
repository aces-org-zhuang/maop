# Vendor

This directory stores external repositories, the research workspace, and long-lived vendor resources used by this maop source repository.

## Planned Paths

- `vendor/research/aces-research`: locked research workspace submodule.
- `vendor/runtime/`: runtime or packaging resource repositories.
- `vendor/assets/`: external asset repositories.
- `vendor/harness/`: agent, MCP, verifier, or workflow harness repositories.
- `vendor/external/`: long-lived external repositories that do not fit another category.

## Host Project Reference

Host projects may add maop as `vendor/ai/maop`. This maop source repository must not add itself there.

See `docs/02-development/submodules-index.md` before adding or changing submodules.
