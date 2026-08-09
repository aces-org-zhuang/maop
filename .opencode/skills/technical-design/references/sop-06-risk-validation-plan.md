# SOP 06 - Risk Validation Plan

## Goal

把设计风险转成验证策略和实施切片。

## Steps

1. 列出功能、兼容性、性能、安全、数据、可观测性和交互风险。
2. 为每个关键风险给出验证方式：测试、构建、静态检查、手工流程、日志或探针。
3. 将实现拆成小切片，每个切片有输入、修改点和验证信号。
4. 标注必须先验证的高风险假设。
5. 对照 Delegation Quality Gate 判断是否必须前置委派 Option/Risk lens 或 Verification lens；多方案取舍、高风险假设、验证入口未知或 90% confidence 证据不足时必须委派补证/复核。
6. 将 Option/Risk lens 字段吸收到 handoff：`option`、`decision`、`accepted_reason`、`rejected_reason`、`risk`、`mitigation`、`fallback_only_if`、`confidence`。
7. 将 Verification lens 字段吸收到 90% Confidence Evidence Map：`claim_or_risk`、`verification_method`、`command_or_manual_entry`、`expected_evidence`、`required_before_implementation`、`gap`、`confidence`。
8. 形成 Technical Handoff Packet：需求追踪、Source Map、源码目录结构、模块 owner、Interface/State 影响、推荐方案、拒绝方案、Option/Risk、风险、Verification 策略、实施切片、Reuse Ledger 和 docs 归档/修订状态。
9. 输出给 `implementation-delivery` 可消费的实施计划输入；fallback 只列为主路径失败或证据不足时的兜底，不作为默认实施路径。

## Validation

- 验证策略能证明关键设计假设。
- 实施切片不要求一次性大改。
- Technical Handoff Packet 足以让 implementation-delivery 开始实现计划，不要求重复技术方案研究。
- Option/Risk 和 Verification lens 已字段级吸收到 handoff 与 90% Confidence Evidence Map；未达 90% 的项已标 gap 和 fallback。
