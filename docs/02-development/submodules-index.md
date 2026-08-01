# Submodules Index

This index records long-lived external repositories used by maop or planned for host-project initialization.

| Path | URL | Status | Boundary | Consumer | Validation |
| --- | --- | --- | --- | --- | --- |
| `vendor/research/aces-research` | `https://github.com/aces-org-zhuang/aces-research.git` | Added at `b2025592f1b5a5b37f1ca538ab6dfcf091e74e36`. | Research workspace for process notes, papers, repo comparisons, and evidence packages. | Research tasks and research skills. | `git submodule status --recursive`. |
| `vendor/ai/maop` | `https://github.com/aces-org-zhuang/maop.git` | Not applicable inside this repository; required for host projects. | maop AI engine submodule with sparse-checkout for `.opencode/` and `README.md`. | Host project `.opencode/opencode.json` bridge. | `git -C vendor/ai/maop sparse-checkout list` should include `/.opencode/` and `/README.md`. |

## Rules

- Add external repositories through Git submodule unless there is a documented reason not to.
- Do not clone research references into the main repository tree.
- Research reference repositories belong under `vendor/research/aces-research/topics/<slug>/repos/<repo_name>`.
- Before updating or removing a submodule, inspect submodule status and avoid touching uncommitted submodule changes.
