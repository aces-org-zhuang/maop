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

- **架构模型是唯一真源，且只用 LikeC4**。所有图都必须用 LikeC4 表达，不降级到 Mermaid、PlantUML 或其他工具。平替方案与各自代价见 `references/09-likec4-substitutions.md`。
- **主干先于分支，分支独立成图**。任何视图先只画主干（happy path / 核心链路）并让用户确认，再逐条展开分支；分支各占一张视图，命名 `*-branch-<条件>`，只画增量 + 接缝锚点，不重复主干步骤。视图容量上限：元素 12 / 步骤 8 / 状态 8，超限即拆。**把主干 + 异常 + 降级 + 外围需求塞进一张图是明确错误**——面面俱到即无法评审。详见 `references/11-trunk-first-design.md`。
- **主干确认后即冻结**。分支阶段只能新增视图，不得修改主干模型或主干视图。扩散过程中若发现主干本身有缺陷，走主干变更门禁交用户裁决，**不得"顺手补一下"**——分支反复侵蚀主干会让它失去共识基线。
- **图类型先路由再动手**。写任何图之前先执行 `references/00-diagram-routing.md`，禁止凭印象直接选语法。
- **所有图只用 LikeC4，禁止降级**。没有「LikeC4 画不了所以换工具」的情况。泳道用嵌套容器，状态机用「状态即元素 + 迁移即关系」，分支拆多视图，类图用嵌套 + 依赖，ER 用 `store` 承载实体。每种平替都有代价，交付时说明，不静默换工具。
- **版本敏感，官方文档不等于可用能力**。本技能语法经 **likec4 1.58.0 实机验证**。官方文档描述最新版本，`opt` `loop` `break` `alt` `try` 与视图文件夹分组在 1.58.0 **不可用**。写入未验证语法会让 `validate` 失败。
- **能力边界必须诚实，但不降级**。LikeC4 不原生支持类图继承、状态机外观、泳道竖列。每一种都有 LikeC4 内的平替表达与已知代价，按 `references/09-likec4-substitutions.md` 执行并**把代价告知用户**，不得静默换到另一套工具。
- **写入前必须 validate**。任何 `.c4` 写入后必须运行 `likec4 validate`，非零退出码时不得声明完成。
- **架构设计 FQN 的必要性来自嵌套，不来自「跨文件」这件事本身**。实测：跨文件引用**顶层**元素用 short name 合法；引用**嵌套**元素必须 FQN。**注意区分架构设计 FQN（`.c4` 内元素定位路径）与源码路径引用（`src/x.js`，写在 description 里），两者并列，无派生关系。** Feature 内嵌各环后跨作用域引用一律需 FQN。详见 `references/02-multifile-and-fqn.md`。
- **视图类型由设计层的性质决定，不由文件组织决定**。各层的读者不同，视图形态也不同：US/F/NF 用 element view，I 环步骤用 dynamic view 且状态机用「状态即元素 + 迁移即关系」，UI 环交互面用 element view 而信息设计用表格，SRC 环用 element view + sequence，构建部署用 deployment view。详见 `references/07-design-chain.md`。
- **设计资产分层存放**。单服务设计放项目层设计仓并由主仓 submodule 引用；跨项目视图放全局聚合层，禁止把多个项目的设计塞进同一个被 submodule 引用的仓（会造成 gitlink 指针抖动）。
- **依赖必须锁版本**。LikeC4 跨版本 DSL 行为差异大，`package.json` 用精确版本号而非 `^`。
- **环境问题不是阻塞理由，先降级再上报**。MCP 自带 LikeC4 内核，零安装即可查询模型；本地无 CLI 时走 npx，再不行就只读降级交付。详见 `references/04b-environment-and-sync.md`。
- **不把环境故障误报为模型缺陷**。`EBADENGINE` / `MODULE_NOT_FOUND` / 网络错误是环境问题；`Invalid` + 行号是模型问题。
- **完整需求走设计链，缺一环即不完整**。需求应产出 Feature → US → I → UI → SRC 的可追溯链路，并单独说明构建部署为何此时不产出。各环读者与语言不同：I 环不含源码（换技术栈依然成立），SRC 必须绑定真实文件路径。详见 `references/07-design-chain.md`。
- **`validate` 通过不等于能构建**。`dynamic view` 只有 `include` 没有消息时 `validate` 通过但 `build` 布局失败（`actors array must not be empty`）。交付前必须跑 `build`。
- **交互式推进，不一次性抛全量**。设计是需要人类介入业务判断的环节，AI 负责给候选与推荐，用户负责确认业务决策。按 `references/08-design-decision-tree.md` 的节点 -1 到 6 推进，每个 ⏸ 节点停下等确认，收尾必须输出缺口清单。一次性输出全部内容会导致用户在关键判断上无法纠偏，只能整体返工。
- **只有 Feature 是闭环的开端；起点不是 Feature 就必须先上升**。US / F / NF / I / UI / SRC 任一环作为起点，都要先上升到 Feature 确认交付范围，再逐环下钻。区别只是要跨几环，不是要不要上升。上升到 Feature 时若发现改动超出本次交付边界，**立即停下交用户裁决**，不自行扩大范围——任何环的实现都无权替业务扩大交付范围。
- **产品愿景不是门禁，只作坐标原点**。愿景可证伪性弱，把它设为起点会让范围裁决变成走过场。上升止于 Feature。见 `references/12-design-origin.md`。
- **F 与 NF 是能力单元清单，不是路径环节**。下钻路径只有一条：`US → I → UI → SRC`，两条链相同。F / NF 是与 US **并列**的清单（`Feature ⊃ {US, 清单, I, UI, SRC}`），**US 下钻时中途不经过它们**。把它们画成 `US → F → I` 会同时造成两个误解：暗示 F 属于 US、暗示必须经过 F 才能到 I。**Feature 才是 US 的超集。**
- **验收标准的成分各归各的链**。一条验收标准可能含两种成分：**业务结果判定**（做完了吗/ 做对了吗）属 F 链，**质量判定**（多快 / 多稳 / 多少 / 多久失效）属 NF 链。**F 链 US 的验收标准与交付边界中出现任何数值、时限、比例、可用性词（秒/ms/P95/%/不超过/至少/最多），即为跨链污染**——它本该是 NF 链上一条独立 US，而不是本条 US 的附加条件。混写会让 F 链的验收结论依赖 NF 链的度量，**两条链无法独立验收**。发现污染走成分拆分交用户裁决，**不得静默删除指标**（删除等于丢弃一个质量承诺）。详见 `references/07-design-chain.md`。
- **推演不能停在链内，要跨链接力**。链内闭环后必须沿关联关系**起第二条推演**（NF 链推完起关联 F 链的，F 链推完起关联 NF 链的），重跑红绿循环直到两侧都无法再起新推演。「在原链里检视对方」不算——对方链的红点从未被验证。
- **SRC 环有四个独立维度，缺一不可**。①**代码结构与文件目录**（唯一带真实磁盘路径的环）；②**数据流**（DFD 全景 + 数据载体全景 + 数据模型全景，载体按`IN`/`BIZ`/`POD`/`OUT`/`DAO`/`CVT` 角色编号，**不用 PO/VO/BO/DTO**）；③**对外接口**（API 清单 + **按调用方向划分的泳道时序**，接口编号 `API-<编号> <METHOD> <路径> <名称>`，泳道只是分组手段不是存放位置）；④**运行时**（`deployment` 里的 `processNode` / `threadNode`，需自定义 `deploymentNode`）。四类边 `.trace` / `.depends` / `.flow` / `.convert` 各司其职。详见 `references/07-design-chain.md`。
- **一个 Feature 先分叉，两条链各自闭环，最后在构建部署收敛**。**分出去的是关注点，合回来的是运行现实**。分叉是决策不是标注：两问（新增什么能力 / 保证什么极端场景）都有答案就分出两条链，**各自的 US 分别识别**（不是共享的）。收敛是必然的——两条链的 SRC 进同一制品与运行时。
- **NF 是极端场景下的系统表现，不是「质量属性」**。「性能」「可用性」「可审计性」只是**观察角度**，不是交付物——角度必须落到具体场景才成为 NF 单元。每个 NF 项必须能答出**谁**（角色）、**什么场景**（极端条件）、**因此得到什么**（可感知收益）三项；答不出就是角度名伪装。**NF 链同样有完整 US / I / UI / SRC 与用户参与**，不是约束。详见 `references/12-design-origin.md` 第三节。
- **全景必须同类聚合，一张全景只放一种元素**。`pano-f` 只有 F 单元、`pano-us` 只有 US。**「F 全景」里混入 US 会让这个名字失去意义**——读者无法判断这张图回答什么。单元与 US 的对应关系放在各链的能力清单视图 `chain<链>-f`，那是唯一允许同图出现 US 的例外。
- **链视图按环聚焦，禁止 `include *`**。一张链视图只承载一个环。**I 环必须按内容子类拆图**：业务目标 / 状态流转 / 业务步骤各自成图；状态用「状态即元素 + 迁移即关系」，步骤有责任边界时用**泳道流程图**。`include *` 会把六环加载体加泳道全塞进一张——这是"视图跨层"的真正来源。
- **视图名必须自带类型信息**：`pano-<环>`（同类聚合全景）/ `chain<链>-<环>`（分环）/ `seq<链>-<场景>`（时序）/ `dfd`·`carrier`·`erm`·`api`·`srcdir`·`proc`（SRC 各维度）。连字符可用。
- **全量设计时每一环都要有全景视图**，不只 NF：F/NF/US/I/UI/SRC 六张，另有 I 状态、数据载体、API 三张 SRC 维度全景。**聚合发生在全景层，不发生在链视图层。**
- **推演是红绿循环，不是一次画完的图**。每轮三步：给当前视野所有节点打标（🟢 已覆盖 / 🔴 缺口）→ 选最宽泛的 🔴 判断下钻或横向扩散 → 取最高保真证据把红点转绿或边界化。**每轮必须输出 `Round N Map`**，让用户看到判断如何演进。一轮没取到新证据只是重画图，那是空转不是推进。
- **I 环与 US 环的业务语义不能从源码反推**。改了代码不等于业务目标变了，也不等于没变。这必须问用户，是最容易出错的地方。
- **改完要能同步看到效果**。优先用 MCP 查询确认；需要可视化时用 `serve` 热更新。
- **架构不推导出代码**。模型回答「有什么、在哪里、怎么连」，代码实现回答「怎么做、对不对」。业务规则、边界条件、接口签名无法从拓扑推导，因此本技能**不产出可执行代码**，也不声称「架构即开发」。
- **消除重复而非消除实现**。本技能的交接价值在于：实现阶段不必重新分析架构组件、依赖方向与部署约束。交接按 `references/06-architecture-handoff.md` 执行，产出 `technical-design` 交接包的架构子集。

