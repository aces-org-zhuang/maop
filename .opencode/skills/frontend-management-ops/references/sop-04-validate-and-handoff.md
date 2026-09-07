# SOP-04 Validate and Handoff

## Goal and scope

在成功、阻塞或失败退出前验证 CRUD、CLI、导入导出、doctor、构建安装和文档/i18n 同步，并交付可重启证据。

## Pre-read

1. 读取本轮所有 `todo/status`、修改 diff、测试输出和 RED。
2. 若修改 docs 或证据文件，确认对应索引已同步。

## Fresh verification gate

按修改范围选择并记录实际结果：

- `npm run typecheck` 或 package 级类型检查。
- 相关 `npm test`/Vitest 单测或更小测试入口。
- `npm run lint` 或项目等价 lint。
- CLI 源码态 smoke：`<bin> --help`、`<bin> doctor --json`、至少一个实体 CRUD dry-run 或测试数据路径。
- 构建验证：`npm run build`。
- 安装/打包后 CLI 验证：Windows 打包或本地安装后的 `<bin> --version`、`doctor`、`export`、`import --dry-run`。

没有运行的项目必须写 `not run` 和原因；失败必须写真实失败，不得把部分通过写成完成。

## Handoff packet

交付时包含：

- `Entities`: 覆盖实体、动作和 out-of-scope 实体。
- `Contracts`: shared type/schema、IPC/preload、persistence、CLI 命令和 import/export 格式。
- `Files`: 实际修改路径和关键行。
- `Verification`: 运行命令、结果、产物路径和安装后 CLI 状态。
- `Data safety`: dry-run、备份、冲突策略、删除保护和 doctor 写入边界。
- `RED`: 未闭环风险、blocked 输入、未验证外部环境。
- `Next step`: 可重启命令或下一最小动作。

## Exit

退出前把所有 todo/status 更新为 `succeeded`、`blocked` 或 `failed`，最后把 workflow 标为 `exited`。若存在 blocked 子项，整体不得写成完全成功。

## RED

- 没有 fresh verification evidence。
- 没有构建安装后的 CLI 证据，却声明用户安装后可用。
- i18n、IPC/preload 或 shared types 变更缺同步。
- 真实数据迁移未证明可回滚。
