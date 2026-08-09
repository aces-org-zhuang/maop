# SOP 01 - Implementation Plan

## Goal

把需求或设计拆成小步、可验证的实现计划。

## Steps

1. 读取需求、Technical Handoff Packet 和现有代码上下文。
2. 复用 technical-design 给出的实施切片、目录边界和验证策略；只有源码事实、测试结果或用户反馈冲突时才重新拆分。
3. 根据 Delegation Quality Gate 结论，先完成必要的只读探索、测试面发现、冲突解析或证据提取，再把接受结果写入计划。
4. 列出需要修改、创建、测试或文档更新的文件类别。
5. 按风险和依赖排序，把工作拆成小切片。
6. 为每个切片补齐 Worktree/Submodule Isolation、Interrupted Slice Guard 和 Pre-Code Acceptance Contract。
7. 对较大或高风险实现先执行 POC Gate，使用 `templates/poc-slice-plan.md` 或更适合的 POC 形式，确认目标文件、验证信号和回滚/风险点。
8. 每个切片写明修改目标、验证方式和回滚/风险点。
9. 若项目已有任务格式或 tracker，遵循项目格式；没有时可使用 `templates/implementation-plan.md`。

## Validation

- 每个切片都有明确验证信号。
- 较大或高风险实现已有 POC Gate，或说明本次是窄改不需要 POC。
- 计划不要求一次性大范围重写。
- 计划说明哪些设计切片被复用、哪些被修订，以及修订证据。
- 必需 delegation 结果已通过 synthesis 后进入计划；fallback 只记录为阻塞、缩小范围或主 agent 自行处理。
- Pre-Code Acceptance Contract 明确 allowed/not-to-touch、验收检查和 submodule 读写边界。
