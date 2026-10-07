# SOP 06: Architecture Handoff

## 目标

把架构模型转成**可交接的实现输入**,让实现阶段不必重新分析架构。本 SOP 产出 `implementation-delivery` 能直接消费的规格,同时与 `technical-design` 已有的 Handoff 契约衔接,不重复造轮子。

## When Required

- 架构模型完成并通过 `likec4 validate` 后,进入实现准备阶段
- 实现方需要知道「有哪些组件、边界在哪、依赖怎么走、部署要求是什么」
- `technical-design` 需要架构事实作为其设计输入
- 架构变更后需要重新评估实现影响面

## 核心定位：架构规格是交接的子集,不是替代

架构模型**推不出**代码实现。它能回答「有什么、在哪里、怎么连」,不能回答「怎么做、对不对」。

| 架构规格能提供 | 仍需 technical-design 提供 |
| --- | --- |
| 组件清单与职责边界 | 接口签名、参数类型 |
| 依赖方向与约束 | 错误处理、业务规则 |
| 部署拓扑与运行时要求 | 数据结构、ORM 模型 |
| 关键流程时序 | 边界条件、验收细则 |

**因此本 SOP 的产出是 `Implementation Handoff Mini-Spec` 的架构视角子集**,由 `technical-design` 补齐接口与数据细节后形成完整交接包。本技能不产出可执行代码,也不声称「架构即开发」。

```text
architecture-design（本 SOP）
  └─ 架构规格：组件/边界/依赖/部署/流程
       ↓
technical-design
  └─ 补齐接口契约、数据结构、业务规则 → 完整 Technical Handoff Packet
       ↓
implementation-delivery
```

若需求较小、架构未变,可用本 SOP 的规格直接进入实现,不必强制走完整技术设计。

## 执行步骤

### 1. 从模型取事实,不要凭记忆写

优先经 MCP 查询,避免手抄出错:

```
search-element            定位元素与所在 project
read-project-summary      了解全局结构、可用 kind
subgraph-summary          取组件树与子元素
query-incomers-graph      取上游依赖
query-outgoers-graph      取下游影响面
read-deployment           取部署实例与节点
```

MCP 不可用时读取 `.c4` 源文件,并说明取自哪个文件。

### 2. 产出架构规格

按 `templates/architecture-handoff-spec.md` 输出,必含五部分:

| 部分 | 内容 | 来源 |
| --- | --- | --- |
| 组件边界 | 每个组件的职责、归属层、禁止越界 | `model` 元素的 description |
| 依赖约束 | 谁调谁、方向、禁止反向依赖 | `query-outgoers-graph` |
| 流程锚点 | 关键链路的时序视图 id | `dynamic view` 的 view id |
| 部署要求 | 运行时实例、环境、资源 | `deployment` 模型 |
| 验收锚点 | 每个组件的可验证信号 | 组件职责 + 部署约束 |

**每一条都必须能追溯到模型元素或视图 id。** 写不出模型依据的内容标记为 `待补充`,不凭空补齐。

### 3. 标注置信度

关键架构结论置信度低于 90% 时,不得声明 ready,只能输出缺口与补证动作。置信度依据:

- 模型有明确 description 且无冲突 → 高
- 仅靠元素名推断 → 中,需用户确认
- 依赖外部系统且未验证 → 低,必须标注

### 4. 判断交接路径

| 条件 | 路径 |
| --- | --- |
| 架构未变,仅补实现细节 | 架构规格 + `implementation-delivery` |
| 架构有变更或新增组件 | 架构规格 → `technical-design` 补接口与数据 → 实现 |
| 架构本身尚未定版 | 先完成建模与评审,不产出交接规格 |
| 架构变更影响多个模块 | 先 `reasoning-map` 收敛影响面,再产出规格 |

### 5. 与项目规则同步

架构变更后,项目仓 `AGENTS.md` 的设计仓规则与 `docs/02-development/submodules-index.md` 的 pinned 值需同步。主仓 PR 需说明关联的设计仓提交。

## 与其他技能的边界

- **不替代 `technical-design`**。接口契约、数据结构、业务规则仍由它产出。
- **不生成代码**。本技能无代码生成能力,也不应假装具备。
- **不跳过建模**。模型未通过 `likec4 validate` 时不产出交接规格。
- **不改主仓代码**。架构变更落在设计仓,主仓只更新指针。

## 常见 RED 点

- 产出「架构即代码」的承诺:架构推不出业务规则,强行生成会产出看似完成实则空心的实现。
- 规格里的组件职责与模型 description 不一致,实现方按规格做但模型是另一回事。
- 依赖方向写反:模型里 `a -> b`,规格写成 `b 依赖 a`。
- 流程锚点给出不存在的 view id,实现方无法查阅。
- 置信度全部标 100%:没有说明依据的置信度等于没有置信度。
- 架构刚变更就交接,用的是旧模型的规格。

## 交付标准

交付时说明:架构模型位置与 `likec4 validate` 结果、架构规格落盘位置、取事实的方式(MCP 或读文件)、规格中每部分对应的模型依据、置信度与未达 90% 的项、交接路径判断结论、以及哪些内容必须由 `technical-design` 补齐。
