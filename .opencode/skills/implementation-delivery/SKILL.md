---
name: implementation-delivery
description: 必须用于实现交付、按设计落地代码、bugfix、测试验证、代码审查、安全/CVE 修复、交付说明、验收闭环和 fresh verification evidence。用户说“实现功能”“按设计实现”“修 bug”“跑测试验证”“交付摘要”时优先使用本技能；不要用于产品定义、架构主设计、项目初始化或声称完成当前环境无法验证的仓库外状态变更。
---

# Implementation Delivery

本技能用于把已确认需求或技术设计落地为代码、测试、验证证据和交付说明。`SKILL.md` 只做路由；具体执行按需读取 `references/sop-*.md`、模板和检查清单。

## 触发后先做什么

1. 读取 `references/sop-00-intake.md`，确认输入是实现、bugfix、验证、代码审查、安全/CVE 还是交付说明。
2. 若缺少产品需求或技术设计，回到 `product-definition` 或 `technical-design`；不要凭空补齐关键需求和架构决策。
3. bug 根因、复杂时序、跨模块影响或安全问题不清时，先使用 `reasoning-map`。
4. 跨阶段实现、代码交付或会产生证据记录时，按 `development-workflow/references/knowledge-handoff-gate.md` 执行 Knowledge & Handoff Gate：优先消费 Technical Handoff Packet，维护 Reuse Ledger，并在交付时产出 Delivery Evidence Packet。
5. 改代码前先执行实现侧 `references/delegation-quality-gate.md`：把 Read-Only Code Exploration、Test Surface、Diff/Risk Review、Conflict Resolution、Evidence Extraction 作为前置防错主路径；fallback 只在 delegation 不可隔离或证据不可用时兜底，不替代前置检查。
6. 大范围代码探索、根因假设收集、测试面发现、独立代码审查或验证证据整理可使用 subagent Task；使用前按 `development-workflow/references/subagent-context-budgeting.md` 和本技能 Delegation Quality Gate 定义边界、Worktree/Submodule Isolation 和 return contract，生产修改、最终修复方案、完成声明和 verification 结论由主 agent 负责。
7. 真实改代码、POC、脚本、构建、测试、外部服务调用、生成、打包或验证前，按 `development-workflow/references/configuration-readiness-gate.md` 统一确认必需路径、命令、依赖、环境变量/凭据边界、外部服务、写入/联网授权、验证信号和回滚方式；required 配置缺失时停止，不在执行中途零散索要。
8. 编码前必须建立 Pre-Code Acceptance Contract：把用户目标、完成边界、验收命令/检查、不可触碰范围、Worktree/Submodule Isolation 和中断续接标记写清楚；如果验收契约无法从需求、设计或代码上下文推出，先提 1 个短问题或输出阻塞项，不直接开写。
9. 若发现任务是中断续接、半成品修复、失败重试或存在未提交/非本人变更，先执行 Interrupted Slice Guard：识别当前切片状态、已完成证据、未完成边界、冲突风险、worktree/submodule 隔离状态和下一步最小安全动作；不得覆盖用户或其他 agent 的进行中工作。
10. 前端视觉、交互、原型或其他表达产物需要高质量设计时，转入 `expression-delivery`。
11. 仓库外状态变更必须以当前环境真实可验证的结果为准；本技能可以生成交付材料，但不能假装完成未执行或无法验证的外部操作。
12. 进入较大或高风险实现前，先执行 POC Gate，确认最小纵向切片、目标文件、验证信号和回滚风险。POC 可以是薄代码切片、交互原型、Mermaid/状态机验证、前端静态 preview、数据转换样例或算法小样。
13. 当用户明确要求“先不要改代码 / 只输出 POC Plan”时，不做文件编辑，不扩大仓库探索；只输出 POC 计划、缺失输入和停止条件，形式可为 ASCII、Mermaid、表格或原型说明。
14. 用户未提供项目专有系统名称、路径或运行时能力时，POC plan 必须保持跨项目中性；不要引入当前仓库的产品名、目录、运行时、网关或工具链。
15. 不要把实现交付请求改派给角色型名称；在 maop 技能体系内，本技能就是实现、修复、验证和交付入口。
16. 真实脚本、构建、生成和高成本实现前先使用 `reasoning-map` 做推演预检；交付前执行 Review Gate，review 分数必须 >=80；测试、构建、POC、review 或 verification 失败时按 `development-workflow/references/auto-remediation-gate-loop.md` 自动修复并重跑，硬阻断才询问用户。

## Stage Router

