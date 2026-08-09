---
name: technical-design
description: 必须用于技术设计、架构影响面、技术方案、技术选型、依赖选型、开源库/框架/仓库评估、GitHub repo 候选对比、接口设计、数据/状态设计、变更边界、兼容性风险、验证策略和实施切片。用户说“需求已确认”“不要写代码”“先设计接入现有系统”“接口和状态”“验证策略”“选哪个库/框架/仓库”“开源项目评估”时优先使用本技能；不要用于产品方向判断、代码实现或项目初始化。
---

# Technical Design

本技能用于把已确认的需求转成可实现、可验证、可追踪的技术方案。`SKILL.md` 只做路由和交付约束，阶段步骤按需读取 `references/sop-*.md`。

## 触发后先做什么

1. 读取 `references/sop-00-intake.md`，确认需求输入、项目上下文和设计范围。
2. 先执行 `development-workflow` 的 Delegation Quality Gate，把前置防错作为主路径：判断是否必须委派、可选委派或禁止委派，并在委派前写清 Source Map、Interface/State、Option/Risk 和 Verification 四个 lens 的输入、输出字段和 stop 条件；fallback 只用于兜底，不得替代主路径证据。
3. 涉及复杂影响面、跨模块关系、异步时序、兼容性、架构、路线或根因不明的设计取舍时，先使用 `reasoning-map`，并对照 `checklists/design-governance.md` 执行事前推演门禁；进入下一设计环节前，关键结论置信度必须 >=90%，低于 90% 时只能输出假设、风险和验证动作，不能定版或推进实现。
4. 代码/文档探索、候选扩展、依赖初筛、方案局部评审可使用 subagent Task；使用前按 `development-workflow/references/subagent-context-budgeting.md` 和 Delegation Quality Gate 定义边界、lens、return contract 和证据字段，最终架构、技术路线、primary 依赖和 Review Gate 由主 agent 决定。
5. 跨阶段设计、架构定版或 implementation handoff 必须按 `development-workflow/references/knowledge-handoff-gate.md` 执行 Knowledge & Handoff Gate：优先消费 Product Handoff Packet，维护 Reuse Ledger，并在交给 `implementation-delivery` 前产出 Technical Handoff Packet。
6. 只要设计面向既有代码仓、模块接入、重构、能力扩展或 implementation handoff，必须先确认源码目录结构和相关入口文件；技术方案必须映射到现有目录/模块 owner，并说明新增、修改、禁止触碰的目录边界。无法确认源码结构时，不得定版架构或实施切片，只能输出待补证设计。
7. 进入 POC、implementation handoff、真实构建/验证设计或外部服务接入前，按 `development-workflow/references/configuration-readiness-gate.md` 统一确认必需路径、命令、依赖、版本锁、环境变量/凭据边界、外部服务、验证信号和授权；缺失 required 配置时只输出补证/降级方案，不推进下游。
8. 需要图表、原型或其他表达产物时转入 `expression-delivery`；本技能决定是否需要表达产物，`expression-delivery` 决定形式和质量。
9. 需要技术选型、依赖选型、开源库/框架/仓库评估或 GitHub repo 候选对比时，使用本技能的 Selection Evaluation 子阶段；缺候选时先转入 `research` 的 Discovery Path 发现候选，深度开源实现洞察或证据包也转入 `research`。本技能的开源选型面向解决方案依赖引入，不等同于 research 的论文/样本仓库选择。
10. 如果项目缺少基础治理、目录规则或 `.opencode` 桥接，转入 `project-init-manager`，不要在本技能中重建初始化规则。
11. 生成完整技术设计或实施切片前，先执行 Preview Gate；除非用户明确要求确认、required 配置/授权缺失、关键 tradeoff 需要用户偏好，或继续会改变已确认架构方向，否则记录假设并继续。预览可用 ASCII/Mermaid 架构图、时序图、状态机图、DFD、接口草案或低保真交互草图。
12. 当用户明确要求“先只输出草图 / 不要完整设计 / 不要写代码”时，不做仓库探索、不读取大量文档；只基于已给输入生成预览和待确认假设。
13. 用户未提供项目专有系统名称、路径或运行时能力时，草图必须保持跨项目中性；不要引入当前仓库的产品名、目录、运行时、网关或工具链。
14. 不要把技术设计请求改派给角色型名称；在 maop 技能体系内，本技能就是需求确认后的设计入口。
15. 设计定版、进入实现或高风险 POC 前执行 Review Gate，review 分数必须 >=80，`checklists/design-governance.md` 关键项必须通过，Delegation Quality Gate 和 Configuration Readiness Gate 必须通过，且关键架构/路线/选型结论置信度必须 >=90%；低于门槛按 `development-workflow/references/auto-remediation-gate-loop.md` 自动补 reasoning-map、选型矩阵、governance、build map、风险和验证策略并复审，硬阻断才询问用户。
16. 设计准备进入 `implementation-delivery` 前，必须输出 Implementation Handoff Mini-Spec 和 90% Confidence Evidence Map；交接至少覆盖 Source Map、Interface/State、Option/Risk、Verification lens、状态/API/模块/测试/验证/外部未知。任一关键架构、接口、状态、模块边界或验证入口低于 90% 置信度时，不得声明 ready for implementation，只能输出缺口、补证动作和 fallback。

