# Skill 与 document-generation 集成经验

## 状态

当前有效。

## 目标

当其他 skill 需要生成、扩展或修订结构化文档时，优先集成 `document-generation`，不要在各 skill 内重复实现文档状态管理、模板渲染、段落更新和校验逻辑。

## 集成原则

- 其他 skill 只定义本领域的文档目标、步骤计划、字段契约和完成条件。
- `document-generation` 负责单一真相源、`.doc-state.json` 状态、文档渲染、局部更新、模板目录和 validate。
- 每次任务只允许一个 `document_dir` 和一个目标文档名；`.doc-state.json` 是同一文档的机器状态，不是第二份文档。
- 领域 skill 不得直接手写第二份 Markdown 报告作为最终产物；如需预览或草稿，也必须回写到同一 `document_dir`。
- 领域 skill 通过 `--steps-plan` 注入渐进步骤，通过 `--document-name` 注入领域文档名，例如 `fix-rca-trace.md`。
- 领域 skill 的 SOP 应说明何时调用 `init`、`next-step`、`update`、`validate`，但不要复制 `doc_cli.py` 的实现细节。
- 完成态以 `document-generation` 的 `next_step=complete` 和 validate 结果为准；领域 skill 可以追加业务完成条件，但不能跳过 fresh validation。

## 推荐集成形态

```text
领域 skill
  -> 确认唯一 document_dir/document_name
  -> 提供 templates/<domain-steps-plan>.json
  -> 调用 document-generation init --document-name ... --steps-plan ...
  -> 循环读取 next-step 并提交结构化 JSON update
  -> validate 通过后执行领域验收
```

## 适用场景

- RCA、PRD、设计方案、实现证据、调试记录、评审报告等需要渐进生成和后续修订的文档。
- 多个 skill 都需要“先建文档骨架，再按步骤补内容，再统一校验”的流程。
- 需要避免 PowerShell 或 shell 直接传复杂 JSON 导致转义、编码或引号破坏的场景；优先使用 UTF-8 JSON 文件作为 `update` payload。

## 不适用场景

- 一次性最终回复，不需要落盘和后续修订。
- 已有稳定专用格式或外部系统是唯一真相源，例如 GitHub issue、第三方知识库或数据库记录。
- 研究过程材料；这类内容应进入 `vendor/research/aces-research/`，不进入主仓 docs。

## 防重复造轮子检查

新增或修改 skill 时，如果出现以下需求，先集成 `document-generation`：

- 需要创建 Markdown 文档并持续更新。
- 需要记录文档生成进度、当前步骤、下一步提示或完成态。
- 需要局部替换段落、表格、ASCII 图或占位符。
- 需要模板目录、文档目录隔离、validate 或交付前一致性检查。

只有当 `document-generation` 的 CLI 契约无法表达需求时，才在领域 skill 中增加新能力；新增能力应优先反哺到 `document-generation`，而不是在领域 skill 内复制一套文档引擎。

## 已验证经验

- `bugfix-rca` 通过 `fix-rca-trace.md` 和 `rca-steps-plan.json` 集成 `document-generation`，把 RCA 领域步骤留在 RCA skill，把文档状态和渲染交给 CLI。
- `doc_cli.py init --document-name ... --steps-plan ...` 可以为领域 skill 建立自定义文档名和步骤计划。
- `next-step` 返回当前步骤契约，领域 skill 应按该契约生成 JSON payload。
- `update` 会校验 `step_id`、`allowed_blocks` 和 schema，并推进下一步。
- `next_step=complete` 后继续 `update` 应被拒绝，避免完成态文档被隐式篡改。
