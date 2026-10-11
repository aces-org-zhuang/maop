# SOP 07 - 设计链（愿景 → Feature → US → I → UI → SRC → 构建部署）

## 目的

架构不是画一张系统图就结束。一个需求从提出到落地要穿过多个环节，每环都有**不同的读者、不同的语言、不同的验收标准**。混在一起会导致业务方看不懂、工程师没细节、评审无法定位问题。

本 SOP 定义各环的边界、命名、产出物与追溯要求。**起点（交付边界、Feature 分类、归属表达）见 `12-design-origin.md`。**

落盘骨架见 `templates/design-chain.md`，其中所有 `.c4` 代码块均经 likec4 1.58.0 实测通过（`✓ Valid` → `build` 输出 `✓ all views layouted`）。

```text
产品愿景        长期方向，坐标原点，不承载追溯门禁
 ↓
Feature        一次可交付增量。F 类（功能主导）/ NF 类（质量主导）
 ↓
US             意图与验收标准
 ↓
I              业务目标、业务状态、业务步骤（不含源码）
 ↓
UI             交互设计（系统如何反馈）、信息设计（展示什么）
 ↓
SRC            类设计、组件设计、时序图、数据流图
 ↓
构建与部署      SRC 的运行投影，交付落地之后才产出
```

**F（功能框架）与 NF（非功能框架）不是独立环节**，它们是 Feature 层的内部分类。理由与判定见 `12-design-origin.md` 第三节。

---

## 集合关系（四组，不可混同）

| 关系 | 性质 | 是否可判定 |
| --- | --- | --- |
| 设计域 ⊃ 各环 | 包含。缺一环即为不完整设计 | 是，缺环即报缺失 |
| Feature ⊃ US | 包含。US 是 Feature 的子元素 | 是，嵌套即归属 |
| F 类 ∪ NF 类 = 全部 Feature | 划分。判据是对外可见能力是否变化 | 是 |
| SRC → 构建部署 | 投影。`instanceOf` 引用，非上下游 | 是 |

**追溯门禁是一条链，聚合关系不是。** Feature ⊃ US 是结构包含，`Feature .trace US` 不必另写——嵌套已经表达了这层归属。

---

## 一、各层职责与边界

### US 层 · 用户故事

**产出物**：用户故事清单，每条含 `US-<编号> <标题>`、用户角色、期望、验收标准。

**回答的问题**：谁在什么场景下要完成什么，做成什么样算完成。

**不属于本层**：技术方案、界面细节、类设计。

### F 层 · 功能框架（Feature 层的内部分类）

**产出物**：`F-<编号> <功能名>`，描述该 Feature 对外提供的能力单元。

**回答的问题**：本次交付让系统能做什么。

**归属**：F 项是所属 Feature 的功能侧，不是独立环节。F 类 Feature 下必有实质 F 项；NF 类 Feature 下**显式声明无需新增**，不沉默跳过。

**不属于本环**：具体实现、业务步骤、界面元素。

### NF 层 · 非功能框架（Feature 层的内部分类）

**产出物**：`NF-<编号> <质量属性名>`，如性能、可用性、安全性、可审计性、可维护性、兼容性。

**回答的问题**：系统必须做到什么程度。

**归属**：NF 项是所属 Feature 的质量侧。NF 类 Feature 下 NF 是**本次主要产出**；F 类 Feature 下 NF 作为附带约束。

**必须可度量**。「系统要快」不合格；「下单 P95 ≤ 500ms」合格。无法度量的 NF 项应标记为 `待补充`，不凭想象编造。

**NF 的落实路径**：通过所属 Feature 的 US 验收标准落到可感知收益上，不再横切各环。详见 `12-design-origin.md` 第三节。

### I 层 · 实现层（业务设计）

**产出物**：`I-<编号> <类型> <名称>`，三类：

| 编号段 | 内容 | 判据 |
| --- | --- | --- |
| 业务目标 | 该功能要达成的业务结果 | 描述收益，不描述手段 |
| 业务状态 | 业务对象的生命周期状态机 | 状态名 + 允许迁移 |
| 业务步骤 | 达成目标的操作序列 | 步骤 + 参与角色 |