## 触发后先做什么

0. **先定交付边界并执行分叉**：读取 `references/12-design-origin.md`。先确认本次要交付什么，**再问两问做分叉决策**——「这次要新增什么对外可见的能力」「要保证哪个极端场景下的什么表现」。两问都有答案就分出 `Feature-NNN-F`（能力链）与 `Feature-NNN-NF`（极端场景链），两条链的 US 分别识别，最后在构建与部署收敛。**这是全流程第一道门禁**——交付边界未定就往下走，等于默认需求已清楚；分叉未定就画图，必然把两类关注点混在一条链里。
1. **先定主干与分支的切分**：读取 `references/11-trunk-first-design.md`，确定主干路径、分支清单与视图粒度。**这是先决步骤**——没切分就选图类型，必然产出一张什么都塞的图。
2. 先读取 `references/00-diagram-routing.md`，确认目标图类型及其 LikeC4 表达方式。
2a. 需要泳道、状态机、分支、类图、数据模型或信息设计时，同时读取 `references/09-likec4-substitutions.md` 取平替方案与代价。
2b. **变更起点不是 Feature，或需确认关联影响是否覆盖时，先按 `references/10-design-reasoning.md` 做双向推演**，确定受影响环后再逐环与用户交互。推演在前，交互在后。
3. **先定验证路径**：读取 `references/04b-environment-and-sync.md`，判断走 MCP 还是 CLI。不要因环境缺 likec4 而停止交付。
4. 读取 `references/01-likec4-basics.md`，确认 specification、命名、样式和目录约定。
5. 涉及多文件、跨项目引用或导入既有模型时，读取 `references/02-multifile-and-fqn.md`。
6. 涉及序列流程、并发或步骤下钻时，读取 `references/03-dynamic-views.md`。
7. 需要落地项目、配置构建、接入 MCP 或接入 CI 时，按 `references/04-project-integration.md` 执行。
8. **写入前确认目标位置**：先读 `references/05-design-repo-layout.md` 判断设计资产归属层级。
9. **需求涉及完整设计链时（用户故事、功能/非功能框架、业务状态与步骤、交互与信息设计、源码层映射），先读 `references/07-design-chain.md` 按设计链组织产出。**
10. **需要与用户交互式推进设计时，读 `references/08-design-decision-tree.md`。** 它定义每个节点 AI 该给什么候选、问什么问题、以及何时必须停下等确认。含节点 0 规模判定与节点 6 缺口盘点。
11. 建模完成并准备进入实现时，读 `references/06-architecture-handoff.md` 产出架构交接规格。
12. 完成后执行校验，并按 `checklists/model-quality.md` 自检。

