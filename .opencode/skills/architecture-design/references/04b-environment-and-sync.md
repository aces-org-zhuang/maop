# SOP 04b: 环境自适配与同步查看

## 目标

解决两个现实问题：**目标环境可能没有安装或编译 likec4**，以及**改了模型后如何同步查看**。本文件给出零依赖回退链、热重载验证方法和故障降级规则。

## When Required

每次使用 `architecture-design` 技能时先读本文件。它决定「用什么方式验证模型」和「怎么让改动可见」，成本很低但能避免大部分环境问题。

## 核心结论（1.56.0 / 1.58.0 实测）

### 1. MCP 不需要预装 likec4

`@likec4/mcp` 自带完整 LikeC4 内核。实测在**完全没有 `node_modules`、没有本地 likec4** 的目录中，`npx -y @likec4/mcp` 直接可用：

```text
INFO likec4.lang workspace: found 3 source files
INFO likec4.mcp Starting MCP stdio server
serverInfo: {"name":"LikeC4","version":"1.56.0"}
```

这意味着**能力查询链路不受本地环境限制**，不需要 `npm install`，也不需要锁定 likec4 版本。模型解析、依赖查询、影响面分析全部可用。

### 2. MCP 支持 watch 热重载

MCP 默认 `watch: true`。实测：启动 MCP 后新增一个 `.c4` 文件，**不重启 MCP** 即可查到新元素（日志出现新的 `found N source files`）。

### 3. CLI 需要安装，但只有校验/构建需要

区分两件事：

| 需求 | 是否需要本地安装 likec4 |
| --- | --- |
| AI 查询模型、查依赖、查影响面（MCP） | **不需要**，npx 自带 |
| `likec4 validate` 语法校验 | 需要 |
| `likec4 build` 构建静态站 | 需要 |
| `likec4 export png` 导出图片 | 需要，且额外需 Playwright |
| `likec4 serve` 本地预览 | 需要 |

## 能力检测与回退链

写模型前按顺序探测，逐级降级，**不要一上来就要求用户装环境**：

```text
Step 1  探测 MCP 是否可用
        已配置 likec4 MCP 且能返回结果 -> 直接使用，零安装
        ↓ 不可用
Step 2  探测本地 CLI
        command -v likec4 或 npx likec4 --version 可用 -> 用 CLI 校验
        ↓ 不可用
Step 3  尝试按需 npx（无需 install，但首次较慢）
        npx -y likec4@<pinned> validate -> 成功即用
        ↓ 不可用
Step 4  只读降级
        告知无法运行 validate，仅交付模型文件 + 明确的未校验风险
```

**Step 4 不是失败**。必须照常交付模型文件，但交付说明中要写明「未能运行 `likec4 validate`，原因是 X，未经校验的语法风险是 Y」。禁止伪造校验通过。

### 检测命令

```bash
# 1. MCP 能力：看 opencode 配置里是否有 likec4 MCP，且调用后有响应
# 2. 本地 CLI
likec4 --version
# 3. npx 按需（不写入 node_modules）
npx -y likec4@1.58.0 --version
# 4. Node 版本
node --version
```

## Node 版本策略

MCP 内核不受宿主机 Node 版本限制（npx 会自行解析可用版本），但 CLI 对 Node 有下限：

| likec4 版本 | Node 要求 | 说明 |
| --- | --- | --- |
| 1.56.0（MCP 内置） | 随 npx 解析 | 通常不构成障碍 |
| 1.58.0 | 实测 22.22.2 可运行 | npm 会 warn EBADENGINE |
| 1.59.x | 硬性 >= 22.22.3 | 低于该版本直接崩溃 |

**建议策略**：优先使用 MCP（不受版本影响）；需要 CLI 时按需 npx 并选兼容版本；只有在 CI 中才把 likec4 装进 `devDependencies` 并锁定精确版本。

## 同步查看：三种方式

### 方式一：MCP 查询（默认，零安装）

改完模型后直接让 AI 查询确认效果，无需任何服务：

```
搜索新增元素是否已生效
列出 <element> 的入向与出向关系
```

适用：验证模型结构、查依赖、做影响面分析。这是**首选同步方式**。

### 方式二：serve 热预览（需 CLI）

```bash
likec4 serve --port 5173
```

支持热更新：改 `.c4` 后浏览器自动刷新，无需手动重载。`--listen 0.0.0.0` 可让局域网访问；容器内建议配 `--use-dot`。

### 方式三：build 产出静态站（需 CLI，CI 用）

```bash
likec4 build -o ./dist
```

严格绑定 base path。嵌入到文档站或子路径时用 `--base ./` 或 `--base /pages/`。需要完全自包含单文件时用 `--output-single-file`。

## 变更同步纪律

模型与代码的同步靠流程，不靠工具自动完成：

1. **依赖变更必须同 PR 更新模型**。新增服务、调用关系或部署节点时，架构模型在同一个 PR 内一起改。
2. **改动后先自检再交付**：运行 validate（若可用），再用 MCP 查询确认新元素可被检索到。
3. **主仓指针更新**：设计仓发版后由主仓开 PR 更新 submodule 指针。gitlink 不会自动跟随。
4. **不要把 dist 提交进仓**：`build` 产物属发布产物，由 CI 处理。

## 故障降级规则

| 现象 | 判断 | 处理 |
| --- | --- | --- |
| MCP 无响应 | 未配置或 opencode 未重启 | 确认 `opencode.json` 后重启 opencode |
| `npx likec4` 报 EBADENGINE | Node 低于该版本下限 | 换低版本 likec4，或升级 Node |
| `ERR_MODULE_NOT_FOUND` | npx 缓存或依赖损坏 | 改用本地 `npm install likec4@<pinned>` |
| `Could not resolve reference` | 模型语法/引用错误 | 修模型，不是环境问题 |
| `Duplicate view` | 视图名重复 | 改名 |
| MCP 查到旧数据 | watch 未生效或文件未保存 | 确认文件落盘；必要时查 `read-project-summary` 的 `sources` 列表 |
| CI 报 build 失败 | Node 版本或依赖锁定问题 | 确认 `engines` 与锁定版本一致 |

**关键区分**：语法错误与引用错误表现为 `Invalid` 且有行号，这是模型问题；`EBADENGINE`、`MODULE_NOT_FOUND`、网络错误是环境问题。不要把环境故障误报为模型缺陷，也不要把模型语法错误归因于环境。

## 零依赖快速验证脚本

在无本地安装的环境下验证模型语法：

```bash
npx -y likec4@1.58.0 validate
```

该命令不写入 `package.json` 与 `node_modules`（npx 缓存），适合提交前快速自查。CI 中仍应使用锁定版本的本地安装以保证可复现。

## 与其他技能的关系

- 本文件只处理**环境与同步**，DSL 规则见 `references/01-likec4-basics.md` 与 `references/03-dynamic-views.md`。
- 版本特性实测表在 `references/03-dynamic-views.md`，不要凭官方文档假设特性可用。
- 设计仓归属与 submodule 规则见 `references/05-design-repo-layout.md`。

## 常见失败模式

- 一发现没有本地 likec4 就停下要求用户安装，而没先试 MCP 与 npx。
- 把「无法运行 validate」当作不能交付的理由。模型文件仍应交付，只需标注未校验风险。
- 把环境故障（Node 版本、依赖缺失）报成模型语法错误。
- MCP 无响应就反复重装 likec4，而不去检查 opencode 配置与重启。
- 把 `build` 产物 `dist/` 提交进仓。
- 依赖 `serve` 才能验证，而环境不支持，忽略了 MCP 查询这一零安装路径。
