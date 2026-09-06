# 文档更新规则

## 状态

当前有效。

## 规则

- 代码变更影响架构、运行时、契约、验证流程或 LLM 工作流时，评估是否更新 `docs/`。
- 新增 docs 文件时，必须放入正确目录并同步 README 或 index。
- 新增或修改需要落盘文档的 skill 时，优先复用 `document-generation` 作为唯一文档引擎，并把集成经验写入 `docs/07-llm/skill-document-generation-integration.md`。
- 研究过程、论文、候选材料和开源仓库对比不得写入主仓 `docs/`。
- 非研究阶段记录默认放入 `guides/`。
- 常读入口保持短，不放长推演或历史过程。
- 不确定或未来计划标记为 `状态：暂定`。
- 跨阶段研发工作按 `.opencode/skills/development-workflow/references/knowledge-handoff-gate.md` 执行读取、归档、修订和交接；下游优先读取上游 handoff packet，不默认重复上游研究。

## 归档策略

- 归档到 `docs/`：已经 Review Gate 或 fresh verification 支撑、且会长期影响需求、架构、契约、运行时、验证流程、LLM 工作流、可复用失效模式、复杂调试知识或需求到实现证据的内容。
- 归档到 `guides/`：非研究类阶段记录、一次性工程过程、临时实施说明和未稳定流程。
- 归档到 `vendor/research/aces-research/`：研究过程、论文、开源仓库对比、候选材料、外部资料和证据包。
- 不归档：仅对当前对话有用、未验证、不会复用的临时推演；如必须记录，标为 `状态：暂定` 并写明补证动作。

## 修订记录

- 当前源码事实、验证结果或阶段产物与既有 docs 冲突时，先标为 RED，不得静默依赖过期文档。
- 当前任务依赖 stale docs 时，先修订 docs 或在交付中登记 `Docs stale` 与后续 owner。
- 新增 ADR 更新 `docs/06-decisions/README.md`。
- 新增需求到实现证据更新 `docs/evidences/index.md`。
- 新增可复用失效模式更新 `docs/failure-modes/index.md`。
- 新增复杂调试记录更新 `docs/debugs/index.md`。
- 新增 skill 文档生成集成经验更新 `docs/07-llm/skill-document-generation-integration.md`。
- 交付摘要需说明 `Docs updated`、`Docs stale` 或 `Docs not updated` 的原因。

## 行动前

涉及复杂文档体系变更时，先使用 `reasoning-map` 推演影响面。

## 行动后

复核索引同步、token 控制、根规则与局部规则一致性，并确认 Archive Gate、Revision Gate 和 Handoff Packet 状态已说明。
