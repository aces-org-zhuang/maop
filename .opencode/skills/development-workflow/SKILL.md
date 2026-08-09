---
name: development-workflow
description: 必须用于判断研发请求应进入需求、设计、实现还是表达产物阶段，并建立全链路质量门禁。用户要求“从需求到设计到实现”“完整研发流程”“先判断该用哪个技能”“不要让错误滚动放大”“POC 全流程”“需求/设计/实现/验证串起来”“高成本产物前先预览”“复杂 Mermaid/前端/多模态先确认”“置信度 90%+”时优先使用本技能；本技能只做路由和控制点确认，不替代 product-definition、technical-design、implementation-delivery 或 expression-delivery。
---

# Development Workflow

本技能是 maop 通用研发流水线总入口。它只负责判断阶段、安排控制点和交接，不生成完整 PRD、完整技术设计、生产代码或表达产物。

## 触发后先做什么

1. 判断用户请求处于哪个阶段：产品定义、技术设计、实现交付、表达产物，或跨阶段 POC。
2. 若跨阶段执行，先安排质量门禁：Reasoning Gate、Configuration Readiness Gate、Preview Gate、Review Gate、POC Gate、Verification Gate、Confidence Gate 和 Auto-Remediation Gate Loop。
3. 明确每一段应转入的专门技能：`product-definition`、`technical-design`、`implementation-delivery`、`expression-delivery`、`research`。
4. 跨阶段或会产生稳定知识的工作必须执行 Knowledge & Handoff Gate：按 `references/knowledge-handoff-gate.md` 读取最小 docs/上游 packet，记录 Reuse Ledger，明确 Archive Gate、Revision Gate 和下游 Handoff Packet。
5. 遇到复杂根因、时序、影响面、不确定方案、高成本生成、真实脚本运行、构建验证或跨模块修改前，先使用 `reasoning-map` 做低成本推演预检，减少真实执行失败率。
6. 委派 subagent 前必须执行 Delegation Quality Gate：按 `references/delegation-quality-gate.md` 先做前置防错决策、上下文隔离、返回契约和合成门禁；若条件不足或返回不合格，fallback 到主 agent 收敛处理。
7. 大范围检索、代码/文档探索、候选扩展、证据抽取或独立评审可按 `references/subagent-context-budgeting.md` 使用 subagent Task；主 agent 保留 reasoning-map、收敛、评审和最终决策责任。
8. 遇到深度研究、开源仓库对比或证据包时，转入 `research`。
9. 遇到外部资料、技术链接、微信文章、微信关键词搜索、学习资源、趋势发现、工具/skill 查找、创新机会或研究沉淀时，转入 `research` 并先创建或续接 `research_root`。
10. 用户只要求流程图、时序图、架构图、状态图、前端 UI、原型、HTML slides、图片或其他表达产物时，转入 `expression-delivery`，不要展开完整 technical-design 或 implementation-delivery 主流程。
11. 用户要求 90%+ 置信度时，必须给出 eval、验证证据和未闭环风险；不能只口头声明置信度。
12. 用户要求复杂 Mermaid、前端界面、幻灯片、多模态图像、长文档或其他高成本产物时，必须显式经过 Preview Gate；如果同时涉及复杂影响面、根因、时序或方案取舍，顺序是 Reasoning Gate -> Configuration Readiness Gate -> Preview Gate -> Review Gate -> Generation -> Verification Gate。
13. 必要节点需要 Review Gate：需求定版、设计定版、复杂图/前端/多模态预览确认、高风险 POC 后、交付前 review 分数必须 >=80；低于 80 按 `references/auto-remediation-gate-loop.md` 自动修复并复审，不默认停下来等用户继续。
14. 不要把本技能变成万能执行技能；路由完成后交给对应专门技能。

## Stage Router

```text
想法、需求、PRD、用户场景、范围、验收标准不清
  -> product-definition
  -> 控制点: Preview Gate

需求已确认，需要架构、接口、数据、状态、风险、验证策略
  -> technical-design
  -> 控制点: Reasoning Gate when complex + Preview Gate + Review Gate

设计或任务已明确，需要代码、bugfix、测试、审查、交付摘要
  -> implementation-delivery
  -> 控制点: Reasoning Gate before high-cost execution + POC Gate when risky + Review Gate + Verification Gate

只需要图表，不需要完整方案
  -> expression-delivery

只需要 UI、原型、slides、图片、多模态或其他表达产物
  -> expression-delivery

需要外部资料、技术链接、微信文章、微信关键词搜索、学习资源、趋势发现、创新机会或 tool/skill 查找
  -> research

跨阶段 POC 或完整研发流程
  -> product-definition: Preview Sketch
  -> technical-design: Preview Sketch
  -> implementation-delivery: POC Slice Plan when implementation risk is high
  -> expression-delivery: visual/prototype/diagram/slides output when needed
```

