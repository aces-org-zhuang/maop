# SOP-01 Domain Contract Map

## Goal and scope

建立管理实体到前端、IPC/preload、shared types、持久化、导入导出、doctor 和测试入口的源码图谱。此阶段默认只读，除非用户已明确进入实现。

## Pre-read

1. 读取 `sop-00-intake-and-routing.md` 的实体、动作、边界和 RED。
2. 若涉及现有项目实现，优先读取相关 `docs/` 入口、`apps/frontend/package.json`、`apps/frontend/src/shared/types/`、`apps/frontend/src/main/ipc-handlers/`、`apps/frontend/src/preload/`、`apps/frontend/src/renderer/`。
3. 对大范围搜索可并行委派代理执行只读发现，但必须保留主流程收敛。

## Steps

1. 用 `rg`/Glob 搜索实体名、同义词和现有 namespace，例如 `project`、`habit`、`member`、`deliverable`、`team`。
2. 为每个实体确认 source of truth：前端状态、main process store、文件、数据库、远程 API 或尚未存在。
3. 建立契约链：renderer action -> preload API -> IPC channel -> main handler/service -> persistence -> tests。
4. 检查 i18n namespace：新增用户可见文本必须同步 `en`、`fr`、`zh-CN`。
5. 检查 CLI 现状：`package.json` 是否有 `bin`、脚本、打包文件列表、安装后可执行路径、现有 tool manager 或命令探测。
6. 输出或更新 `templates/domain-contract-map.md` 格式的映射；若已有项目文档要求证据落盘，按项目规则写入对应证据索引。

## Write boundary

此阶段只允许写临时设计/证据产物；不修改业务代码、真实数据或 package 配置，除非用户请求已进入实现且前置边界明确。

## Validation

检查每个目标实体至少有一个状态：`existing`、`partial`、`missing`、`out-of-scope`。`existing/partial` 必须有源码路径证据；`missing` 必须给出新增 owner 和验证入口。

## RED

- 只找到 UI 标签，找不到数据 source of truth。
- Renderer、preload、IPC、store 之间存在命名不一致。
- CLI 命令设计早于 schema/source of truth 确认。
- 用户可见文本未纳入 i18n 同步范围。
