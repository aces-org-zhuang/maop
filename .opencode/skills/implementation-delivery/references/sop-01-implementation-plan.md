# SOP 01 - Implementation Plan

## Goal

把需求或设计拆成小步、可验证的实现计划。

## Steps

1. 读取需求、设计和现有代码上下文。
2. 列出需要修改、创建、测试或文档更新的文件类别。
3. 按风险和依赖排序，把工作拆成小切片。
4. 对较大或高风险实现先执行 POC Gate，使用 `templates/poc-slice-plan.md` 或更适合的 POC 形式，确认目标文件、验证信号和回滚/风险点。
5. 每个切片写明修改目标、验证方式和回滚/风险点。
6. 若项目已有任务格式或 tracker，遵循项目格式；没有时可使用 `templates/implementation-plan.md`。

## Validation

- 每个切片都有明确验证信号。
- 较大或高风险实现已有 POC Gate，或说明本次是窄改不需要 POC。
- 计划不要求一次性大范围重写。
