---
name: architecture-design
description: 必须用于用 LikeC4 DSL 编写架构即代码、维护架构模型、补充架构视图，或用户要上下文图、容器图、组件图、部署图、场景流程图、时序图、架构漂移检测、架构评审、跨项目架构视图时。用户说“画架构图”“建模”“写 c4 文件”“架构即代码”“likec4”“部署图怎么看”“时序图用 LikeC4 怎么画”“架构和代码不一致”“架构漂移”“跨项目架构全景”时优先使用本技能；不要用于产品用例定义、代码实现、纯视觉表达产物或类图与状态机等 LikeC4 不支持的图类型。
---

# Architecture Design

本技能用于把架构作为代码来建模、校验、发布和协作。`SKILL.md` 只做路由、图类型决策和能力边界；具体语法、工作流和校验步骤按需读取 `references/`。

## 执行模型

采用短路由层 + SOP 渐进执行。主 LLM 负责图类型选型、模型写入决策、最终校验和交付；子代理只用于跨文件影响面排查和独立评审。

```text
intake -> 图类型路由 -> sop-01..05 执行 -> validate -> 交付
```

## 核心原则

- **架构模型是唯一真源**。LikeC4 模型是结构化、可校验、可被 AI 查询的真源；Mermaid/PlantUML 只作为导出物或补充层，不反向成为架构真相。
- **图类型先路由再动手**。写任何图之前先执行 `references/00-diagram-routing.md`，禁止凭印象直接选语法。
- **版本敏感，官方文档不等于可用能力**。本技能语法经 **likec4 1.58.0 实机验证**。官方文档描述最新版本，`opt` `loop` `break` `alt` `try` 与视图文件夹分组在 1.58.0 **不可用**。写入未验证语法会让 `validate` 失败。
- **能力边界必须诚实**。LikeC4 不支持类图、状态机图、严格 UML 用例图；不得伪造或用错误语法硬凑，改走轨道二/三并向用户说明。
- **写入前必须 validate**。任何 `.c4` 写入后必须运行 `likec4 validate`，非零退出码时不得声明完成。
- **跨文件必须用 FQN**。short name 不跨文件继承容器作用域，跨文件引用一律使用完整限定名，否则 `validate` 必然失败。
- **设计资产分层存放**。单服务设计放项目层设计仓并由主仓 submodule 引用；跨项目视图放全局聚合层，禁止把多个项目的设计塞进同一个被 submodule 引用的仓（会造成 gitlink 指针抖动）。
- **依赖必须锁版本**。LikeC4 跨版本 DSL 行为差异大，`package.json` 用精确版本号而非 `^`。

## 触发后先做什么

1. 先读取 `references/00-diagram-routing.md`，确认目标图类型及其对应工具轨道。
2. 读取 `references/01-likec4-basics.md`，确认 specification、命名、样式和目录约定。
3. 涉及多文件、跨项目引用或导入既有模型时，读取 `references/02-multifile-and-fqn.md`。
4. 涉及序列流程、并行、循环、条件或异常分支时，读取 `references/03-dynamic-views.md`。
5. 需要落地项目、配置构建、接入 MCP 或接入 CI 时，按 `references/04-project-integration.md` 执行。
6. 写入前确认目标位置：先读 `references/05-design-repo-layout.md` 判断设计资产归属层级。
7. 完成后执行 `references/04-project-integration.md` 的校验步骤，并按 `checklists/model-quality.md` 自检。

## 图类型路由（速查，likec4 1.58.0 实测）

| 用户想要的图 | LikeC4 写法 | 轨道 |
| --- | --- | --- |
| 系统上下文图 / 容器图 / 组件图 | `view of <element>` + `include`/`exclude` | 一 |
| 部署图 | `deploymentNode` + `instanceOf` + `deployment view` | 一 |
| 场景流程图 | `dynamic view`（默认 diagram 变体） | 一 |
| 时序图 | `dynamic view` + `variant sequence` | 一 |
| 并发流程 | `parallel` / `par`（不可嵌套） | 一 |
| 循环 / 条件分支 / 异常 | **本版本不可用** → Mermaid flowchart | 二 |
| 类图 / 状态机图 / 严格 UML 用例图 / ER 图 | 不支持 | 二或三 |