```text
任何实现、修复、验证或交付请求
  -> Stage 0 Intake: references/sop-00-intake.md

需要实现计划、任务切片或工作顺序
  -> Stage 1 Implementation Plan: references/sop-01-implementation-plan.md

需要测试优先、验证策略或风险驱动实现
  -> Stage 2 TDD or Verification Strategy: references/sop-02-tdd-or-verification-strategy.md

需要修改代码、测试、文档或配置
  -> Stage 3 Code Change: references/sop-03-code-change.md

用户报告 bug、错误、回归或异常行为
  -> Stage 4 Bug Diagnosis: references/sop-04-bug-diagnosis.md

涉及安全漏洞、CVE、补丁回溯或高风险修复
  -> Stage 5 Security CVE: references/sop-05-security-cve.md

需要证明完成、运行测试、构建、lint 或验收
  -> Stage 6 Fresh Verification: references/sop-06-fresh-verification.md

需要代码审查或变更风险评估
  -> Stage 7 Code Review: references/sop-07-code-review.md

需要交付摘要、验收映射或变更说明草稿
  -> Stage 8 Delivery Summary: references/sop-08-delivery-summary.md
```

## 通用原则

- 先读项目现有风格、测试和相关实现，再改代码。
- 小步修改，优先最小正确变更。
- 完成声明必须基于本轮 fresh verification evidence。
- 编码前先确认 Pre-Code Acceptance Contract；完成声明只能覆盖该 contract 中已验证的范围。
- 中断续接时先收敛到当前最小切片，识别已有变更和未完成边界，不把上一轮假设当作本轮完成事实。
- Worktree/Submodule Isolation 必须贯穿 Interrupted Slice Guard、Pre-Code Acceptance Contract 和 Delivery Evidence Packet；submodule 默认只读，除非用户明确授权写入。
- 完成声明必须使用“完成范围 / Fresh Verification / 未验证或失败 / 残余风险”格式；没有 fresh verification 的内容只能写为未验证或待确认。
- 验证命令失败时报告真实状态，不把部分通过描述成完成。
- 长任务可用 checklist 或项目既有 tracker，但不强制每步 commit。
- 高风险实现前先做 POC 或等价薄切片验证，避免错误需求或设计在代码阶段滚动放大。
- 真实脚本、构建、生成和高成本实现前先 reasoning-map 推演，减少失败率。
- POC、正式实现、构建、测试、外部调用、打包和验证前必须通过 Configuration Readiness Gate；能从项目文件自动解析的配置先解析，缺失 required 配置时停止并一次性列出，不边做边问。
- subagent Task 只用于有边界的探索、审查或证据整理；主 agent 必须保留修改范围、最终补丁、验证结论和交付责任。
- Delegation Quality Gate 是改代码前的防错主路径：must/may/do-not delegate triggers 决定是否派发，fallback 只做兜底，不能把缺证据结果写入完成声明。
- 实现阶段必须复用 Technical Handoff Packet 中的目录边界、实施切片和验证策略；除非源码事实或测试结果冲突，不重复技术设计阶段的完整研究。
- 交付前必须 review，分数 >=80，且完成声明必须有 fresh verification evidence；不达标或验证失败时默认自动修复最多 7 轮，连续 2 轮无进展或遇到环境/权限/配置硬阻断时才停。
- 旧项目交付守护经验、TDD、bugfix 和 CVE 处理经验只作为可迁移模式，不作为跨项目硬规则。

## 资源索引

- `references/sop-00-intake.md`: 输入归类和前置材料检查。
- `references/sop-01-implementation-plan.md`: 小步实现计划。
- `references/sop-02-tdd-or-verification-strategy.md`: TDD 或风险驱动验证策略。
- `references/sop-03-code-change.md`: 代码、测试、文档和配置修改规则。
- `references/sop-04-bug-diagnosis.md`: bug 复现、定位和修复计划。
- `references/sop-05-security-cve.md`: 安全/CVE 处理和证据边界。
- `references/sop-06-fresh-verification.md`: 新鲜验证证据纪律。
- `references/sop-07-code-review.md`: 代码审查和风险检查。
- `references/sop-08-delivery-summary.md`: 交付摘要、验收映射和外部操作材料。
- `references/delegation-quality-gate.md`: 实现侧 delegation 触发、隔离、证据和 fallback 规则。
- `references/pattern-delivery-guards.md`: 旧项目交付守护的可迁移模式。
- `templates/`: 可选实现和交付模板。
- `templates/poc-slice-plan.md`: 高风险实现前的 POC Gate 模板；ASCII 只是默认形式之一。
- `checklists/`: 验证与审查清单。

## 交付标准

交付时必须使用完成声明格式：完成范围、Fresh Verification、未验证/失败/跳过项、残余风险和后续建议。每个完成范围必须映射到本轮实际运行的命令、检查或人工验证证据；未执行、无法执行或失败的验证必须单独列出，不能混入完成声明。交付摘要还必须说明变更文件、需求/设计映射、Delivery Evidence Packet、docs 归档/修订状态，以及需要用户确认的外部操作。
