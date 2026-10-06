# SOP 10: Design Workspace

## 目标

为项目建立架构即代码的设计仓机制：规划或创建项目层设计仓、以 submodule 引入主仓、配置 LikeC4 MCP 让 AI 能查询架构模型，并明确设计资产与代码资产的边界。

架构模型用 LikeC4 建模，能力细节由 `architecture-design` 技能承载。本 SOP 只负责**初始化期的落地编排**，不重复该技能的 DSL 规则。

## 前置判断：设计仓是否适用

设计仓机制**不是无条件必建**。按以下条件判定：

| 条件 | 结论 |
| --- | --- |
| 完整新项目初始化，且存在外部系统交互、部署形态或多模块协作 | **必建** |
| 单模块脚本、一次性工具、无部署边界的实验 | **不建**，在 `docs/` 记录架构决策即可 |
| 已有独立设计仓 | **接入**，只补 submodule 与 MCP，不重复创建 |
| 审计既有仓 | **只报告差距**，不默认执行 submodule 写操作 |

跳过时必须在最终输出写明「已评估设计仓机制，本项目暂不建立，原因是 X」，不能静默跳过。

## 两种设计仓层级

设计仓分两层，职责与引用方向不同，**不可混用**：

```text
项目层 design-<project>
  归属：本项目
  内容：本项目模型、视图、时序图、部署视图、ADR、接口契约
  引用：本项目主仓以 submodule 引入，path = vendor/design/aces-design
  构建：独立 CI，主仓不构建它

全局层 aces-architecture
  归属：跨项目
  内容：跨项目上下文图、服务全景、依赖矩阵、部署拓扑
  引用：不被任何项目 submodule 引用；其 CI 反向聚合各项目设计仓
  构建：独立 CI，发布总览站点
```

### 为什么不能只用一个大设计仓

Git submodule 的 gitlink 记录的是**子仓 HEAD commit**，与实际使用哪个子目录无关。若 A/B/C 三个项目各自 `submodule add` 同一个大设计仓，则该仓任意一次提交都会改变三个项目的指针，迫使三个项目仓各开一个 PR——即使改动与其中两个项目毫无关系。

`sparse-checkout` **不能**解决这个问题：它只影响工作区检出内容，不移动 gitlink 指向；且只检出一个项目的目录会导致 LikeC4 构建失败（跨项目 `include` 目标缺失）。

结论：**项目层一仓一项目，全局层做聚合发布**。全局层的额外收益是能编译校验跨项目一致性，这是单一大仓做不到的——那里项目边界只是约定。

## 归属决策口诀

初始化时按此判定设计内容归属，不要把所有设计塞进设计仓：

| 条件 | 归属 |
| --- | --- |
| 只服务一个项目 | 项目层设计仓 |
| 描述项目之间的关系 | 全局层聚合仓 |
| 变更要能单独发版给别人看 | 全局层 |
| **变更必须与代码同一个 PR** | **主仓 `docs/`，不放设计仓** |

最后一条是设计仓的定位原则：**设计仓是跨 PR 生命周期的资产，不是代码的附属**。凡是需要与代码同 PR 的内容（模块划分、接口草案、实现级契约）放设计仓，会造成设计滞后于代码，架构图随即腐烂。

## 执行步骤

### 1. 确认设计仓是否已存在

```bash
git ls-remote https://github.com/aces-org-zhuang/design-<project>.git
```

远端可达则进入接入流程；不可达则确认是否需要新建。**新建远端仓属于外部写操作，必须先获得用户明确授权**，不得默认创建 GitHub 仓库。

### 2. 设计仓仓库结构

无论新建还是接入，设计仓本身应符合：

```text
design-<project>/
  likec4.config.ts
  package.json              # scripts: dev/build/validate/format:check
  src/
    specification.c4
    model/                  # 逻辑模型
    views/                  # 静态视图 + 动态视图 + deployment view
    deployment/             # 部署模型
  adr/
```

**依赖必须锁精确版本**（如 `"likec4": "1.58.0"`，不用 `^`）。LikeC4 跨版本 DSL 行为差异大，锁版本才能保证 `validate` 可复现。

**Node 版本要求**：LikeC4 1.58.x 要求 Node >= 22.22.3；以锁定版本的 `engines` 字段为准。初始化时把该约束写入设计仓 README 或主仓 docs 工具链说明。

