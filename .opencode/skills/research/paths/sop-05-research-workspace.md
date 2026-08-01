# SOP 05: Research Workspace

统一管理 research workspace、research root 和 README 续点。

## Required README Fields

- title
- slug
- status
- current_paths
- completed_paths
- artifacts
- frozen_decisions
- next_suggestions
- risks
- updated_at

## Path Update Rule

每个 path 完成后更新 README，记录本次新增产物和下一步，不允许只生成文件不更新索引。

## Repository Rule

研究参考开源项目必须作为 Git submodule 加入 `{research_root}/repos/<repo_name>`，不得普通 clone 到主仓目录。
