# SOP 00 - Intake

## Goal

确认实现交付请求的类型、输入完整性和风险等级。

## Steps

1. 判断请求类型：功能实现、bugfix、测试验证、代码审查、安全/CVE、交付材料或混合任务。
2. 按 `development-workflow/references/knowledge-handoff-gate.md` 执行 Read Gate：优先读取 Technical Handoff Packet、Product Handoff Packet 引用、Reuse Ledger、相关代码、测试、验证规则和 evidence index。
3. 查找需求、设计、任务记录、错误日志、测试失败、现有实现和项目规则。
4. 若输入缺少关键需求或设计，回到上游技能；若只是实现细节不足，可通过代码探索补齐。
5. 识别风险：共享契约、数据迁移、安全、性能、并发、平台差异、用户可见回归。
6. 选择下一阶段 SOP。

## Outputs

- 请求类型。
- 输入材料和缺口。
- Technical Handoff Packet 消费状态和 Reuse Ledger。
- 风险等级和下一阶段。
