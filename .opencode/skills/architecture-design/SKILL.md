---
name: architecture-design
description: 必须用于用 LikeC4 DSL 编写架构即代码、维护架构模型、补充架构视图、产出架构交接规格，或用户要上下文图、容器图、组件图、部署图、场景流程图、时序图、架构漂移检测、架构评审、跨项目架构视图、架构影响面、架构约束交给实现时。用户说“画架构图”“建模”“写 c4 文件”“架构即代码”“likec4”“部署图怎么看”“时序图用 LikeC4 怎么画”“架构和代码不一致”“架构漂移”“跨项目架构全景”“架构定版后交给开发”“实现阶段要架构边界”时优先使用本技能；不要用于产品用例定义、代码实现、接口契约与数据结构设计、纯视觉表达产物或类图与状态机等 LikeC4 不支持的图类型。
---

# Architecture Design

本技能用于把架构作为代码来建模、校验、发布和协作。`SKILL.md` 只做路由、图类型决策和能力边界；具体语法、工作流和校验步骤按需读取 `references/`。

## 执行模型

采用短路由层 + SOP 渐进执行。主 LLM 负责图类型选型、模型写入决策、最终校验和交付；子代理只用于跨文件影响面排查和独立评审。

```text
intake -> 图类型路由 -> sop-01..05 执行 -> validate -> 交付
```

## 语言契约（默认中文，必读）

架构图是给人评审的，不是给编译器读的。**默认用中文书写所有面向人的文本。**

| 内容 | 语言 | 示例 |
| --- | --- | --- |
| 元素显示名 `title` | **中文** | `应答编排器`、`微信客服回调入口` |
| 元素描述 `description` | **中文** | `决定自动回复还是转人工` |
| 视图标题与描述 | **中文** | `系统上下文`、`应答链路` |
| 关系标签 | **中文** | `请求应答`、`检索候选知识` |
| 部署节点名 | **中文** | `本地开发环境`、`应用层` |
| 标识符（元素 id、视图 id） | **英文** | `answerOrchestrator`、`answerPath` |
| 技术专有名词 | **保留原文** | `RAGFlow`、`LLM Wiki`、`Node.js`、`HTTP`、`JSON`、`API` |

### 为什么标识符保持英文

标识符会变成导出文件名（`likec4 export png`）和分享 URL 路径。改标识符等于断掉已有链接，也会让 CI 产物路径不稳定。显示名可以随时改，标识符不要动。

### 技术专有名词不要翻译

`RAGFlow`、`LLM Wiki`、`WeChat Work` 译成中文反而降低可读性——团队日常说的就是这些词。文件路径、端口、命令同理：

```c4
description '以 JSON 文件承载状态；src/domain/store.js'    // ✓ 路径保留
title 'localhost:9380'                                      // ✓ 端点保留
title '美妆客服服务'                                        // ✓ 业务词翻译
title 'RAGFlow 知识库'                                      // ✓ 专有名词 + 中文类别
```

### 写完自检

交付前确认没有遗漏的英文面向文本：

```bash
grep -hoE "(title|description) '[^']*'" src/**/*.c4 | grep -oE "'[^']*'" \
  | grep -E "[A-Za-z]{4,}" | grep -vE "RAGFlow|LLM|Node|HTTP|HTTPS|JSON|API|src/|localhost"
```

有输出说明还有未翻译的文本，逐条处理。技术专有名词被误报时，把该词加入排除列表再确认。

## 核心原则

- **架构模型是唯一真源**。LikeC4 模型是结构化、可校验、可被 AI 查询的真源；Mermaid/PlantUML 只作为导出物或补充层，不反向成为架构真相。
- **图类型先路由再动手**。写任何图之前先执行 `references/00-diagram-routing.md`，禁止凭印象直接选语法。
- **版本敏感，官方文档不等于可用能力**。本技能语法经 **likec4 1.58.0 实机验证**。官方文档描述最新版本，`opt` `loop` `break` `alt` `try` 与视图文件夹分组在 1.58.0 **不可用**。写入未验证语法会让 `validate` 失败。
- **能力边界必须诚实**。LikeC4 不支持类图、状态机图、严格 UML 用例图；不得伪造或用错误语法硬凑，改走轨道二/三并向用户说明。
- **写入前必须 validate**。任何 `.c4` 写入后必须运行 `likec4 validate`，非零退出码时不得声明完成。
- **跨文件必须用 FQN**。short name 不跨文件继承容器作用域，跨文件引用一律使用完整限定名，否则 `validate` 必然失败。
- **设计资产分层存放**。单服务设计放项目层设计仓并由主仓 submodule 引用；跨项目视图放全局聚合层，禁止把多个项目的设计塞进同一个被 submodule 引用的仓（会造成 gitlink 指针抖动）。
- **依赖必须锁版本**。LikeC4 跨版本 DSL 行为差异大，`package.json` 用精确版本号而非 `^`。
- **环境问题不是阻塞理由，先降级再上报**。MCP 自带 LikeC4 内核，零安装即可查询模型；本地无 CLI 时走 npx，再不行就只读降级交付。详见 `references/04b-environment-and-sync.md`。
- **不把环境故障误报为模型缺陷**。`EBADENGINE` / `MODULE_NOT_FOUND` / 网络错误是环境问题；`Invalid` + 行号是模型问题。
- **改完要能同步看到效果**。优先用 MCP 查询确认；需要可视化时用 `serve` 热更新。
- **架构不推导出代码**。模型回答「有什么、在哪里、怎么连」，代码实现回答「怎么做、对不对」。业务规则、边界条件、接口签名无法从拓扑推导，因此本技能**不产出可执行代码**，也不声称「架构即开发」。
- **消除重复而非消除实现**。本技能的交接价值在于：实现阶段不必重新分析架构组件、依赖方向与部署约束。交接按 `references/06-architecture-handoff.md` 执行，产出 `technical-design` 交接包的架构子集。

