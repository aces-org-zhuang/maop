# SOP-00 Intake and Routing

## Goal

把用户问题归类为 bug、回归、验证失败或 RCA 追踪，并确定是否需要先初始化 `fix-rca-trace.md`。

## Steps

1. 提取现象、预期/实际行为、触发条件、环境、复现步骤和影响范围。
2. 判断是否已有 RCA 追踪文档；没有则先通过 `document-generation` 初始化单一真相源。
3. 明确本轮目标是定位、修复还是“不再复现”验证。
4. 如果问题边界或时序不清，标记为 reasoning-map 输入。

## Output

问题归类、目标、验证入口、文档状态。
