# SOP-00 Intake and Routing

## Goal and scope

把用户关于前端管理功能的请求转换成可执行的实体、动作、CLI、导入导出和 doctor 任务。此阶段不修改代码。

## Pre-read

1. 读取目标 skill 的 `SKILL.md`。
2. 若会改当前 Aces Desktop 代码，先读仓库根 `AGENTS.md` 和 `docs/README.md`；修 bug 或跑代码测试前读 `docs/failure-modes/index.md`。
3. 建立 `todo/status`，每项记录 SOP、实体集合、动作、输入、产物路径、验证证据和下一步。

## Intake record

记录以下内容：

- `entities`: `projects`、`habits`、`members`、`deliverables`、`teams` 或用户指定实体。
- `actions`: `list|get|create|update|delete|archive|restore|assign|bulk|import|export|doctor`。
- `surface`: UI、IPC/preload、store/persistence、CLI、tests、packaging、docs/i18n。
- `input`: 用户给定数据样例、导入文件、目标命令、安装方式、兼容要求。
- `boundary`: 可写目录、禁止触碰目录、是否允许数据迁移、是否允许删除真实数据。
- `success`: 可观察验收条件，必须包含 fresh verification；CLI 任务必须包含构建安装后命令验证。
- `RED`: 缺 schema、缺 CLI 入口、缺测试、缺安装环境、真实数据风险、i18n 漏同步。

## Route

```text
请求进入
   -> 只要需要了解现有实体/数据契约 -> sop-01-domain-contract-map
   -> 需要 CRUD/UI/IPC/CLI 代码实现 -> sop-02-crud-cli-implementation
   -> 需要 import/export/doctor -> sop-03-import-export-doctor
   -> 任一路径完成、阻塞或失败 -> sop-04-validate-and-handoff
```

## Delegation policy

可委派代理执行只读源码发现、测试面盘点、命令输出抽取或独立风险审查。委派必须给出读取路径、禁止写入范围、停止条件和返回字段：`Finding`、`Evidence`、`Confidence`、`Fidelity`、`RED`、`Excluded scope`、`Next step`。主流程保留最终实体范围、数据契约、代码修改和完成判断。

## Validation

进入下一 SOP 前确认：实体集合和动作集合已记录；写入边界明确；若要删除、迁移或覆盖数据，已有 dry-run/备份策略或被标为 blocked；todo 中没有遗漏 CLI、i18n、测试和构建验证。

## RED

- 用户要求真实数据删除或覆盖但没有备份/确认。
- 当前仓库没有可定位的实体/schema/持久化入口。
- CLI 安装或打包目标无法从项目配置推出。
