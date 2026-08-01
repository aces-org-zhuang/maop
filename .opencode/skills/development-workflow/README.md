# Development Workflow Index

本索引用于说明 maop 中通用研发、表达和知识发现流水线技能的边界和推荐顺序。`SKILL.md` 是自动触发入口；本 README 只做维护索引。

## 推荐顺序

```text
产品/需求不清
  -> product-definition

需求已确认，需要技术方案
  -> technical-design

设计或任务已明确，需要代码、验证或交付
  -> implementation-delivery

需要 UI、原型、图表、slides、图片或多模态表达产物
  -> expression-delivery

需要外部资料、技术链接、微信文章、微信关键词搜索、学习资源、趋势发现、创新机会或 tool/skill 查找
  -> research
```

## 技能边界

- `product-definition`: 把想法、业务目标、MVP、PRD、用户场景、功能范围和验收标准沉淀为产品定义；高成本 PRD 前先做 Preview Gate。
- `technical-design`: 把已确认需求转为技术方案、接口/数据/状态设计、变更边界、风险和验证策略；高成本设计前先做 Reasoning Gate 和 Preview Gate，必要节点 Review Gate >=80。
- `implementation-delivery`: 执行代码实现、bugfix、测试验证、代码审查和交付摘要；真实脚本/高成本实现前先做 Reasoning Gate，高风险实现前先做 POC Gate，交付前 Review Gate >=80，完成声明前必须有 Verification Gate。
- `expression-delivery`: 执行前端 UI、原型、图表、HTML slides、图片和多模态表达产物；高成本生成前必须 Preview Gate，复杂视觉/交互/渲染前先 Reasoning Gate，交付前 Review Gate >=80 和 Verification Gate。
- `research`: 执行基于 research_root 的外部资料、技术链接、微信文章、微信关键词搜索、学习资源、趋势发现、工具/skill 发现、创新机会、证据包和论文/仓库研究；支持只执行本次需要的 path。

## 与 maop 既有技能的关系

- 复杂推演、根因、影响面和时序问题使用 `reasoning-map`。
- 深度研究、开源仓库对比、证据包和论文级材料使用 `research`。
- 外部资料、技术链接、微信文章、微信关键词搜索、学习资源、趋势发现、创新机会或 tool/skill 查找使用 `research`。
- 前端视觉、真实界面、原型、架构图、时序图、状态图、DFD、演示型 HTML slides、图片和多模态表达使用 `expression-delivery`。
- 只要表达产物时直接使用 `expression-delivery`，不要进入完整 `technical-design` 或 `implementation-delivery` 主流程。
- 项目初始化、AGENTS、docs、研究区和 `.opencode` 桥接使用 `project-init-manager`。

## 项目 AGENTS.md 引导建议

项目初始化时可把下面的简短规则写入根 `AGENTS.md`：

```text
## 研发流水线引导

- 需求、PRD、用户场景、功能范围或验收标准不清时，优先使用 `product-definition`。
- 需求已确认但需要架构、接口、数据、状态、风险或验证策略时，优先使用 `technical-design`。
- 设计或任务已明确，需要实现、bugfix、测试、代码审查或交付摘要时，优先使用 `implementation-delivery`。
- 涉及复杂影响面、根因、时序或跨模块取舍时，先使用 `reasoning-map`。
- 外部资料、技术链接、微信文章、微信关键词搜索、学习资源、趋势发现、创新机会或 tool/skill 查找时，优先使用 `research`。
- 深度研究、开源仓库对比或证据包进入 `research`；普通产品/技术判断不要默认写入研究工作区。
- 高成本产物前先做 Preview Gate；预览形式可为 ASCII、Mermaid、wireframe、HTML preview、状态机图、数据流图或表格草案。
- 必要节点执行 Review Gate，review 分数 >=80 才能进入下游或完成声明。
- 高风险实现前先做 POC Gate；完成声明前必须有 Verification Gate。
- 用户要求 90%+ 置信度时，必须给出 eval、验证证据和未闭环风险。
```

## 全链路质量门禁

- Reasoning Gate: 架构、跨模块、根因、异步时序、影响面、需求不确定、方案取舍、真实脚本运行、构建验证或高成本实现前必须使用 `reasoning-map` 做低成本推演预检；它能在真实运行前减少失败率，但不替代 Preview Gate 和 Verification Gate。
- Preview Gate: 高成本产物前先确认低成本预览，形式可以是 ASCII、Mermaid、wireframe、HTML preview、状态机图、数据流图或表格草案。
- Review Gate: 需求定版、设计定版、复杂预览确认、高风险 POC 后和交付前必须 review，分数 >=80 才能进入下游或完成声明。
- POC Gate: 高风险实现、未知依赖、复杂交互、多模态生成、性能/算法不确定时先做 POC 或等价薄切片验证。
- Verification Gate: 声称完成前必须有本轮 fresh evidence。
- Confidence Gate: 用户要求 90%+ 置信度时，必须给出 eval、验证证据和未闭环风险。

## 约束

这些流水线技能不要求项目采用固定目录、固定评审规则、固定阶段数量或特定自动化平台。项目已有流程优先；没有流程时再使用技能内的模板和 checklists。
