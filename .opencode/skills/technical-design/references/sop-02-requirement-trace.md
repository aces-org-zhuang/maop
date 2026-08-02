# SOP 02 - Requirement Trace

## Goal

确保每个设计决策能追溯到明确需求、约束或风险。

## Steps

1. 将需求拆成可设计项：行为、数据、状态、权限、异常、非功能约束。
2. 为每个设计项记录来源和优先级。
3. 将 Product Handoff Packet 中的角色、Use Case、范围和验收映射到设计项；不得新增无来源的产品目标。
4. 标注不会进入本次设计的需求或后续阶段。
5. 识别需求之间的冲突、重复和隐含依赖。
6. 将追踪结果写入设计文档、trace table 或 Technical Handoff Packet。

## Validation

- 没有无来源的设计决策。
- 关键需求都有对应设计响应或明确延后说明。
- 设计没有重复展开已确认产品研究，除非上游 packet 与源码事实冲突。
