# SOP 06 - Risk Validation Plan

## Goal

把设计风险转成验证策略和实施切片。

## Steps

1. 列出功能、兼容性、性能、安全、数据、可观测性和交互风险。
2. 为每个关键风险给出验证方式：测试、构建、静态检查、手工流程、日志或探针。
3. 将实现拆成小切片，每个切片有输入、修改点和验证信号。
4. 标注必须先验证的高风险假设。
5. 形成 Technical Handoff Packet：需求追踪、源码目录结构、模块 owner、接口/状态影响、推荐方案、拒绝方案、风险、验证策略、实施切片、Reuse Ledger 和 docs 归档/修订状态。
6. 输出给 `implementation-delivery` 可消费的实施计划输入。

## Validation

- 验证策略能证明关键设计假设。
- 实施切片不要求一次性大改。
- Technical Handoff Packet 足以让 implementation-delivery 开始实现计划，不要求重复技术方案研究。
