# SOP 03 - Code Change

## Goal

按项目风格执行最小正确代码变更。

## Steps

1. 读取相关现有实现、测试和项目约束。
2. 确认 Delegation Quality Gate 已处理必需 lens；未处理时先回到 intake/plan，不直接开写。
3. 确认 Interrupted Slice Guard、Pre-Code Acceptance Contract 和 Worktree/Submodule Isolation 仍然有效。
4. 优先使用项目已有抽象、工具和平台层，不引入无必要新框架。
5. 做最小范围修改，避免无关重构。
6. 同步更新必要测试、类型、文档或配置。
7. 遇到用户未授权的破坏性操作、凭据、仓库外状态变更、未知归属 dirty change 或未授权 submodule 写入时停止并确认。

## Validation

- 变更范围与计划一致。
- 没有修改无关用户工作或绕过项目规则。
- Diff 未越过 Pre-Code Acceptance Contract 的 allowed/not-to-touch 边界。
- Submodule 状态符合隔离规则；默认未写入 submodule。