## Delegation Quality Gate

技术设计默认由主 agent 负责定版。subagent 只用于前置防错、证据补强和局部评审，不能替代主 agent 的架构判断。

- Must delegate triggers: 需要跨大量代码/文档建立 Source Map；存在多消费者接口、状态机、异步链路或权限边界；有两个以上可行架构/依赖选项且风险不清；implementation handoff 需要独立验证入口或 90% confidence evidence；用户要求复核高风险设计。
- May delegate triggers: 候选方案资料补全、开源依赖初筛、局部接口契约审阅、测试入口盘点、低成本风险清单补漏。
- Do-not delegate triggers: 最终架构定版、primary 依赖选择、breaking change 决策、用户偏好取舍、Review Gate 打分、是否 ready for implementation；上下文不足以写清 return contract 时也不得委派。
- Source Map lens: 输出 `source_path`、`owner/module`、`entrypoint`、`test_or_config_path`、`evidence_type`、`confidence`、`gap`。
- Interface/State lens: 输出 `contract_or_state`、`producer`、`consumer`、`source_of_truth`、`lifecycle_or_sequence`、`compatibility`、`failure_mode`、`confidence`。
- Option/Risk lens: 输出 `option`、`decision`、`accepted_reason`、`rejected_reason`、`risk`、`mitigation`、`fallback_only_if`、`confidence`。
- Verification lens: 输出 `claim_or_risk`、`verification_method`、`command_or_manual_entry`、`expected_evidence`、`required_before_implementation`、`gap`、`confidence`。
- Lens 输出必须字段级吸收到 Technical Handoff Packet、Implementation Handoff Mini-Spec 和 90% Confidence Evidence Map；未吸收的 subagent 结果只能作为参考，不得支撑 ready 判断。

## Stage Router

```text
任何技术设计请求
  -> Stage 0 Intake: references/sop-00-intake.md

需要理解现有系统、代码位置或项目约束
  -> Stage 1 Context Discovery: references/sop-01-context-discovery.md

需要把需求映射到设计决策
  -> Stage 2 Requirement Trace: references/sop-02-requirement-trace.md

需要比较方案、架构或技术路线
  -> Stage 3 Solution Options: references/sop-03-solution-options.md

需要技术选型、依赖选型、开源库/框架/仓库评估或候选 repo 对比
  -> Stage 3b Selection Evaluation: references/sop-03b-selection-evaluation.md

需要第三方软件、CLI、SDK、服务、容器镜像、二进制、系统包或 source-build 的部署引入设计
  -> Stage 3c Deployment Integration Design: references/sop-03c-deployment-integration.md

需要接口、数据、状态、错误处理或权限设计
  -> Stage 4 Interface Data State: references/sop-04-interface-data-state.md

需要模块变更边界、冻结区或兼容性影响
  -> Stage 5 Change Boundary: references/sop-05-change-boundary.md

需要风险、验证策略和实施切片
  -> Stage 6 Risk Validation Plan: references/sop-06-risk-validation-plan.md

设计准备进入实现、POC 或需要 handoff 给 implementation-delivery
  -> Stage 6 Risk Validation Plan: references/sop-06-risk-validation-plan.md
  -> Template: templates/implementation-handoff-mini-spec.md
  -> Template: templates/validation-plan.md

已有设计需要评审或修订
  -> Stage 7 Design Review: references/sop-07-design-review.md
```

## 通用原则