## 触发后先做什么

1. 先读取 `references/00-diagram-routing.md`，确认目标图类型及其对应工具轨道。
2. **先定验证路径**：读取 `references/04b-environment-and-sync.md`，判断走 MCP 还是 CLI。不要因环境缺 likec4 而停止交付。
3. 读取 `references/01-likec4-basics.md`，确认 specification、命名、样式和目录约定。
4. 涉及多文件、跨项目引用或导入既有模型时，读取 `references/02-multifile-and-fqn.md`。
5. 涉及序列流程、并发或步骤下钻时，读取 `references/03-dynamic-views.md`。
6. 需要落地项目、配置构建、接入 MCP 或接入 CI 时，按 `references/04-project-integration.md` 执行。
7. 写入前确认目标位置：先读 `references/05-design-repo-layout.md` 判断设计资产归属层级。
8. **建模完成并准备进入实现时，读 `references/06-architecture-handoff.md` 产出架构交接规格。**
9. 完成后执行校验，并按 `checklists/model-quality.md` 自检。

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

环境未安装 likec4、或需要同步查看改动效果
  -> Stage 4b 环境自适配与同步: references/04b-environment-and-sync.md

需要决定设计资产放项目层还是全局层
  -> Stage 5 设计仓分层: references/05-design-repo-layout.md

建模完成，准备进入实现或需要交接给实现方
  -> Stage 6 Architecture Handoff: references/06-architecture-handoff.md
```

推荐执行顺序：

```text
00 -> 01 -> 02 -> 03 -> 04 -> 05
                        └-> 06（进入实现前）
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
- `references/04b-environment-and-sync.md`: 零依赖回退链（不装 likec4 也能查询模型）、MCP watch 热重载、同步查看方式、故障降级规则。
- `references/05-design-repo-layout.md`: 设计资产分层、仓边界、submodule 引用与指针抖动规避。
- `references/06-architecture-handoff.md`: 架构交接规格，组件边界、依赖约束、流程锚点、部署要求与验收锚点，供实现阶段直接消费。
- `checklists/model-quality.md`: 模型质量自检清单。
- `templates/`: 可落盘模板。
- `templates/c4-project-skeleton.md`: 新设计仓的最小文件骨架模板（已实机验证）。
- `templates/architecture-handoff-spec.md`: 架构交接规格模板，字段与 `technical-design` 的 Handoff Mini-Spec 对齐。
- `evals/evals.json`: 触发与路由评测用例。

## 边界

- 不修改项目业务代码；架构模型落盘位置遵循 `references/05-design-repo-layout.md`。
- 不伪造未知技术栈命令；未确认的命令标为 `待补充`。
- 不把 Mermaid/PlantUML 图倒推成 LikeC4 模型并声称是模型真源。
- **不写入未经当前版本验证的语法**。官方文档中的部分特性（1.58.0 下的 `opt` `loop` `break` `alt` `try`、视图文件夹分组）在当前锁定版本不可用，写入会导致 `validate` 失败。
- **环境缺 likec4 不是停止交付的理由**。MCP 自带内核可零安装查询模型；CLI 可用 npx；仍不可用时照常交付模型文件并标注未校验风险。
- 写入 `.c4` 后应运行 `likec4 validate`；无法运行时必须说明原因、降级证据和残余风险，**不得声称已校验**。
- 升级 LikeC4 版本后，必须重新验证本技能模板与 references 中的示例，并更新实测表。

## 交付标准

默认交付模型与视图位置、验证路径（MCP / CLI / npx / 只读降级）、`likec4 validate` 结果或未校验原因、跨文件引用是否已用 FQN、设计资产归属层级（项目层或全局层），以及 LikeC4 无法表达而改走轨道二/三的部分及其原因。

**进入实现阶段时追加**：架构交接规格落盘路径（`vendor/design/<repo>/handoff/current.md`）与模型版本、取事实方式（MCP 或读文件）、规格各部分对应的模型依据、置信度与未达 90% 的项、建议交接路径（直接实现 / 先技术设计 / 先完成建模），以及必须由 `technical-design` 补齐的内容清单。
