# SOP 07 - Design Review

## Goal

检查技术设计是否完整、可实现、可验证、可追踪。

## Steps

1. 对照 `checklists/design-completeness.md` 检查设计产物。
2. 对照 `checklists/compatibility-risk.md` 检查契约、数据、迁移和消费者影响。
3. 标注必须修复、建议修复和可延后的设计问题。
4. 对用户反馈进行最小必要修订，不重写已确认内容。
5. 给出 review 分数；设计定版、进入实现或进入高风险 POC 前必须 >=80。
6. 说明是否可进入实现阶段。

## Validation

- 关键节点 review 分数 >=80；低于 80 必须修订并复审。
- 关键 RED 点有明确后续动作。
