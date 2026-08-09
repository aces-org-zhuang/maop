# SOP 07 - Design Review

## Goal

检查技术设计是否完整、可实现、可验证、可追踪。

## Steps

1. 对照 `checklists/design-completeness.md` 检查设计产物。
2. 对照 `checklists/compatibility-risk.md` 检查契约、数据、迁移和消费者影响。
3. 对照 `checklists/design-governance.md` 检查技术栈归一、源码目录结构、特性模块唯一归属、依赖唯一性、契约 owner、数据/状态 source of truth、层级边界、运行时边界、构建复杂度、回滚策略和不重复造轮子。
4. 对照 Delegation Quality Gate 检查 must/may/do-not delegate 是否执行正确，subagent return contract 是否覆盖 Source Map、Interface/State、Option/Risk、Verification lens，禁止委派的关键决策是否仍由主 agent 定版。
5. 检查设计是否把新增/修改/禁止触碰目录写入实施切片；缺失目录边界时必须修订。
6. 对照 Knowledge & Handoff Gate 检查 Technical Handoff Packet、Reuse Ledger、Archive Gate 和 Revision Gate；缺失时必须补齐或标 RED。
7. 检查 lens 输出是否字段级吸收到 Technical Handoff Packet、Implementation Handoff Mini-Spec 和 90% Confidence Evidence Map；未吸收或低置信项不得支撑 ready 判断。
8. 标注必须修复、建议修复和可延后的设计问题。
9. 对用户反馈进行最小必要修订，不重写已确认内容。
10. 给出 review 分数；设计定版、进入实现或进入高风险 POC 前必须 >=80。
11. 如果 `design-governance.md` 中技术栈归一、源码目录结构、特性模块唯一归属、依赖唯一性、契约 owner 或 source of truth 任一关键项未通过，即使分数 >=80 也不得进入实现。
12. 说明是否可进入实现阶段。

## Validation

- 关键节点 review 分数 >=80；低于 80 必须修订并复审。
- governance 关键项全部通过，或未通过项已降级为明确 RED 且不阻塞当前最小 POC。
- Delegation Quality Gate 已通过；fallback 被限定为兜底路径，不是默认方案。
- 关键 RED 点有明确后续动作。
- 已说明 docs 归档、docs 修订、docs stale 或不归档原因。
