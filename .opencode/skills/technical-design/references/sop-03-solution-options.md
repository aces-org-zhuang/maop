# SOP 03 - Solution Options

## Goal

提出足够但不过度的方案选项，并给出可辩护取舍。

## Steps

1. 先给出最小可行方案，再考虑更复杂方案。
2. 对每个方案比较实现成本、风险、兼容性、可测试性、可维护性和扩展空间。
3. 明确拒绝的方案及原因，避免后续反复讨论。
4. 推荐方案前执行 Preview Gate，使用 `templates/design-sketch.md`、Mermaid、状态机、时序图、接口草案或其他适合形式，展示上下文、组件、数据/状态、风险和验证；如果用户要求只要草图，不读取仓库材料，直接用输入内容和显式假设生成。
5. 如果需要技术选型、依赖选型、开源库/框架/仓库评估或候选 repo 对比，转入 `references/sop-03b-selection-evaluation.md`；缺候选时用 `research` 的 Discovery Path 发现候选，深度证据包转入 `research`。
6. 推荐一个方案，并说明它满足哪些需求和约束。

## Validation

- 方案比较围绕项目约束，不是泛泛技术偏好。
- 推荐方案有明确取舍，不是多个方案并列结束。
- 已先完成 Preview Gate，或说明为什么本次窄设计不需要预览。
