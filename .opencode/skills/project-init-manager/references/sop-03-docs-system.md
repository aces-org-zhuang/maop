# SOP 03: Docs System

## 目标

建立短入口、分层索引、按需读取、可反哺的 `docs/` 体系。`docs/` 保存长期稳定知识，不保存研究过程和一次性长推演。

## 标准目录

```text
docs/
  AGENTS.md
  README.md
  00-overview/
  01-architecture/
  02-development/
  03-runtime/
  04-operations/
  05-contracts/
  06-decisions/
  07-llm/
  08-roadmap/
  failure-modes/
  debugs/
  evidences/
  _templates/
```

`docs/07-llm/operational-experiences.md` 是按需读取的环境/组织作业经验入口，不属于项目规则或业务知识。

不适用的目录可以保留简短 README 和“状态：暂定”，避免未来迁移时失去位置；也可以在极简项目中暂缓创建，但必须在 `docs/README.md` 说明缺省策略。

## 执行步骤

1. 创建 `docs/README.md`，只写快速入口和目录边界。
2. 创建 `docs/AGENTS.md`，只写 docs 写作、索引和 token 规则。
3. 为每个编号目录创建 `README.md`，内容保持短导航。
4. 创建 `docs/failure-modes/index.md`、`docs/debugs/index.md`、`docs/evidences/index.md`。
5. 创建 `docs/_templates/` 中的失效模式、调试记录、实现证据和 ADR 模板。
6. 创建 `docs/07-llm/llm-reading-order.md` 和 `docs/07-llm/doc-update-rules.md`，控制 LLM 按任务读取最小上下文。
7. 从 `templates/operational-experiences.md.template` 生成 `docs/07-llm/operational-experiences.md`，只保存单行、脱敏、去项目化的可迁移作业经验。

## 反哺机制

- 架构事实、长期规则、契约和操作流程进入 `docs/` 对应分层。
- 非研究类阶段性工程记录进入 `guides/`。
- 研究过程、论文、开源对比、候选材料和证据包进入研究区。
- 已复用问题进入 `docs/failure-modes/` 并更新 index。
- 复杂定位过程进入 `docs/debugs/` 并更新 index。
- 需求到实现证据进入 `docs/evidences/` 并更新 index。
- 环境/组织作业经验进入 `docs/07-llm/operational-experiences.md`，每条只占一行并按需读取。

## token 控制

- 不默认读取整个 `docs/`。
- 先读 `docs/README.md`，再按 `docs/07-llm/llm-reading-order.md` 选择 1-3 个目标文档。
- 常读入口保持短，不放长报告、研究过程或历史案例。
- 研究区不进入默认上下文，只有研究任务才读取研究区 index 和目标课题。
- 作业经验不进入默认上下文，只有相似环境作业才读取经验入口。

## 模板

- `templates/docs-README.md.template`
- `templates/docs-AGENTS.md.template`
- `templates/llm-reading-order.md.template`
- `templates/operational-experiences.md.template`
- `templates/doc-update-rules.md.template`
- `templates/failure-modes-index.md.template`
- `templates/debugs-index.md.template`
- `templates/evidences-index.md.template`

## 常见 RED 点

- `docs/README.md` 过长，变成默认上下文负担。
- 子目录新增后未同步索引。
- 把研究过程或论文草稿写进主仓 `docs/`。
- 文档写未来计划但没有标记“状态：暂定”。
- 作业经验入口缺失、包含多行复盘或混入项目规则。