## 图类型路由（速查，likec4 1.58.0 实测）

**所有图都在 LikeC4 内表达。** 平替方案的完整写法与代价见 `references/09-likec4-substitutions.md`。

| 用户想要的图 | LikeC4 写法 | 代价 |
| --- | --- | --- |
| 系统上下文图 / 容器图 / 组件图 | `view of <element>` + `include`/`exclude` | 无 |
| 部署图 | `deploymentNode` + `instanceOf` + `deployment view` | 交付后才产出 |
| 场景流程图 | `dynamic view`（默认 diagram 变体） | 无 |
| 时序图 | `dynamic view` + `variant sequence` | 只连叶子元素；须有显式消息 |
| 并发流程 | `parallel` / `par` | **不可嵌套** |
| 泳道图 | `stage` 类元素作嵌套容器 | 非真泳道，不保证竖列 |
| 状态机 | 状态即元素，迁移即关系 | 不能自环；非经典外观 |
| 条件分支 | 拆成多个视图，各表达一条路径 | 视图数量增加 |
| 循环 | 单次迭代视图 + 循环关系视图 | 需人工拆分 |
| 异常处理 | 独立异常路径视图 | 需人工拆分 |
| 类图 / 组件设计 | 嵌套表达包含，关系表达依赖 | **继承无对应** |
| ER 图 / 数据模型 | `store` 承载实体 | 无字段级、无基数标注 |
| 信息设计 | 界面为容器，字段为元素 | 字段多时图较宽 |
| 用例图 | `actor` 元素 + 关系 | 无 use case 椭圆、无 `<<extend>>` |

