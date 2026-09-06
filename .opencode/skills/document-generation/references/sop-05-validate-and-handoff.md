# SOP-05 Validate and Handoff

## Goal

在成功、阻塞或失败退出前验证文档、引用、模板、状态和 CLI 产物。

## Checks

- `SKILL.md` frontmatter 可解析且入口不超过 300 行。
- SOP 编号连续且索引中的文件真实存在。
- 目标路径匹配 `.aces/features/<k-case>`，且一次任务只有一个 `document.md`。
- 文档 YAML 头部包含 `title`、`version`、`author`、`date`、`last-update`、`status`。
- 占位符格式统一为 `{name}`；标题层级合法。
- 表格保持 Markdown Table；图形内容保持 fenced ASCII block，不要求 LLM 改写。
- 运行 `python scripts/doc_cli.py validate <document_dir>`。
- 记录验证输出、未执行的外部动作和最终 RED。

## Handoff

交付目标文档路径、`.doc-state.json`、模板路径、最近一次 CLI 命令和验证结果。失败时保留日志，不伪造成功；冲突时回到 `status` 或 `lock` 检查。Exit 前将 todo/status 更新为 `succeeded`、`blocked` 或 `failed`，最后为 `exited`。
