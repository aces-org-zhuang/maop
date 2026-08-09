# SOP 06 - Review and Revision

## Goal

检查产品定义产物是否完整、可测试、可追踪，并支持小范围修订。

## Steps

1. 对照 `checklists/requirement-quality.md`、`checklists/prd-completeness.md` 和 Preview 结果检查产物。
2. 检查角色 -> Use Case -> 功能需求 -> 验收信号是否贯通；未绑定角色或 Use Case 的核心功能必须修订或移出范围。
3. 对照 `references/delegation-quality-gate.md` 检查委派是否完成前置防错：delegate trigger、上下文隔离、返回契约、Synthesis Gate、fallback 记录均必须可追踪。
4. 对照 Knowledge & Handoff Gate 检查 Product Handoff Packet、Reuse Ledger、Archive Gate 和 Revision Gate；缺失时必须补齐或标 RED。
5. 用 User/Use Case、Acceptance/Risk、Market/Alternative、Scope/Revision lens 标注缺失、冲突、证据弱点和范围漂移。
6. 将问题分为必须修复、建议修复和可延后。
7. 按用户反馈修订产物，保留重要决策和取舍。
8. 给出 review 分数；需求定版或进入 `technical-design` 前必须 >=80。
9. 交付时说明是否已具备进入 `technical-design` 的条件。

## Validation

- 关键节点 review 分数 >=80；低于 80 必须修订并复审。
- 关键缺口有明确修订动作或后续 owner。
- 已说明 docs 归档、docs 修订、docs stale 或不归档原因。
- 委派结果只有在通过 Synthesis Gate 后才被计入 review 分数或 handoff readiness；fallback 未替代前置门禁。