**禁止写入**：`swimlane` `lane` `participant` `column`（不存在）；`opt` `loop` `break` `alt` `when` `else` `try` `catch` `finally`（1.58.0 不可用）。

完整决策树与版本差异见 `references/00-diagram-routing.md`、`03-dynamic-views.md`。

## Stage Router

```text
任何架构建模请求
  -> Stage 0a 主干优先与视图切分: references/11-trunk-first-design.md
  -> Stage 0 Intake 与图类型路由: references/00-diagram-routing.md

需要分析变更影响面、确认关联影响是否覆盖、或变更起点不是 US 层
  -> Stage 0c 设计双向推演: references/10-design-reasoning.md

需要泳道、状态机、条件分支、循环、异常、类图、数据模型或信息设计的 LikeC4 表达
  -> Stage 0b 平替方案与代价: references/09-likec4-substitutions.md

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

需求涉及完整设计链（用户故事、功能/非功能框架、业务状态与步骤、交互与信息设计、源码层映射）
  -> Stage 6 设计链: references/07-design-chain.md

需要逐步引导用户完成设计、决定何时停下确认、或产出缺口清单
  -> Stage 7 设计作业决策树: references/08-design-decision-tree.md

建模完成，准备进入实现或需要交接给实现方
  -> Stage 8 Architecture Handoff: references/06-architecture-handoff.md
```

