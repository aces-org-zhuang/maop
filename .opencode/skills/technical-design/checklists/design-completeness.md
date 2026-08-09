# Design Completeness Checklist

- [ ] 需求到设计决策可追踪。
- [ ] 当前系统依据明确。
- [ ] Delegation Quality Gate 已完成，must/may/do-not delegate 触发和禁止委派决策明确。
- [ ] Source Map lens 已覆盖相关代码、文档、配置、测试入口和证据置信度。
- [ ] 推荐方案和被拒绝方案都有理由。
- [ ] Option/Risk lens 已说明推荐、拒绝和 fallback-only 条件。
- [ ] 接口、数据、状态、错误和权限影响已覆盖。
- [ ] Interface/State lens 已明确 producer、consumer、source of truth、生命周期/时序、兼容性和 failure mode。
- [ ] 技术栈归一、特性模块唯一归属、依赖唯一性、契约 owner 和数据/状态 source of truth 已按 `design-governance.md` 检查。
- [ ] 风险和验证策略明确。
- [ ] Verification lens 已明确验证方法、命令或手工入口、期望证据、handoff 前 required 项和 gap。
- [ ] 实施切片可被 implementation-delivery 消费。
- [ ] Technical Handoff Packet、Implementation Handoff Mini-Spec 和 90% Confidence Evidence Map 已吸收 lens 字段；fallback 仅为兜底。