**这一层完全不涉及源码**。判断标准：**换一个人、换一种技术栈来实现，这层设计依然成立**。一旦出现类名、函数名、表名，就越界了。

**为什么单独设 I 层**：业务方评审时看的就是这层。如果业务目标、状态、步骤混在技术方案里，业务方无法评审——这是设计与需求脱节的根因。

### UI 层 · 界面层

**产出物**：`UI-<编号> <类型> <名称>`，两类，缺一不可：

| 类型 | 内容 | 必须回答 |
| --- | --- | --- |
| 交互设计 | 系统对用户操作的响应 | 每个操作触发什么、反馈什么、失败怎么回退、可否撤销 |
| 信息设计 | 系统需要展示的信息 | 字段、列表、可见区域、筛选区域、扩展功能（通知、导出、批量操作） |

**交互设计不等于界面布局**。按钮长什么样、颜色如何是视觉设计；交互设计关注的是**行为与反馈**。

**信息设计的常见遗漏**：空状态、加载状态、错误状态、无权限状态。这四种必须在设计里出现，否则实现时会临时发明，导致不一致。

### SRC 层 · 源码层

**产出物**：`SRC-<编号> <单元名>` + 真实文件路径。

**回答的问题**：代码怎么组织。

**必须绑定真实路径**。`SRC-002 订单服务 → src/services/order-service.js`，而不是「订单服务模块」。没有路径约束的 SRC 层会与实际代码脱节。

**本层可包含**：类设计、组件设计、时序图、数据流图、依赖方向。

**边界**：I 层说「状态如何迁移」，SRC 层说「哪个类的哪个方法执行迁移」。前者不含源码，后者必须含。

### 构建与部署（SRC 的运行投影）

**方向是 SRC → 部署，不是上下游环节。** 部署视图的全部内容来自 `instanceOf` 引用 SRC 元素，它是对SRC 的展开，不是 SRC 的后继。

只有当设计落地为代码后才产出：CI 流程、镜像、环境拓扑、发布策略、回滚方案。**在设计阶段不产出构建部署图**——它依赖最终实现，提前画必然返工。

例外：部署形态会影响架构决策（如是否需要跨网络隔离），此时只记录**约束**，不画完整部署图。

---

## 二、命名规范（强制）

| 环 | 格式 | 示例 |
| --- | --- | --- |
| Feature | `Feature-<三位编号> <标题>` | `Feature-001 结算下单` |
| US | `US-<三位编号> <标题>` | `US-001 提交订单` |
| F | `F-<三位编号> <功能名>` | `F-001 订单功能` |
| NF | `NF-<三位编号> <质量属性>` | `NF-001 可审计性` |
| I | `I-<三位编号> <类型> <名称>` | `I-002 业务状态 订单状态机` |
| UI | `UI-<三位编号> <类型> <名称>` | `UI-002 信息设计 订单列表信息` |
| SRC | `SRC-<三位编号> <单元名>` | `SRC-002 订单服务` |

编号**全局唯一且不复用**。删除元素后编号不回收，避免历史引用失效。

**语言**：编号与显示名分隔。编号前缀是英文（跨工具稳定），显示名用中文。依据 `01-likec4-basics.md` 的语言契约。

---

## 三、追溯要求（硬门禁）

### 链路必须完整

```text
Feature → US → I → UI → SRC
```

**任一环缺失即为不完整设计**，必须在交付时明确报告缺失哪一环，不能静默跳过。

理由：环间追溯是这套体系的全部价值。如果 US 直接连到 SRC，就退化成「画了个系统图」，业务方无法参与，评审无法定位断点。

**F 与 NF 不在门禁里**——它们是 Feature 的内部分类，不是链上一环。**没有「US → F 或 NF」这种写法**，那是把从属关系写成了并列关系。

### 两类边必须可区分

**追溯边**回答「为什么连」，**依赖边**回答「运行时怎么走」。两者用不同 relationship kind 表达，不可混用同一箭头。

