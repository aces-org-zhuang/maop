# SOP-06 Dialectical Adversarial Merge

## Goal and scope

用不同视角分别执行不同 SOP，再由主流程对证据进行辩证和对抗式合并，最终给出最佳决策。适用于需要比较多个可行路径、平衡冲突目标或避免单视角偏差的 skill 设计。

## Pre-read and todo/status

1. 先读取 `../SKILL.md`，确认当前请求已被路由到 `dialectical` 模式。
2. 为每个视角建立独立 todo：视角名、目标、输入、输出、证据、状态、负责人。
3. 在发散前后、对抗比较前后、主流程裁决前后都更新 `todo/status`。

## Execution shape

```text
user intent
  -> split into multiple views
  -> run different SOPs per view
  -> collect evidence from each view
  -> adversarial compare contradictions
  -> dialectical merge in main flow
  -> best decision + residual risks
```

视角示例：

- 路由视角：这个 skill 应该如何分阶段执行。
- 验证视角：哪些路径最容易被证明或证伪。
- 风险视角：哪些路径会过触发、漏触发或越界。
- 交付视角：哪种结构最利于后续维护和复用。

## Main-loop contract

- 每个视角只负责一个角度的 SOP 执行，不抢主决策。
- 主流程负责整合冲突证据、处理对抗结果并做最终裁决。
- 如果某个视角证据不足，标记 `RED`，但不允许用空白意见覆盖其他视角。
- 最终输出必须同时说明：推荐决策、为什么不是其他选项、残余风险和下一步。

## Validation

- 检查每个视角都有独立输入、输出和证据。
- 检查对抗比较不是简单投票，而是证据驱动裁决。
- 检查最终决策保留了被否决方案的关键反对理由。
- 检查 todo/status 在每轮合并前后都被更新。