推荐执行顺序：

```text
00 -> 01 -> 02 -> 03 -> 04 -> 05
       ↑ 先做 11（主干与分支切分）
                        └-> 07（六层设计链）-> 06（进入实现前）
```

## 工具轨道规则

**所有图必须用 LikeC4 表达，不允许降级到 Mermaid、PlantUML 或其他工具。** 每种图在 LikeC4 中都有对应表达方式与已知代价，详见 `references/09-likec4-substitutions.md`。

选择 LikeC4 的理由只有一条但足够充分：**单一真源、可校验、可 diff、可被 AI 经 MCP 查询。** 引入第二套工具会让架构真相分裂成两份且无法互相验证。

| 图类型 | LikeC4 表达 | 已知代价 |
| --- | --- | --- |
| 状态机 | 状态即元素，迁移即关系 | 不能自环；非经典状态机外观 |
| 条件分支 | 拆成多个视图，各表达一条路径 | 视图数量增加 |
| 循环 | 单次迭代视图 + 循环关系视图 | 需人工拆分 |
| 异常 | 独立异常路径视图 | 需人工拆分 |
| 类图 / 组件 | 嵌套表达包含，关系表达依赖 | **继承无对应**，须在 description 记录 |
| ER / 数据模型 | `store` 承载实体 | 无字段级、无基数标注 |
| 泳道 | 嵌套容器（`stage` 类元素） | 非真泳道，不保证竖列排列 |
| 信息设计 | 界面为容器，字段为元素 | 字段多时图较宽 |
| 用例图 | `actor` 元素 + 关系 | 无 use case 椭圆、无 `<<extend>>` |

**没有一条路径是零代价的。** 遇到代价较大的场景，**先告知用户代价并让其选择**，不得静默换工具。

**禁止写入的语法**（不存在或本版本不可用）：

```text
swimlane   lane   participant   column
opt   loop   break   alt   when   else   try   catch   finally
```

前四个在官方 `llms-full.txt` 与 1.58.0 中均不存在；后八个在 1.58.0 不可用（官方文档描述的是更新版本）。写入会让 `validate` 失败。

## 资源索引

