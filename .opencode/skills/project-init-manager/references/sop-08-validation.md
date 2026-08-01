# SOP 08: Validation

## 目标

验证初始化结果是否完整、可索引、可继续开发，并明确未闭环 RED 点。

## 执行步骤

1. 读取 `checklists/init-completeness.md`。
2. 检查根 `README.md`、`AGENTS.md`、`docs/README.md`、`docs/AGENTS.md` 是否存在或是否按审计结果标记缺失。
3. 检查根 `AGENTS.md` 的项目结构是否覆盖所有已创建顶层目录；不能只列 `src/`。
4. 检查 docs 索引目录和 `failure-modes`、`debugs`、`evidences` index。
5. 检查 `.opencode/README.md` 和本地组件目录。
6. 检查研究区 `vendor/research/aces-research/index.md` 或锁定 submodule 计划。
7. 检查 AI 引擎 `vendor/ai/maop` submodule 或锁定 submodule 计划。maop 源仓模式下检查是否明确排除自嵌套。
8. 检查项目仓 `.opencode` 与 `vendor/ai/maop/.opencode` 的边界说明；maop 源仓模式下检查本仓 `.opencode` 是否被标记为能力源码目录。
9. 检查 `.gitmodules` 与实际 submodule 状态；如果涉及真实 submodule，读取 `checklists/submodule-safety.md`。
10. 检查技术栈或能力开发命令是否来自真实配置；未知命令必须保留 `待补充`。
11. 输出 pass/fail、未闭环 RED 点和下一步。

## 推荐验证命令

按可用性选择，不要强行运行不存在的命令：

```bash
git status --short
git submodule status --recursive
```

如果项目已有包管理器或测试配置，再运行相应 typecheck、lint、test 或 build。

## 验收输出

最终回复应包含：

- 项目路径。
- 创建和更新的关键结构。
- 保留未覆盖的已有文件。
- 研究区路径。
- AI 引擎 submodule 路径。
- `.opencode/opencode.json` 处理结果。
- 验证命令和结果。
- 未闭环 RED 点。

## 常见 RED 点

- 初始化后没有索引同步。
- 创建了 docs 子目录但没有 README。
- 创建了研究区但没有 index。
- 未规划锁定的 `aces-research` 或 `maop` submodule。
- 未说明项目仓 `.opencode` 与 maop `.opencode` 的边界。
- 创建了多个顶层目录，但 `AGENTS.md` 项目结构没有完整列出。
- 写了 OpenCode 配置但没有 schema 或重启提醒。
- maop 源仓模式没有排除 `vendor/ai/maop` 自嵌套，或没有说明 `.opencode/skills` 是能力源码。
