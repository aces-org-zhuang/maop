# Workbench Runtime Feedback Plane

This repository exposes a project-local MCP server named `workbench`.

When working in this repo, prefer the Workbench MCP tools for feedback and verification. MCP exposes abstract tools only; concrete Workbench actions are CLI subcommands dispatched through `workbench.execute_subcommand`.

- Use `workbench.help` for CLI help text.
- Use `workbench.list_subcommands` and `workbench.describe_subcommand` to inspect available Workbench subcommands.
- Use `workbench.execute_subcommand` for all concrete actions, such as `get-environment-status`, `get-workspace-changes`, `get-electron-status`, `doctor-workspace`, `run-build`, `run-tests`, `run-verifier`, `get-latest-feedback`, and `get-artifact-summary`.

If MCP is unavailable, read the fallback guide and facts generated under `.workbench/context/` and `.workbench/latest/`.
Do not treat terminal text as the final pass/fail signal; verifier reports and artifacts are the final facts.