- `references/11-trunk-first-design.md`: **主干优先与视图分离**。主干先行 T1、一图一意图与容量上限 T2、主干冻结与变更门禁 T3、外围需求隔离、分支清单格式。**先于图类型路由执行。**
- `references/00-diagram-routing.md`: 图类型决策树、LikeC4 表达与代价对照、禁止写入的语法。
- `references/09-likec4-substitutions.md`: 泳道、状态机、条件分支、循环、异常、类图、数据模型、信息设计的 LikeC4 平替写法与各自代价（全部实测通过）。
- `references/10-design-reasoning.md`: 设计双向推演。自上而下与自下而上两条路径、横向扩展触发条件、范围裁决、闭环停止条件。沿用 reasoning-map 的渐进地图与 RED/GREEN 模式。
- `references/01-likec4-basics.md`: specification、model、element 样式、静态视图、部署视图和命名约定。
- `references/02-multifile-and-fqn.md`: 多文件组织、`import`/`extend`、嵌套元素的 FQN 规则（主要服务 SRC 层）与常见校验失败。
- `references/03-dynamic-views.md`: 动态视图语法、sequence 变体、并发块、限制，以及 1.58.0 实测可用/不可用特性表。
- `references/04-project-integration.md`: 项目结构、构建脚本、CLI 校验、MCP 接入、CI 漂移检测。
- `references/04b-environment-and-sync.md`: 零依赖回退链（不装 likec4 也能查询模型）、MCP watch 热重载、同步查看方式、故障降级规则。
- `references/05-design-repo-layout.md`: 设计资产分层、仓边界、submodule 引用与指针抖动规避。
- `references/06-architecture-handoff.md`: 架构交接规格，组件边界、依赖约束、流程锚点、部署要求与验收锚点，供实现阶段直接消费。
- `references/07-design-chain.md`: 设计链的路径环节与能力单元清单区分、各环边界、命名规范、两类门禁（路径完整性 + 清单对应）、两类边区分与工具路由。
- `references/12-design-origin.md`: **设计起点与切分维度**。交付边界确认、F 链与 NF 链的划分与同构关系、跨链边禁令、文件物理隔离、增量与全量两种模式、归属嵌套表达、变更上升路径。
- `references/08-design-decision-tree.md`: 设计作业决策树，节点 0-6 的引导流程、每步的确认点、场景分支与反模式。
- `checklists/model-quality.md`: 模型质量自检清单。
- `templates/`: 可落盘模板。
- `templates/c4-project-skeleton.md`: 新设计仓的最小文件骨架模板（已实机验证）。
- `templates/architecture-handoff-spec.md`: 架构交接规格模板，字段与 `technical-design` 的 Handoff Mini-Spec 对齐。
- `templates/design-chain.md`: 设计链落盘骨架，含已实测通过的 element kind 与必备视图。
- `evals/evals.json`: 触发与路由评测用例。

## 边界

- 不修改项目业务代码；架构模型落盘位置遵循 `references/05-design-repo-layout.md`。
- **不在一张视图里混合主干、分支与外围需求**。超容量即拆，不以"内容完整"为理由把分支塞回主干。
- **不在分支展开中就地修改已冻结的主干**；主干缺陷走变更门禁交用户裁决。
- 不伪造未知技术栈命令；未确认的命令标为 `待补充`。
- 不把 Mermaid/PlantUML 图倒推成 LikeC4 模型并声称是模型真源。
- **不写入未经当前版本验证的语法**。官方文档中的部分特性（1.58.0 下的 `opt` `loop` `break` `alt` `try`、视图文件夹分组）在当前锁定版本不可用，写入会导致 `validate` 失败。
- **环境缺 likec4 不是停止交付的理由**。MCP 自带内核可零安装查询模型；CLI 可用 npx；仍不可用时照常交付模型文件并标注未校验风险。
- 写入 `.c4` 后应运行 `likec4 validate`；无法运行时必须说明原因、降级证据和残余风险，**不得声称已校验**。
- 升级 LikeC4 版本后，必须重新验证本技能模板与 references 中的示例，并更新实测表。

## 交付标准

默认交付模型与视图位置、验证路径（MCP / CLI / npx / 只读降级）、`likec4 validate` 结果或未校验原因、嵌套元素引用是否已用 FQN（顶层元素不应被强制写全名）、设计资产归属层级（项目层或全局层），以及使用了哪些平替方案及其代价（见 `references/09-likec4-substitutions.md`）。

**追加（主干优先，规则见 `references/11-trunk-first-design.md`）**：主干路径一句话说明；分支清单（编号 / 条件 / 归属环 / 优先级 / 是否本次交付）；视图分工（哪张是主干视图、哪张是分支视图、各自回答什么问题）；每张视图的元素或步骤数是否在上限内；主干是否已冻结、本次是否发生过主干变更（若有附门禁记录）；登记但未展开的分支及原因。

**进入实现阶段时追加**：架构交接规格落盘路径（`vendor/design/<repo>/handoff/current.md`）与模型版本、取事实方式（MCP 或读文件）、规格各部分对应的模型依据、置信度与未达 90% 的项、建议交接路径（直接实现 / 先技术设计 / 先完成建模），以及必须由 `technical-design` 补齐的内容清单。