- 优先遵循项目已有架构、文档、平台抽象、编码约束和设计模板。
- 设计必须能追溯到需求，不用个人偏好替代约束。
- 设计阶段不写生产代码；若用户要求实现，转入 `implementation-delivery`。
- 既有代码仓的技术设计必须先建立源码目录图谱；目录结构是架构约束，不是实现细节。设计输出必须把能力、模块 owner、接口、状态、配置、测试和实施切片落到明确目录或文件类别。
- 技术设计必须复用 Product Handoff Packet 中已确认的角色、Use Case、范围和验收；除非源码事实或用户反馈冲突，不重复产品定义阶段的完整研究。
- 明确变更边界、兼容性、迁移风险和验证方式。
- 设计应优先保持技术栈归一、特性模块唯一归属、依赖唯一性、契约 owner 清晰、数据/状态单一来源、运行时边界可维护和构建复杂度受控。
- 技术选型必须输出候选、推荐理由、拒绝理由、风险和验证动作；缺少候选时先用 `research` 的 Discovery Path 发现，不用猜测补齐。
- 方案、架构、路线和依赖选型推进必须通过 `reasoning-map` 门禁：关键判断置信度 >=90% 才能进入下一设计环节、实现计划或 POC；未达标时保留为暂定方案并列出补证动作。
- subagent 委派必须先通过 Delegation Quality Gate；能用 Source Map、Interface/State、Option/Risk 和 Verification lens 预防错误滚动放大时优先前置委派，fallback 只记录在风险与验证计划中作为兜底路径。
- 开源库/框架/仓库选型默认以项目依赖方式引入，优先声明依赖、锁定版本、满足 license/security 边界并保障项目构建完整性；非必要不侵入修改第三方源码，不把候选仓库复制进项目后自研化，也不把选型评估误当作 research 样本冻结。
- 第三方能力接入遵循 deployment-first：优先服务/API、包、SDK、CLI/binary、镜像、系统包或 pinned submodule；只有证据证明部署引入不足时才设计 source-build、fork/patch 或自研。目录规划必须统一到项目 tech 流水线，不默认复制 `.aces/deploy` 或历史脚本目录。
- POC、implementation handoff、外部服务接入和构建/验证设计前必须通过 Configuration Readiness Gate；不要把路径、命令、env、凭据边界或服务配置留到实现过程中再问。
- Implementation handoff 不是任务列表摘要；必须明确模块/文件域、Source Map、API/契约、状态/source of truth、Option/Risk、测试入口、验证证据和外部未知，确保 `implementation-delivery` 不需要重新猜测设计意图。
- 90% Confidence Evidence Map 必须把关键设计结论绑定到代码、文档、命令、用户确认、subagent lens 输出或外部证据；没有证据来源的结论只能标为假设。
- 长设计前先给低成本预览，避免遗漏影响面后继续放大到实现阶段。
- 复杂影响面、真实脚本运行、构建验证或高成本实现前先用 `reasoning-map` 做推演预检。
- 设计定版前必须 review，分数 >=80 才进入实现阶段；不达标时默认自动修复最多 7 轮，连续 2 轮无进展或遇到 required 配置/授权/用户偏好硬阻断时才停。
- 旧项目设计守护经验只作为可迁移模式，不作为跨项目硬规则。

## 资源索引

- `references/sop-00-intake.md`: 设计范围、输入和上下文判定。
- `references/sop-01-context-discovery.md`: 项目、文档和代码上下文发现。
- `references/sop-02-requirement-trace.md`: 需求到设计决策映射。
- `references/sop-03-solution-options.md`: 方案选项与取舍。
- `references/sop-03b-selection-evaluation.md`: 技术选型、依赖选型、开源库/框架/仓库评估和候选 repo 对比。
- `references/sop-03c-deployment-integration.md`: 第三方能力 deployment-first 引入、镜像、CLI/binary、系统包、source-build fallback 和 tech 流水线目录规划。
- `references/selection/evaluation-workflow.md`: 选型评估详细流程。
- `references/sop-04-interface-data-state.md`: 接口、数据、状态、错误和权限设计。
- `references/sop-05-change-boundary.md`: 模块边界、冻结区、兼容性和迁移。
- `references/sop-06-risk-validation-plan.md`: 风险、验证策略和实施切片。
- `references/sop-07-design-review.md`: 设计完整性评审。
- `references/pattern-design-guards.md`: 旧项目设计守护的可迁移模式。
- `templates/`: 可选设计产物模板。
- `templates/design-sketch.md`: 长技术设计前的设计预览模板；ASCII 只是默认形式之一。
- `templates/implementation-handoff-mini-spec.md`: 进入 `implementation-delivery` 前的最小交接规格，覆盖 Source Map、Interface/State、Option/Risk、Verification、模块、API、状态、测试、验证和外部未知。
- `templates/validation-plan.md`: 90% Confidence Evidence Map，用于把关键设计 claim 映射到证据、验证方式、缺口和 fallback；fallback 只做兜底。
- `templates/selection-matrix.md`: 技术选型候选矩阵模板。
- `checklists/`: 设计质量清单。
- `checklists/design-governance.md`: 技术栈归一、模块归属、依赖唯一性、状态/契约 owner、运行时和构建复杂度治理门禁。
- `checklists/selection-evaluation.md`: 技术选型检查清单。

## 交付标准

交付时说明：需求追踪、当前系统依据、Delegation Quality Gate 结果、Source Map、推荐方案、被拒绝方案、Interface/State 影响、Option/Risk 取舍、变更边界、Verification 策略、实施切片、Implementation Handoff Mini-Spec、90% Confidence Evidence Map，以及是否已具备进入 `implementation-delivery` 的条件。若不具备，必须列出 blocking gaps、补证动作和 fallback。
