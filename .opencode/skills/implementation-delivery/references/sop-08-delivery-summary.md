# SOP 08 - Delivery Summary

## Goal

生成可验收的交付摘要、变更说明或发布说明草稿。

## Steps

1. 汇总实际变更、需求/设计映射和验证结果。
2. 标注未完成、未验证、被跳过或需要用户确认的事项。
3. 如需同步仓库外状态，只生成可审阅材料；只有环境提供真实工具且用户授权时才执行。
4. 对用户可见行为变化写清楚影响和验证方式。
5. 生成 Delivery Evidence Packet：实际变更文件、需求/设计映射、Delegation Quality Gate 采用/拒绝结果、Worktree/Submodule Isolation 结果、验证命令和 fresh evidence、未运行检查、残余风险、docs updated、docs stale、docs not updated with reason。
6. 对照 Archive Gate 和 Revision Gate 判断是否需要更新 `docs/`、`guides/`、`docs/evidences/`、ADR、failure-mode 或 debug index。
7. 给出自然后续步骤，但不把未执行的外部操作说成已完成。

## Validation

- 摘要与实际 diff 和验证输出一致。
- 不伪造当前环境无法验证的仓库外状态。
- 已说明 docs 归档、docs 修订、docs stale 或不归档原因。
- 已说明 fallback 是否发生；fallback 只作为兜底记录，不作为完成证据。
