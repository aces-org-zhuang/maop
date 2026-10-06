# SOP 00 - 图类型路由与能力边界

## Goal

在写任何图之前，先确定「这张图属于哪一类、该用哪条轨道、LikeC4 能不能表达」。避免用错语法硬凑，避免伪造 LikeC4 不支持的图类型，避免把导出物误当架构真源。

## When Required

每次使用 `architecture-design` 技能时都必须先执行本 SOP。它是唯一入口路由，不允许跳过。

## 决策树

```text
用户要画什么图？
├─ 架构结构类
│  ├─ 系统上下文 / 全景 / 系统间关系 -> view（轨道一）
│  ├─ 容器级（服务、库、外部依赖）  -> view of <system>（轨道一）
│  ├─ 组件级（模块内部）             -> view of <component>（轨道一）
│  ├─ 部署 / 运行时拓扑 / 环境       -> deployment view（轨道一）
│  └─ 基础设施 / 节点 / 区域         -> deployment view（轨道一）
│
├─ 时序与流程类
│  ├─ 某个 use-case 或场景怎么走     -> dynamic view（默认 diagram 变体，轨道一）
│  ├─ 标准 UML 时序图                -> dynamic view + variant sequence（轨道一）
│  ├─ 并发                          -> parallel / par（轨道一，不可嵌套）
│  ├─ 循环 / 条件 / 异常             -> 本版本不可用，转 Mermaid flowchart（轨道二）
│  └─ 分步下钻到更细粒度             -> navigateTo（轨道一）
│
├─ LikeC4 不支持的类型
│  ├─ 类图 / 组合 / 继承 / 泛化      -> Mermaid 或 PlantUML（轨道二/三）
│  ├─ 状态机图                       -> Mermaid stateDiagram（轨道二）
│  ├─ 严格 UML 用例图（use case 椭圆 + <<extend>>）
│  │                                 -> PlantUML（轨道三），必须说明 LikeC4 不支持
│  └─ ER 图                          -> Mermaid erDiagram（轨道二）
│
└─ 纯视觉表达产物（非架构）
   └─ 界面草图、视觉稿、信息图 -> 转 expression-delivery，不在本技能范围
```

## 图类型速查（likec4 1.58.0 实测）

| 用户想要的图 | LikeC4 写法 | 轨道 | 实测状态 |
| --- | --- | --- | --- |
| 系统上下文图 / 全景 | `view` | 一 | 可用 |
| 容器图 | `view of <system>` | 一 | 可用 |
| 组件图 | `view of <component>` | 一 | 可用 |
| 部署图 | `deploymentNode` + `instanceOf` + `deployment view` | 一 | 可用 |
| 场景流程图 | `dynamic view`（diagram 变体） | 一 | 可用 |
| 时序图 | `dynamic view` + `variant sequence` | 一 | 可用 |
| 并发流程 | `parallel` / `par` | 一 | 可用（不可嵌套） |
| 条件分支 / 循环 / 异常 | `alt` / `loop` / `try` | — | **本版本不可用**，走轨道二 |
| 类图 / 继承 / 泛化 | 不支持 | 二/三 | Mermaid classDiagram 或 PlantUML |
| 状态机图 | 不支持 | 二 | Mermaid stateDiagram-v2 |
| 严格 UML 用例图（<<extend>>） | 不支持 | 三 | PlantUML，必须说明差异 |
| ER 图 | 不支持 | 二 | Mermaid erDiagram |

> 官方文档描述的是最新版本。`opt` `loop` `break` `alt` `try` 在官方文档中存在，但 **1.58.0 实测不可用**。使用前必须确认版本，详见 `references/03-dynamic-views.md` 的实测表。

## UML 概念到 LikeC4 的映射