### 3. 以 submodule 引入主仓

```bash
git submodule add https://github.com/aces-org-zhuang/design-<project>.git vendor/design/aces-design
git submodule status --recursive
```

主仓**不对设计仓做 sparse-checkout**：LikeC4 CLI 需要完整工作区才能 `validate` 与 `build`。

### 4. 配置 LikeC4 MCP

在项目 `.opencode/opencode.json` 的 `mcp` 段增加：

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

若主仓已有其他 MCP（如 playwright），**增量合并**，保留既有字段。

MCP 让 AI 查询结构化架构关系（例如「列出某 API 的所有入向依赖」），而不是读一堆 `.c4` 文本。这是设计仓相对于 Mermaid 图的核心价值，不可省略。

`LIKEC4_WORKSPACE` 路径必须与 submodule path 一致。配置变更后提醒用户重启 OpenCode。

### 5. 登记主仓索引

在 `docs/02-development/submodules-index.md` 记录设计仓的：

- `path`: `vendor/design/aces-design`
- `url`: 设计仓远端地址
- `pinned_ref`: 当前 pinned commit
- `boundary`: 设计仓维护模型与视图；主仓维护代码与 `docs/` 下需与代码同 PR 的内容
- `consumer`: `architecture-design` 技能经 MCP 读取；开发者经 `likec4 serve` 浏览
- `build_entry`: `none`（主仓不构建设计仓，构建在设计仓自身 CI）
- `validation_entry`: 设计仓 CI 执行 `likec4 validate` 与 `format --check`
- `update_policy`: 设计仓发版后由主仓开 PR 更新指针

**`build_entry` 写 `none` 是关键**：它明确架构了职责边界，避免后续在主仓 CI 里加设计仓构建。

### 6. 更新项目规则

在根 `AGENTS.md` 补充设计仓规则，至少包含：

- 设计仓路径与归属层级
- AI 引擎规则中区分 `architecture-design`（架构建模）与 maop 其他技能的职责
- 架构图与文档的同步纪律：依赖关系变更时模型必须同 PR 更新
- 禁止把需与代码同 PR 的内容放进设计仓
- MCP 配置位置与重启要求

### 7. 主仓 CI 注意事项

若主仓 CI 需要感知设计模型（例如在架构评审时校验）：

```yaml
- uses: actions/checkout@v4
  with:
    submodules: recursive        # 必须，否则设计仓目录为空
```

主仓 CI **不执行** `likec4 validate` 与 `build`——那是设计仓自身 CI 的职责。只在需要校验模型可读性时做只读检出。

## 边界

- 本 SOP 不重复 `architecture-design` 的 DSL 规则、shape 枚举、版本特性表；这些以该技能的 references 为准。
- 不在主仓复制设计仓的模型文件。
- 不把 LikeC4 构建产物（`dist/`）提交进主仓或设计仓。
- 不用 sparse-checkout 裁剪设计仓工作区。
- 不把需与代码同 PR 的设计内容放进设计仓。
- 全局层聚合仓不由本 SOP 在主仓引用；它独立建设、独立 CI。

## 关联技能

- 架构建模与图类型边界：`architecture-design`
- submodule 写操作细节：`submodule-manager`
- 主仓索引与 `.gitmodules` 一致性：`sop-07-submodule-governance.md`

## 常见 RED 点

- 把所有项目的设计放进一个设计仓，再被多个项目 submodule 引用，造成指针抖动。
- 用 sparse-checkout 裁剪设计仓，导致 LikeC4 构建失败。
- 主仓 CI 里构建设计仓，职责越界且构建复杂度不可控。
- 只加 submodule 不配 MCP，AI 仍然只能读 `.c4` 原文，浪费结构化模型的价值。
- 把需与代码同 PR 的接口契约放进设计仓，导致设计滞后于代码。
- 忘记登记 `submodules-index.md`，设计仓成为无人知道如何构建和验证的孤岛目录。
- LikeC4 用 `^` 版本号，升级后 `validate` 行为变化且 CI 不可复现。
- 在主仓复制设计仓文件，形成双源维护。
- 项目无部署边界仍强行建设计仓，过度工程。