完整决策树、版本差异和边界说明见 `references/00-diagram-routing.md` 与 `references/03-dynamic-views.md`。

## Stage Router

```text
任何架构建模请求
  -> Stage 0 Intake 与图类型路由: references/00-diagram-routing.md

需要写 specification、model、静态视图或样式
  -> Stage 1 DSL 基础: references/01-likec4-basics.md

需要多文件组织、跨文件引用或导入共享模型
  -> Stage 2 多文件与 FQN: references/02-multifile-and-fqn.md

需要时序流程、并发、步骤下钻，或需确认循环/条件/异常是否可用
  -> Stage 3 Dynamic Views: references/03-dynamic-views.md

需要项目落地、构建脚本、MCP、CI 或漂移检测
  -> Stage 4 项目集成: references/04-project-integration.md

需要决定设计资产放项目层还是全局层
  -> Stage 5 设计仓分层: references/05-design-repo-layout.md
```

推荐执行顺序：

```text
00 -> 01 -> 02 -> 03 -> 04 -> 05
```

## 工具轨道规则

- **轨道一（LikeC4）**：架构真源。上下文图、容器图、组件图、部署图、场景流程图、时序图、并发流程。可校验、可 diff、可被 AI 经 MCP 查询。
- **轨道二（Mermaid）**：用例图、状态机图、条件分支与循环流程图、数据流图、ER 图、甘特图。可由 `likec4 gen mermaid` 导出或独立手写，只作补充产物。
- **轨道三（PlantUML）**：类图、组合与继承、严格 UML 用例图泛化关系。仅在轨道一无法表达时作为逃生层使用。

收敛规则：能用轨道一就不用轨道二；轨道三仅作例外，且必须向用户说明为什么 LikeC4 不支持。

## 资源索引

- `references/00-diagram-routing.md`: 图类型路由决策树、UML 映射、能力边界与轨道选择。
- `references/01-likec4-basics.md`: specification、model、element 样式、静态视图、部署视图和命名约定。
- `references/02-multifile-and-fqn.md`: 多文件组织、`import`/`extend`、跨文件 FQN 规则和常见校验失败。
- `references/03-dynamic-views.md`: 动态视图语法、sequence 变体、并发块、限制，以及 1.58.0 实测可用/不可用特性表。
- `references/04-project-integration.md`: 项目结构、构建脚本、CLI 校验、MCP 接入、CI 漂移检测。
- `references/05-design-repo-layout.md`: 设计资产分层、仓边界、submodule 引用与指针抖动规避。
- `checklists/model-quality.md`: 模型质量自检清单。
- `templates/`: 可落盘模板。
- `templates/c4-project-skeleton.md`: 新设计仓的最小文件骨架模板。
- `evals/evals.json`: 触发与路由评测用例。

## 边界

- 不修改项目业务代码；架构模型落盘位置遵循 `references/05-design-repo-layout.md`。
- 不伪造未知技术栈命令；未确认的命令标为 `待补充`。
- 不把 Mermaid/PlantUML 图倒推成 LikeC4 模型并声称是模型真源。
- **不写入未经当前版本验证的语法**。官方文档中的部分特性（1.58.0 下的 `opt` `loop` `break` `alt` `try`、视图文件夹分组）在当前锁定版本不可用，写入会导致 `validate` 失败。
- LikeC4 1.58.x 要求 Node >= 22.22.3；环境不满足时先报告阻塞，不降级为其他工具假装完成。
- 写入 `.c4` 后必须运行 `likec4 validate`；无法运行时说明原因、降级证据和残余风险。
- 升级 LikeC4 版本后，必须重新验证本技能模板与 references 中的示例，并更新实测表。

## 交付标准

交付时说明：目标图类型与所用轨道、LikeC4 版本、模型或视图文件位置、`likec4 validate` 结果、跨文件引用是否已用 FQN、设计资产归属层级（项目层或全局层）、以及 LikeC4 无法表达而改走轨道二/三的部分及其原因。
