# SOP-02 CRUD CLI Implementation

## Goal and scope

按源码图谱实现或补齐管理实体 CRUD、批量操作和 CLI 命令，使 UI 与 CLI 共用同一数据契约和验证路径。

## Pre-read

1. 读取 `sop-01-domain-contract-map.md` 的实体映射和 RED。
2. 修代码或跑测试前读取 `docs/failure-modes/index.md`。
3. 若涉及 React UI，确认 `react-i18next` namespace 和现有组件模式。
4. 若涉及 CLI，确认 Node/Electron 构建产物、`package.json` 的 `files`/`bin`/scripts、Windows 打包约束。

## Steps

1. 定义每个实体的最小 CRUD contract：输入字段、必填校验、id 生成、更新时间、错误码、权限/边界、幂等性。
2. 让 renderer、preload、IPC、main service、persistence 和 CLI 复用同一 shared type 或 schema；避免 UI 和 CLI 各自维护不同字段。
3. 为 CLI 提供稳定命令形态：`<bin> <entity> list|get|create|update|delete`；输出默认 JSON，支持 `--format table|json`、`--project`、`--workspace`、`--dry-run`、`--yes`。
4. 删除类动作默认走 soft delete、archive 或 require confirmation；真实 destructive 操作必须支持 dry-run 和显式确认。
5. 为批量操作提供事务边界：逐条结果、部分失败报告、退出码和可重试输入。
6. 前端新增可见文本必须写 translation key，并同步 `apps/frontend/src/shared/i18n/locales/en/`、`fr/`、`zh-CN/`。
7. 为每个实体补单元测试或服务级测试；CLI 至少要有命令解析、成功路径、校验失败、dry-run 和退出码测试。

## Write boundary

只修改当前任务相关模块、shared types/schema、i18n、测试、CLI 入口、构建配置和必要文档。不得重构无关前端布局或替换持久化方案，除非 reasoning-map 和技术设计已确认。

## Validation

至少运行与修改范围匹配的 `typecheck`、`test`、`lint` 或更小测试命令；CLI 变更必须运行源码态命令验证和构建后产物验证。验证失败进入 loop：定位失败实体/命令 -> 最小修复 -> 重跑 fresh verification。

## RED

- UI 和 CLI 走不同数据写入路径。
- CLI 只在源码态可用，构建安装后不可执行。
- 删除/导入等高风险动作没有 dry-run 或确认机制。
- 测试只覆盖 happy path，不覆盖 schema 校验和失败退出码。
