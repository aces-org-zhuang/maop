# SOP-03 Repair and Fresh Verification

## Goal

实施修复并验证原问题不再复现。

## Steps

1. 只在最小切片内修复被确认的根因或高置信候选。
2. 运行与风险匹配的验证入口：构建、API、WebUI、回归或手工复现。
3. 若仍可复现，返回 reasoning-map 或修复循环，不进入完成态。

## Output

修复结果、验证结果、是否仍可复现。
