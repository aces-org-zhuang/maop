---
name: product-definition
description: 必须用于产品定义、PRD、MVP、角色、Use Case、用户场景、功能范围、验收标准、需求澄清、需求修订和轻量竞品/差异化分析。用户说“写 PRD”“沉淀需求”“角色和用例”“验收标准太虚”“产品想法”“轻量竞品分析”“不要进入长期研究”时优先使用本技能；不要用于代码实现、架构定稿或长期研究课题。
---

# Product Definition

本技能用于把原始想法、问题描述或业务目标沉淀为可验证、可交付、可追踪的产品定义。`SKILL.md` 只做路由；具体步骤按需读取 `references/sop-*.md`、模板和检查清单。

## 触发后先做什么

1. 读取 `references/sop-00-intake.md`，判断本次是完整产品定义、PRD 生成、需求修订、轻量竞品分析，还是只补齐验收标准。
2. 若问题边界、用户、目标、约束或成功标准存在复杂不确定性，先使用 `reasoning-map` 推演影响面。
3. 根据 Stage Router 只读取当前需要的 SOP。不要把所有 SOP 一次性载入。
4. 跨阶段需求、PRD、MVP 或会沉淀稳定产品知识时，按 `development-workflow/references/knowledge-handoff-gate.md` 执行 Knowledge & Handoff Gate：读取最小 docs/既有材料，维护 Reuse Ledger，并在交给 `technical-design` 前产出 Product Handoff Packet。
5. PRD、MVP 或需求范围定版前必须先建立角色 -> Use Case -> 验收信号主轴；功能列表只能挂到明确角色和用例下，不能以离散 feature 清单替代产品中心。
6. 若需要深度外部证据、开源仓对比、论文级证据包或长期课题沉淀，转入 `research`；普通 PRD 竞品扫描不自动进入研究工作区。
7. 若需要真实前端界面、原型、图表、slides 或其他表达产物，转入 `expression-delivery`；本技能只负责产品定义和 prototype brief。
8. 生成完整 PRD、产品定义文档或长需求清单前，先执行 Preview Gate；除非用户明确要求确认、关键产品目标/用户/成功标准无法推断，或继续会改变已确认范围，否则记录假设并继续。预览可用 ASCII Product Sketch、需求地图、验收表格、Mermaid 流程或低保真线框，按产物选择。
9. 不要把产品定义请求改派给角色型名称；在 maop 技能体系内，本技能就是 PRD/需求/轻量竞品分析入口。
10. 需求定版、PRD 定版或进入 `technical-design` 前执行 Review Gate，review 分数必须 >=80；低于 80 按 `development-workflow/references/auto-remediation-gate-loop.md` 自动补齐角色、Use Case、范围、场景、验收、风险和假设并复审，硬阻断才询问用户。

## Stage Router

```text
任何产品定义请求
  -> Stage 0 Intake: references/sop-00-intake.md

需求模糊、目标不清、用户或场景缺失
  -> Stage 1 Problem Framing: references/sop-01-problem-framing.md

需要用户旅程、场景、边界和约束
  -> Stage 2 User Scenario: references/sop-02-user-scenario.md

需要功能、非功能需求、优先级和验收标准
  -> Stage 3 Requirements Definition: references/sop-03-requirements-definition.md

需要轻量竞品、差异化、市场或创新分析
  -> Stage 4 Lightweight Market Analysis: references/sop-04-lightweight-market-analysis.md

需要 PRD、产品定义文档或需求交付物
  -> Stage 5 PRD Generation: references/sop-05-prd-generation.md

已有产物需要评审、修订或补漏
  -> Stage 6 Review and Revision: references/sop-06-review-and-revision.md
```

## 通用原则

- 保留原始输入和用户真实意图，不把用户的建议方案直接当成最终需求。
- 分离问题、用户、场景、约束、需求和实现方案；产品定义阶段不提前定技术架构。
- 产品定义以角色和 Use Case 聚合需求；每个核心功能必须回答“哪个角色、在哪个触发条件下、为完成哪个目标、如何验收”。
- 验收标准必须可观察、可测试，避免抽象口号。
- 验收标准不得把未验证的第三方服务、外部平台、外部数据源或人工流程作为唯一成功前提；若依赖外部能力，必须同时写明可控降级、替代验证信号或前置验证任务。
- 产品定版交给技术设计前必须说明已读材料、复用结论、拒绝重复研究路径、归档动作、修订动作和开放 RED 点。
- 长产物前先给低成本预览，避免错误需求滚动传递到设计和实现阶段。
- PRD 修订必须同步标注“已具备 / 待补齐 / 范围外”，避免需求文档描述与当前实现、依赖或验收状态过期。
- 需求定版前必须 review，分数 >=80 才进入设计阶段；不达标时默认自动修复最多 7 轮，连续 2 轮无进展或需要用户关键偏好时才停。
- 若项目已有 PRD 或需求模板，优先遵循项目模板；没有模板时再使用本技能模板。
- 旧项目探索/评审经验只作为可迁移 pattern，不作为跨项目硬规则。

## 资源索引

- `references/sop-00-intake.md`: 输入归类、范围判定和既有材料检查。
- `references/sop-01-problem-framing.md`: 问题、目标、用户和约束澄清。
- `references/sop-02-user-scenario.md`: 用户场景、边界和流程梳理。
- `references/sop-03-requirements-definition.md`: 功能、非功能需求和验收标准。
- `references/sop-04-lightweight-market-analysis.md`: 轻量竞品、差异化和创新分析。
- `references/sop-04b-innovation-opportunity.md`: 轻量创新机会识别，承接旧综合创新分析中的可迁移产品定义部分。
- `references/sop-05-prd-generation.md`: 产品定义或 PRD 落稿。
- `references/sop-06-review-and-revision.md`: 完整性评审、修订和追踪。
- `references/pattern-product-exploration.md`: 旧项目产品探索的可迁移模式。
- `templates/`: 可选产物模板。
- `templates/product-sketch.md`: 长 PRD 前的产品预览模板；ASCII 只是默认形式之一。
- `checklists/`: 质量检查清单。

## 交付标准

交付时说明：已确认的问题/目标/用户/场景、需求范围、验收标准、仍未闭环的问题、引用的既有项目规范或外部证据，以及建议进入 `technical-design` 或 `implementation-delivery` 的条件。
