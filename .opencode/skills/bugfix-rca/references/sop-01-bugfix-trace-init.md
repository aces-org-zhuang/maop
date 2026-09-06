# SOP-01 RCA Trace Init

## Goal

初始化并持续维护 `fix-rca-trace.md`，作为唯一事实载体。

## Steps

1. 准备 RCA 步骤计划：`problem-definition -> evidence -> reasoning-slice -> root-cause -> fix -> non-regression -> handoff`。
2. 用 `document-generation` 的 `init --document-name fix-rca-trace.md --steps-plan <plan>` 创建报告骨架。
3. 每个阶段先调用 `next-step`，再按返回的 schema 用 `update` 写入片段并推进下一阶段。
4. 记录问题摘要、环境、复现步骤、影响范围和已知证据。
5. 将“待验证项”和“候选根因”写入报告，不预先下结论。

## Output

可持续更新的 RCA 追踪报告。