## Quality Gates

```text
Workflow Control
  Reasoning Gate
    -> use reasoning-map for complex impact, root cause, async order, uncertainty, tradeoff, or high-cost execution preflight
    -> run before real scripts/builds/generation/implementation when failure cost is high
    -> does not replace Preview Gate for expensive artifacts

  Configuration Readiness Gate
    -> confirm required paths, commands, env/credential boundaries, external services, dependencies, validation signals, and write/network authorization before POC, implementation, build, packaging, verification, or external calls
    -> auto-discover from project files first; for missing required items, provide how to obtain the value and ask the user once, never piecemeal during execution
    -> follow references/configuration-readiness-gate.md

  Preview Gate
    -> confirm a low-cost preview before expensive artifacts
    -> forms: ASCII sketch | Mermaid | wireframe | HTML preview | state diagram | table draft
    -> primary gate for Mermaid, frontend UI, slides, multimodal output, PRD, design docs, and long artifacts
    -> must be named explicitly even when Reasoning Gate runs first

  Review Gate
    -> review necessary checkpoints before downstream work or completion
    -> score must be >=80; otherwise auto-remediate and review again

  Auto-Remediation Gate Loop
    -> gate failure means repair and rerun, not stop by default
    -> max_auto_remediation_rounds = 7; stop early after 2 consecutive no-progress rounds
    -> stop only on hard blockers: missing required config, missing authorization, unavailable external boundary, user tradeoff, scope change, exhausted rounds
    -> follow references/auto-remediation-gate-loop.md

  POC Gate
    -> validate high-risk implementation with a thin vertical slice or equivalent proof

  Verification Gate
    -> require fresh evidence before claiming completion

  Confidence Gate
    -> require eval, verification evidence, and residual risk notes for 90%+ confidence claims
    -> name the gate explicitly when the user asks for 90%+ confidence

  Knowledge & Handoff Gate
    -> read minimum stable context and upstream packets before broad exploration
    -> archive stable knowledge to docs/, stage notes to guides/, and research materials to research_root
    -> revise stale docs or record Docs stale before downstream handoff
    -> produce Product Handoff Packet, Technical Handoff Packet, or Delivery Evidence Packet
    -> maintain Reuse Ledger to avoid repeated upstream work and repeated research
    -> follow references/knowledge-handoff-gate.md

  Subagent Context Gate
    -> use bounded subagent Task for retrieval, exploration, candidate expansion, extraction, or independent review
    -> main agent keeps final reasoning-map, synthesis, convergence, and decision ownership
    -> follow references/subagent-context-budgeting.md

  Delegation Quality Gate
    -> prefer preventing bad delegation before dispatch: decide, isolate context, define return contract, and protect worktree/submodule boundaries
    -> after return, run Synthesis Gate before accepting findings, edits, or decisions
    -> fallback to main agent when delegation is unsafe, stale, incomplete, conflicting, or outside contract
    -> follow references/delegation-quality-gate.md
```

## 防滚动放大规则

- 未确认需求不要进入技术设计。
- 未确认设计不要进入大范围实现。
- 未确认必需配置不要进入 POC、正式实现、真实脚本、构建、外部服务调用、submodule 写操作或验证。
- 未确认需求或设计不要生成最终表达产物；先用 expression-delivery 做 Preview Gate。
- POC 切片失败时停止扩大实现，回到设计或需求阶段修正。
- Gate 不达标时默认自修复并复检，最多 7 轮；连续 2 轮无实质进展、缺 required 配置/授权、外部边界不可用、需要用户偏好或会改变已确认范围时才停。
- 真实脚本、构建、生成和高成本实现前先做 Reasoning Gate；它比真实运行更低成本，能降低失败率。
- 高成本产物前先做 Preview Gate；预览形式不固定为 ASCII，应按产物选择。
- 必要节点必须做 Review Gate，分数 >=80 才能进入下游或完成声明；低于 80 先自动修复和复审。
- 跨阶段交接必须做 Knowledge & Handoff Gate：先读上游 packet 和最小 docs，不重复上游完整研究；稳定知识归档到 `docs/`，阶段记录入 `guides/`，研究材料入 `research_root`。
- 委派 subagent 必须先做 Delegation Quality Gate；默认用前置防错减少错派、串上下文、越权写入和错误合成，失败时由主 agent fallback 兜底。
- 仓库外状态变更必须以当前环境真实可验证结果为准，不能用文字交付伪装完成。
- 项目已有流程优先；没有流程时使用三个专门技能的模板和 checklists。