```c4
specification {
  relationship trace {
    notation '追溯'
    line solid
    color secondary
  }
  relationship depends {
    notation '依赖'
    line solid
    color green
  }
}

model {
  feat.us_place .trace feat.i_step '落为业务步骤'
  feat.i_step .trace feat.src_checkout '落到实现'
  feat.src_checkout .depends feat.paymentClient '调用支付网关'
}
```

**为什么必须分开**：依赖节点（如 `paymentClient`）没有入追溯边，但不代表它是超范围实现——它只是依赖链上的中间节点。混用箭头时，追溯门禁无法区分「超范围」与「纯依赖」。

> 实测记录（likec4 1.58.0）：`✓ Valid` 且 `build` 输出 `✓ all views layouted`。语法是 `a .kind b`（点号在两端之间），**不是** `kind a -> b`（前缀写法会报 `Duplicate element name`）。`line` / `color` 写在 relationship 块**顶层**，写进 `style { }` 会解析失败。

### 父子之间不可连边

嵌套本身已表达包含关系，**不能再补一条边说明包含**：

```c4
src_checkout .depends src_checkout.validate '委派'
→ Invalid parent-child relationship
```

SRC 内部的父子组件依赖必须靠嵌套表达，不能靠边。

### 追溯关系要写明语义

关系标签必须说明**为什么连接**，不能只写「关联」。

### 反向检查

每个 SRC 单元应能回答：**它服务于哪个 I 环步骤或 UI 元素**。答不上的 SRC 单元分两种情况：超范围实现（报待确认），或纯依赖节点（确认后标注为依赖链中间节点）。不可一律判为超范围。

---

## 四、LikeC4 映射（1.58.0 实测）

### element kind 定义

```c4
specification {
  element feature     { style { shape rectangle } }
  element userStory { style { shape document } }
  element function   { style { shape rectangle } }
  element nonFunction { style { shape mobile } }
  element implStep   { style { shape rectangle } }
  element uiSurface  { style { shape browser } }
  element srcUnit    { style { shape component } }
  element system

  relationship trace {
    notation '追溯'
    line solid
    color secondary
  }
  relationship depends {
    notation '依赖'
    line solid
    color green
  }
}
```

**shape 合法值实测**：`rectangle` `component` `storage` `cylinder` `browser` `mobile` `person` `queue` `bucket` `document`。**没有 `hexagon`**，非功能框架用 `mobile` 或 `cylinder` 区分。

### 元素归属用嵌套表达

每一环的元素嵌套在所属 Feature 之下，**这样任何视图打开都能看到归属**：

```c4
model {
  feat_checkout = feature 'Feature-001 结算下单' {
    description '本次交付：客服在对话中可直接完成下单。'

    us_place = userStory 'US-001 提交订单' { }
    us_pay   = userStory 'US-002 完成支付' { }

    i_step = implStep 'I-001 业务步骤' { }

    src_checkout = srcUnit 'SRC-001 结算入口' { }
  }
}

views {
  view usLayer of feat_checkout {
    title 'US 层视图 · 归属于 Feature-001'
    include *
  }
}
```

嵌套后**跨作用域引用嵌套元素必须用 FQN**（`feat_checkout.us_place`）。详见 `02-multifile-and-fqn.md`。

### 五个实测约束

| 约束 | 说明 |
| --- | --- |
| **不支持通配 include** | `include f_*` 会报 `Expecting token of type '}' but found '*'`。分层视图必须逐个列出元素 |
| **sequence 必须有消息** | 只有 `include` 没有消息时，布局报 `actors array must not be empty`，且 `likec4 validate` 仍通过——**只 validate 发现不了** |
| **sequence 只连叶子元素** | `variant sequence` 下不可连有子元素的容器 |
| **父子之间不可连边** | `parent .depends parent.child` 报 `Invalid parent-child relationship`。包含关系已由嵌套表达 |
| **relationship 语法是 `a .kind b`** | 前缀写法 `kind a -> b` 会报 `Duplicate element name`。`line` / `color` 在块顶层，不写 `style { }` |

