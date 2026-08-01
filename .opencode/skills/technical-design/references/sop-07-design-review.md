# SOP 07 - Design Review

## Goal

检查技术设计是否完整、可实现、可验证、可追踪。

## Steps

1. 对照 `checklists/design-completeness.md` 检查设计产物。
2. 对照 `checklists/compatibility-risk.md` 检查契约、数据、迁移和消费者影响。
3. 对照 `checklists/design-governance.md` 检查技术栈归一、特性模块唯一归属、依赖唯一性、契约 owner、数据/状态 source of truth、层级边界、运行时边界、构建复杂度、回滚策略和不重复造轮子。
4. 标注必须修复、建议修复和可延后的设计问题。
5. 对用户反馈进行最小必要修订，不重写已确认内容。
6. 给出 review 分数；设计定版、进入实现或进入高风险 POC 前必须 >=80。
7. 如果 `design-governance.md` 中技术栈归一、特性模块唯一归属、依赖唯一性、契约 owner 或 source of truth 任一关键项未通过，即使分数 >=80 也不得进入实现。
8. 说明是否可进入实现阶段。

## Validation

- 关键节点 review 分数 >=80；低于 80 必须修订并复审。
- governance 关键项全部通过，或未通过项已降级为明确 RED 且不阻塞当前最小 POC。
- 关键 RED 点有明确后续动作。
