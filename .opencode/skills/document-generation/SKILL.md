---
name: document-generation
description: 用于生成、扩展和修订单个结构化文档。触发于“写文档”“生成报告/方案/规范”“更新某段内容”等请求；必须以一个目标文档为唯一真相源，并通过该技能的 scripts/doc_cli.py 渐进驱动、校验和渲染。必须支持文档模板（元数据、YAML头部、标题格式、占位符、MarkdownTable/ASCII图弹性）、文档管理（单一工作目录与状态隔离，避免重复执行冲突）、CLI update 模板。文档名由调用方或报告场景决定，不在通用技能中硬编码。
---
# Document Generation

## 执行模型

选择的基础模型：任务依赖树 + round + loop + dialectical。

LLM 只产生 CLI 所需的结构化 JSON、读取 CLI 返回的下一步提示并执行下一步；CLI 负责状态、校验、段落更新、模板渲染和文档管理。

```text
单一真相源确认
  -> sop-00-intake-and-routing {主流程，绑定一个 workspace/document + template}
  -> doc_cli.py init/status/next-step {CLI 生成渐进提示}
  -> sop-01-cli-driven-generation {按 next-step 逐步提交 JSON}
  -> sop-02-paragraph-update {按 paragraph_id 局部更新并自动 validate}
  -> sop-03-template-management {模板创建/更新}
  -> sop-04-document-management {单一工作目录与状态隔离}
  -> sop-05-validate-and-handoff {主流程 fresh validation 与交付}
       -> {失败且有明确修复动作} loop 回到 CLI next-step
       -> {缺少唯一文档或配置} blocked
```

只有需要独立抽取来源、并行事实核验或对抗性审阅时，才由主 LLM 按明确条件派发边界明确的代理执行对应 SOP；代理不得创建第二份真相源、决定最终文档结构或替代最终验证。纯路由、CLI 调用、最终验证和交付由主 LLM 完成。每个阶段执行前后都更新 todo/status，保留当前文档路径、命令、产物和证据。

当状态流转会影响结果时，委派代理执行 reasoning-map 检查时序边界。

## 核心契约

- **Single source of truth**：一次任务只允许一个 `document_dir` 和一个目标文档定义。`.doc-state.json` 是同一文档的机器状态，不是第二份文档。所有读取、更新、验证、渲染和交付都回归该路径。文档名由状态或调用方约定，不在通用技能中硬编码。
- **Document template**：必须支持 YAML 头部（title、version、author、date、last-update、status）、标题格式（# ## ###）、占位符（{placeholder}）、MarkdownTable 和 ASCII图弹性。
- **Document management**：文档工作目录必须唯一且可复用，目录约束由调用方或场景层定义；`.doc-state.json` 维持同一文档状态。模板文件放在目标工作目录约定的位置。
- **CLI first**：必须调用 `python scripts/doc_cli.py <sub_command> ...`。初始化时可通过 `--steps-plan <json-or-file>` 定义渐进步骤；每步可声明 `step_id`、`instruction`、`next_step`、`allowed_blocks` 和 JSON `schema`。优先使用 `next-step` 获取当前步骤的提交契约；`update` 按当前步骤校验 `step_id`、块类型和 schema 后再推进状态。

## 资源索引

- `references/sop-00-intake-and-routing.md`
- `references/sop-01-cli-driven-generation.md`
- `references/sop-02-paragraph-update.md`
- `references/sop-03-template-management.md`
- `references/sop-04-document-management.md`
- `references/sop-05-validate-and-handoff.md`
- `scripts/doc_cli.py`
- `evals/evals.json` (可选)
