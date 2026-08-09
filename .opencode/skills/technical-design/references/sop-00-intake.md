# SOP 00 - Intake

## Goal

确认技术设计输入是否充分，并确定当前设计阶段。

## Steps

1. 读取用户提供的需求、PRD、Product Handoff Packet、任务记录、设计草案或错误背景。
2. 按 `development-workflow/references/knowledge-handoff-gate.md` 执行 Read Gate：优先消费 Product Handoff Packet 和 Reuse Ledger，再读取相关架构文档、设计模板、接口契约、编码规则、平台抽象和最小 docs 索引。
3. 执行 Delegation Quality Gate：判断 must/may/do-not delegate，并为可委派任务预先定义 Source Map、Interface/State、Option/Risk、Verification lens 的字段级 return contract。
4. 检查上游 packet 是否足以支撑设计；缺少角色、Use Case、范围或验收时标 RED，能从现有材料修复则修复，否则回到 `product-definition`。
5. 判断设计范围：新功能、改造、重构、接口变更、数据变更、风险评估或设计评审。
6. 若需求本身不清，回到 `product-definition`，不要用设计假设补需求缺口。
7. 若缺少代码仓或必要上下文，列出阻塞项；若可通过只读探索或前置委派获得，先获得 Source Map 再判断。

## Outputs

- 设计范围。
- 已有材料和项目约束。
- Product Handoff Packet 消费状态和 Reuse Ledger。
- Delegation Quality Gate 结果：must/may/do-not delegate、lens return contract、禁止委派的关键决策。
- 下一阶段 SOP。
- 阻塞项或待确认问题。
