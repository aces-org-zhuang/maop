# SOP 04 - 项目集成（构建、MCP、CI）

## Goal

把架构模型接入项目工程：建立可构建的设计仓项目、配置 LikeC4 MCP 让 AI 能查询模型、建立 CI 漂移检测，并明确导出命令的能力边界。

## When Required

需要把模型落盘为可构建项目、让 opencode 通过 MCP 读取架构、或在 CI 中防止架构漂移时。

## 前置：Node.js 版本

LikeC4 **1.58.x 要求 Node >= 22.22.3**。实测在 22.22.2 下 npm 报 `EBADENGINE`，且运行时会因缺失依赖崩溃（`ERR_MODULE_NOT_FOUND: @rolldown/pluginutils`）。

官方文档写「Node.js 20+」是宽松表述，实际以锁定版本的 `engines` 字段为准：

```bash
node -e "console.log(require('likec4/package.json').engines)"
```

不满足时先升级 Node，不要降级工具后假装完成。

## 最小项目结构

```text
<repo>/
  package.json
  likec4.config.ts        # 工作区与项目定义
  src/
    specification.c4
    model/*.c4
    views/*.c4            # 静态视图 + 动态视图 + deployment view
    deployment/*.c4       # 部署模型
```

### package.json

```json
{
  "name": "aces-design-beauty",
  "private": true,
  "scripts": {
    "dev": "likec4 serve",
    "build": "likec4 build -o ./dist",
    "validate": "likec4 validate",
    "format": "likec4 format",
    "format:check": "likec4 format --check"
  },
  "devDependencies": {
    "likec4": "1.58.0"
  }
}
```

**版本必须锁定**（不用 `^`）：LikeC4 跨版本 DSL 特性差异大，锁版本才能保证 `validate` 行为稳定。

`likec4 serve` 默认在 5173 端口（`--port` 可改），支持热更新。

## MCP 接入（让 AI 读取架构）

### 方式一：@likec4/mcp 包（推荐用于 opencode）

在主仓 `.opencode/opencode.json` 增加：

```json
{
  "mcp": {
    "likec4": {
      "type": "local",
      "command": ["npx", "-y", "@likec4/mcp"],
      "enabled": true,
      "environment": {
        "LIKEC4_WORKSPACE": "vendor/design/aces-design"
      }
    }
  }
}
```

`LIKEC4_WORKSPACE` 指向设计仓工作区；未设置时使用当前目录。

### 方式二：本地 CLI

```bash
likec4 mcp --stdio                 # stdio 传输
likec4 mcp --http -p 33335         # http 传输
```

VS Code 装 likec4 扩展后会自动注册 MCP。

### MCP 能做什么

暴露模型的自然语言查询能力，例如：

- 「列出 backend api 的所有入向关系」
- 「Backend 的哪些嵌套元素与 legacy api 有关系」
- 「列出所有打了 legacy 标签、且属于 team1 项目的元素」
- 「导出 Backend 到 SQS 的关系为 CSV」

**这是 LikeC4 相对 Mermaid 的核心优势**：AI 拿到的是结构化图查询结果，而不是一堆文本。Mermaid 图 AI 只能读注释。

配置变更后需重启 opencode 生效。

## 导出能力

```bash
likec4 export json -o dump.json        # 结构化 JSON，可接自有渲染或校验
likec4 export png -o ./assets          # 需要 Playwright
likec4 export jpg -o ./assets --quality 90
likec4 export drawio                   # 每视图一个 .drawio；--all-in-one 合并
likec4 gen mermaid                     # 导出 Mermaid
likec4 gen plantuml
likec4 gen d2
likec4 gen dot
likec4 gen react                       # 生成 React 组件
```

### 导出边界（必须告知用户）

- `export png` / `jpg` 依赖 Playwright；CI 中需按 Playwright 文档配置，并注意 `chromium-sandbox`。
- **PNG/JPG 导出建议放本地或独立可选任务**，不要放进主 CI 路径，避免成为流水线不稳定源。
- `likec4 build` 内部走 Vite；部署可参考 https://likec4.dev/tooling/github。

## CI 漂移检测

架构漂移 = 模型与代码/配置不一致。最小的 CI 门禁：

```yaml
name: architecture
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive        # 若设计仓以 submodule 引入
      - uses: actions/setup-node@v4
        with:
          node-version: '22.22.3'   # 1.58.x 实际下限，不要写 20
      - run: npm ci
      - run: npm run validate          # 失败退出码非 0
      - run: npm run format:check      # 格式化门禁
      - run: npm run build             # 构建发布产物
```

### 检测要点

- **CI 必须显式设置 `node-version`**，且不低于锁定版本的 `engines` 下限（1.58.x 为 22.22.3）。写 `20` 或留空都可能触发运行时崩溃。
- 若 design 仓以 submodule 引入，`submodules: recursive` 必须开，否则目录为空，`validate` 无模型可校验。
- **依赖必须锁版本**（`likec4: "1.58.0"` 而非 `^1.58.0`）。LikeC4 升级可能改变 DSL 解析行为，解锁版本会让 CI 行为不可复现。
- `format:check` 失败退出码为 1，可作为风格门禁。
- 发布静态站：`build` 后将 `dist/` 推到 gh-pages。
- CI 环境变量复杂，建议本地先跑通三条命令再上 CI。

## 交付前必跑

```bash
likec4 validate        # 通过时输出 ✓ Valid (N files)，退出码 0
likec4 format --check  # 通过时输出 All N file(s) are formatted
```

实测链路：`validate` → `format --check` → `build` 三步均可在 1.58.0 + Node 22.22.2（本机为 22.22.2 时 1.58.0 可正常运行，但 npm 会警告 engine 要求 >= 22.22.3；1.59.x 则硬性阻断）下通过。

无法运行时必须说明原因、降级证据和残余风险，不得声称已校验。

## 与项目 CI 的边界

设计仓独立构建发布，主仓 CI **不构建**设计仓。主仓只在其 `docs/02-development/submodules-index.md` 登记该 submodule 的 path / url / pinned_ref / boundary / consumer / build_entry / validation_entry / update_policy，其中 `build_entry` 写 `none` 并注明原因。

## 常见失败模式

- `setup-node` 未指定版本 → 可能低于 20，`export png` 与 CLI 行为异常。
- 主仓 CI 未开 `submodules: recursive` → 设计仓目录为空，校验形同虚设。
- 把 PNG 导出放进主 CI → 依赖 Playwright，成为流水线不稳定因素。
- 改了 `.c4` 后不重启 opencode → MCP 仍读旧模型，误判架构。
- 主仓 CI 试图构建设计仓 → 职责越界，构建复杂度不可控。