第二条尤其要注意：`validate` 通过但 `build` 失败。只跑 validate 会漏掉。

### 必备视图

必备的跨环视图如下，各环专属视图见下一节：

| 视图 | 覆盖环 | 用途 |
| --- | --- | --- |
| 链路总览 | Feature → SRC 全链 | 架构评审 |
| 业务设计视角 | Feature/US/F/NF/I/UI，**不含 SRC** | 业务方确认 |
| 源码实现视角 | I/UI/SRC | I 环如何落到代码 |
| 功能与非功能框架 | Feature + US + F + NF | 产品与架构 |
| 设计时序 | I/UI/SRC，`variant sequence` | 工程师 |

---

## 五、环与视图类型的对应关系

**视图类型由该环的性质决定，不由「是否跨文件」决定。** 每环的读者不同，视图的形态也不同。

| 环 | 主视图类型 | 可用视图类型 | 主要读者 | 关键要求 |
| --- | --- | --- | --- | --- |
| Feature | `element view` | element | 产品与业务 | 一句话说清本次交付边界 |
| US | `element view` | element | 全体 | 验收标准必须可判定 |
| F / NF | `element view` | element | 产品与架构 | NF 项与 F 项同图可见，便于对照 |
| I | `dynamic view`（步骤序列） | dynamic + 状态机视图 | 业务方 | **不含 SRC 元素** |
| UI | `element view`（交互面） | element + 表格 | 设计与前端 | 交互与信息设计都要出现 |
| SRC | `element view` + `variant sequence` | element + dynamic + 数据流 | 工程师 | 嵌套引用需 FQN |
| 构建部署 | `deployment view` | deployment | 运维 | 交付后才产出 |

### 为什么这样分配

- **Feature / US / F / NF 是静态结构**，用 `element view` 表达「谁包含谁、谁要求谁」。
- **I 环的核心是步骤与状态**。步骤序列用 `dynamic view`（diagram 变体）；**状态机用「状态即元素 + 迁移即关系」表达**，见 `09-likec4-substitutions.md`。
- **UI 环是静态面 + 动态反馈的组合**：交互面用 element view 表达「哪个界面触发哪个行为」，信息设计（字段、列表、筛选区、通知）用表格更清晰，硬塞进图会失焦。
- **SRC 环是唯一需要多种视图的环**：组件结构用 element view，调用时序用 `variant sequence`，数据流向用 element view 的依赖关系表达。
- **构建部署用 `deployment view`**，且只在交付落地后产出。

### 跨环视图

除各环自己的视图外，必须有跨环视图承载追溯链：

| 视图 | 覆盖环 | 用途 |
| --- | --- | --- |
| 链路总览 | Feature → SRC 全链 | 架构评审，一图看全 |
| 业务设计视角 | Feature / US / F / NF / I / UI | **排除 SRC**，供业务方确认 |
| 源码实现视角 | I / UI / SRC | I 环如何落到代码 |
| 设计时序 | I / UI / SRC | `variant sequence`，须含显式消息 |

**业务设计视角排除 SRC 是硬要求。** 业务方评审时看到源码元素就失去焦点，这是本环的意义所在。

### 视图命名的环归属

视图名建议带环前缀，便于导航与检索：

```text
feat-<编号>-<名称>  Feature 视图
us-<编号>          用户故事视图
frame-<名称>       F / NF 框架视图
impl-<名称>        I 环步骤视图
ui-<名称>          UI 环视图
src-<名称>         SRC 环视图
chain-<名称>       跨环链路视图
dep-<环境>         部署视图
```

视图名**全局唯一**，不同文件间也不能重名。**不要使用视图文件夹分组**——1.58.0 不支持 `views 'Label'`，按用途拆文件、用文件名表达环归属。

**主干与分支视图的命名规则**见 `11-trunk-first-design.md`：主干 `*-main`，分支 `*-branch-<条件>`。

### 视图与多文件的关系

视图类型和文件组织是两件事：

- **视图类型**由环性质决定（上表）
- **文件组织**按环拆分，详见 `02-multifile-and-fqn.md`
- **FQN 规则**：Feature 内嵌后，各环元素都成了嵌套元素，**跨作用域引用一律需FQN**（`feat_checkout.us_place`）。详见 `02-multifile-and-fqn.md`