| UML 概念 | LikeC4 对应 | 差异与注意 |
| --- | --- | --- |
| System Context Diagram | `view`，包含 actor 与 system | 一致 |
| Container Diagram | `view of <system>` | 一致 |
| Component Diagram | `view of <component>` | 一致 |
| Deployment Diagram | deployment view | 一致 |
| Sequence Diagram | `dynamic view` + `variant sequence` | 无生命线（lifeline）与激活棒（activation bar）；只支持叶子元素之间的连接 |
| Use Case Diagram（场景流程） | `dynamic view`（diagram 变体） | **语义不同**：LikeC4 表达「一次交互的时间顺序」，不是「参与者—目标」矩阵；无 use case 椭圆、无 include/extend 关系 |
| Communication Diagram | `dynamic view`（diagram 变体） | 接近 |
| State Machine Diagram | 无 | 走 Mermaid `stateDiagram-v2` |
| Class Diagram | 无 | 走 Mermaid `classDiagram` 或 PlantUML |
| ER Diagram | 无 | 走 Mermaid `erDiagram` |
| Activity / DFD | `dynamic view`（diagram 变体） | 结构相似但非等价，不承诺 DFD 语义 |

## 硬边界（必须诚实告知用户）

以下能力 LikeC4 **不提供**，不得用错误语法硬凑，不得静默降级：

1. **类图与继承体系**。C4 Level 4（代码级建模）仍是社区讨论议题，不是既有能力。
2. **UML 生命线与激活棒**。sequence 变体只渲染参与者顺序与消息，不表达对象生命周期。
3. **strict use case 泛化**。`<<extend>>` / `<<include>>` 关系没有对应写法。
4. **状态机**。无状态定义与转移图原语。
5. **native ER 建模**。无实体关系原语，只能借道 Mermaid。
6. **视图文件夹分组**。`views 'Label' { ... }` 在 1.58.0 不可用，改用按用途拆分文件。

另外，官方文档中的 `opt` `loop` `break` `alt` `try` 流程控制块在 **1.58.0 不可用**。用户要求条件分支、循环或异常处理时，必须改走轨道二或升级 LikeC4 版本，不得直接写入这些语法。

需要这些内容时，按顺序尝试：

```text
轨道一无法表达
  -> 轨道二 Mermaid（用例图/状态机/ER）
  -> 轨道三 PlantUML（类图/继承/严格 UML 用例图）
  -> 都无法表达 -> 告知用户并建议外部工具，不要伪造
```

## 轨道收敛规则

- 架构真相只能有一个来源。LikeC4 模型是结构化真源；Mermaid/PlantUML 是单向导出物或补充产物。
- 不得从 Mermaid/PlantUML 图反推生成 LikeC4 模型后，声称该模型是从图「还原」的真源。若确需建模，必须从代码或设计意图重新建模。
- 轨道二/三的产物若需与模型保持同步，必须由模型导出（如 `likec4 gen mermaid`），并在交付说明中指出来源方向。

## 常见失败模式

- 用户说「画用例图」，直接用 `dynamic view` 硬凑并宣称是 UML 用例图——语义不符，必须说明差异。
- 用户要类图，用 element 嵌套模拟继承——错误做法，应走轨道二/三。
- 在 `variant sequence` 中连接有子元素的容器——不受支持，sequence 只接受叶子元素。
- 同时维护 LikeC4 模型和手写 Mermaid 图，且两者无生成关系——必然漂移。
- 把 `par`/`opt`/`loop` 等流程控制块当稳定特性使用，未标注 experimental 风险。

## 与其他技能的边界

- 本技能决定「架构图用什么工具表达」；`expression-delivery` 决定「非架构的表达产物如何呈现」。
- 本技能产出的架构模型是 `technical-design` 的架构确认输入之一。`technical-design` 的 `sop-02b-architecture-confirmation.md` 要求 Context / Component / Deployment 图，可由本技能用 LikeC4 落地，而不是手画 Mermaid。
- 产品用例与验收标准属 `product-definition`，架构建模不替代产品定义。