---

## 六、按环路由到不同工具

能力边界必须诚实：

| 环 | 轨道 | 说明 |
| --- | --- | --- |
| Feature / US / F / NF | **一（LikeC4）** | 结构化关系，AI 可查询 |
| I 业务状态 | **一（LikeC4）** | 状态即元素 + 迁移即关系；代价是不能自环 |
| I 业务步骤 | **一（LikeC4 dynamic view）** | 步骤序列可表达 |
| UI 交互 | **一（dynamic view）** | 反馈流程用 dynamic view；分支拆多视图 |
| UI 信息 | **一（LikeC4）** | 界面为容器、字段为元素；代价是字段多时图较宽 |
| SRC 类设计 | **一（LikeC4）** | 嵌套 + 依赖关系；代价是继承无对应 |
| SRC 组件与依赖 | **一（LikeC4）** | 组件划分与依赖方向；父子含关系靠嵌套，不靠边 |
| SRC 时序与数据流 | **一（dynamic view）** | 分支拆多视图 |
| 构建部署 | **一（deployment view）** | 交付后产出 |

**全部图都用 LikeC4 表达，不降级。** LikeC4 1.58.0 不支持 `opt`/`loop`/`alt`/`try`，所以条件分支、循环、异常一律拆成多个视图；状态机用「状态即元素 + 迁移即关系」。完整写法与代价见 `09-likec4-substitutions.md`。

---

## 七、交付标准

设计链交付时说明：

1. **交付边界与 Feature 分类**（一句话 + F 类 / NF 类）
2. 覆盖的 US 清单，以及每条 US 的链路是否完整（缺哪一环）
3. 各环产出物位置（全部在 LikeC4 模型内）
4. **各环使用的视图类型**，以及是否与本 SOP 第五节的对应表一致
5. LikeC4 版本与 `likec4 validate` **及 `build`** 结果（两者都要，只 validate 会漏掉布局错误）
6. 哪些图使用了平替方案及其代价
7. SRC 的源码文件路径是否已核对真实代码
8. **嵌套元素的 FQN 使用情况**（架构设计 FQN，与源码路径引用是两回事）
9. NF 项中无法度量的条目
10. NF 类 Feature 的 F 环是否已显式声明「无需新增」
11. 构建部署图是否产出（应说明为何未产出或已产出）
12. 主干与分支的视图分工（见 `11-trunk-first-design.md`）

---

## 与其他 SOP 的关系

| 需求 | 去哪 |
| --- | --- |
| 画系统架构、上下文图、部署图 | `01-likec4-basics.md` |
| 判断图类型能否用 LikeC4 | `00-diagram-routing.md` |
| **多文件组织与架构设计 FQN** | `02-multifile-and-fqn.md` |
| 时序与动态视图 | `03-dynamic-views.md` |
| 环境探测与同步查看 | `04b-environment-and-sync.md` |
| 设计资产放项目层还是全局层 | `05-design-repo-layout.md` |
| 交接给实现阶段 | `06-architecture-handoff.md` |
| **起点判定、交付边界、Feature 分类、归属表达** | `12-design-origin.md` |
| 主干优先与视图分离 | `11-trunk-first-design.md` |
| **设计链各环边界、命名、追溯门禁** | **本 SOP** |

交接规格映射：**F 环对应依赖约束**（功能边界即依赖方向的依据），**NF 环对应验收锚点**（可度量值即验收依据），I 环对应组件边界，UI 环对应交互与信息，SRC 环对应部署要求。本 SOP 产出的设计链是交接规格的上游——交接规格是它的子集视图。

**FQN 规则归属**：见 `02-multifile-and-fqn.md`。注意区分两种引用——**架构设计 FQN**指 `.c4` 文件内元素的定位路径（`feat_checkout.us_place`），**源码路径引用**指磁盘上的源码文件（`src/routes/checkout-routes.js`，写在 `description` 里）。两者并列，无派生关系。
