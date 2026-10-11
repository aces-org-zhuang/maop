# SOP 07 - 设计链（F 链与 NF 链各自闭环）

## 目的

架构不是画一张系统图就结束。一个需求从提出到落地要穿过多个环节，每环都有**不同的读者、不同的语言、不同的验收标准**。混在一起会导致业务方看不懂、工程师没细节、评审无法定位问题。

本 SOP 定义各环的边界、命名、产出物与追溯要求。**起点（交付边界、Feature 分类、归属表达）见 `12-design-origin.md`。**

落盘骨架见 `templates/design-chain.md`，其中所有 `.c4` 代码块均经 likec4 1.58.0 实测通过（`✓ Valid` → `build` 输出 `✓ all views layouted`）。

```text
产品愿景        长期方向，坐标原点，不承载追溯门禁
 ↓
Feature        一次可交付增量（一个，不是两个）
 ↓  ⤷ 分叉决策：这次交付的性质是什么
Feature-001-F        Feature-001-NF
能力链               极端场景链
按业务能力切          按极端场景切
 ↓                    ↓
各自识别自己的 US      各自识别自己的 US
US-001 / US-002       US-003 / US-004
 ↓                    ↓
I → UI → SRC          I → UI → SRC
F 单元清单             NF 单元清单
（并列，非路径环节）    （并列，非路径环节）
 ↓                    ↓
 └──── 构建与部署 ────┘
              SRC 的运行投影。两条链的 SRC 同处一个制品与同一个
              运行时，收敛是必然的。交付落地之后才产出。
```

**三个关键动作不能省**：

| 动作 | 是什么 | 跳过会怎样 |
| --- | --- | --- |
| **分叉** | 判断这次交付是能力变更还是极端场景表现 | 直接画图，把两类关注点混在一条链里 |
| **各自识别 US** | 两条链的 US **分别识别**，内容完全不同 | 误以为 US 共享，把 NF 场景塞进 F 链的 US |
| **收敛** | 两条链的 SRC 进同一制品与运行时 | 交付与部署时才发现两条链要合并部署 |

**分叉是决策，不是标注。** 开发人员提出一项 Feature，第一个动作就是判断它的性质——这次要新增能力，还是要保证某个极端场景下的表现。两者都要，就分出两条链，各自闭环。

**收敛是必然的，不是可选的。** 两条链最终进同一个镜像、同一个运行时。**分出去的是关注点，合回来的是运行现实**——这也解释了为什么一次交付会产生两个 Feature 却仍算一次交付。

**两条链的下钻路径相同**：`US → I → UI → SRC`。但**它们的 US 是分别识别的**，不是共享的。

**F 与 NF 不在路径上。** 它们是与 US 并列的能力单元清单，标注该链交付了什么。

**Feature 才是 US 的超集**——它同时容纳 US、能力单元清单、以及 I / UI / SRC。

---

## 集合关系（四组，不可混同）

| 关系 | 性质 | 是否可判定 |
| --- | --- | --- |
| **Feature ⊃ US** | **包含**。Feature 是 US 的超集 | 是，嵌套即归属 |
| Feature ⊃ {能力单元清单} | 包含。同为Feature 的直接子元素 | 是 |
| 下钻路径 = US → I → UI → SRC | 环节序列。两条链相同 | 是，缺环即报缺失 |
| F 链 ∩ NF 链 = ∅ | **不相交**。链内不出现对方元素 | 是 |

**能力单元清单与 US 的关系不是链上一步**，而是超集内的两个并列子集：清单里每项要能对应到本链某条 US，但 US 下钻时不经过它。

**两条链的序号配对**（`Feature-001-F` 与 `Feature-001-NF`）表达「服务于同一次交付」，不构成包含关系。

**跨链边是硬错误。** 详见第三节。

---

## 一、路径环节与能力单元清单

**这一节区分两类东西，不可混同**：

| | 是什么 | 是否在路径上 |
| --- | --- | --- |
| **路径环节** | US / I / UI / SRC | **是**，逐环推进 |
| **能力单元清单** | F 单元清单或 NF 单元清单 | **否**，与 US 并列 |

**下钻路径只有一条**：US → I → UI → SRC。**US 下钻到 I，中途不经过 F 或 NF。**

### US 环节 · 用户故事

**产出物**：用户故事清单，每条含 `US-<编号> <标题>`、用户角色、期望、验收标准。

**回答的问题**：谁在什么场景下要完成什么，做成什么样算完成。

**不属于本环节**：技术方案、界面细节、类设计。

#### 验收标准的成分归属（两条链通用）

**一条验收标准可能含两种成分，各归不同的链。混写即跨链污染。**

| 成分 | 判定问句 | 归属 |
| --- | --- | --- |
| **业务结果判定** | 做完了吗？做对了吗？ | **F 链** |
| **质量判定** | 多快？多稳？多少？多久失效？ | **NF 链** |

判定动作是**逐句拆**：每句问「这句在问什么」。同一句里两种成分都有，就是污染。

```text
错F 链US   验收：提交后 2 秒内返回订单号
           →「2秒内」属 NF，「返回订单号」属 F，两者写进了同一条

对  F 链 US   验收：订单已创建，且订单号已送达客户端
对  NF 链 US  验收：响应超 2 秒时给出含原因与重试入口的提示
```

**硬门禁**：F 链 US 的验收标准出现**任何数值、时限、比例、可用性词**（秒 / ms / P95 / % / 可用 / 不超过 / 至少 / 最多）即为跨链污染。

**为什么必须硬门禁**：F 链与 NF 链**独立验收**。若 F 链 US 的验收含 NF 指标，F 链的验收结论就依赖 NF 链的度量结果——独立性被破坏，两条链的验收记录互相污染。这正是切面分离要避免的。

**指标内容不得就地删除**。发现污染时走成分拆分：业务结果部分留在本链；指标部分确认由哪条 NF 链承接，或交用户判定本次不做。静默删掉等于丢弃一个质量承诺。

完整拆分流程见 `08-design-decision-tree.md` 第 1.1 节。

### F 清单 · 功能单元（F 链的能力单元清单）

**产出物**：`F-<编号> <功能名>`，按业务能力切分的能力单元。

**回答的问题**：本次交付让系统能做什么。

**归属**：F 项只存在于 **F 链**（`Feature-<序号>-F`）内。NF 项不出现在 F 链的任何位置。

**与 US 的关系**：**并列，同为 Feature 的直接子元素**。每项 F 要能对应到本链某条 US，但 US 下钻时不经过它。

**不属于本清单**：具体实现、业务步骤、界面元素。

### NF 清单 · 极端场景下的系统表现（NF 链的能力单元清单）

**产出物**：`NF-<编号> <场景>下的<系统表现>`。

**回答的问题**：在某个极端场景下，系统会怎样表现、用户因此能得到什么。

**NF 是场景，不是角度。** 「性能」「可用性」「可审计性」是**观察角度**，不是交付物。角度必须落到具体场景才成为 NF 单元：

```text
错  NF-001 性能                    只是角度名，无角色、无场景、无受益者
错  NF-002 支付响应时延             只是角度名，答不出「谁因此受益」
对  NF-001 高峰 200 并发下单不卡      角色：客服｜场景：月末高峰｜验收：无需手工刷新
对  NF-002 支付网关不可用时可感知    角色：客服｜场景：第三方故障｜验收：提示明确可操作
```

**每个 NF 项必须能答出三项**，缺一即不合格：

| 项 | 判据 |
|---|---|
| **谁** | 有明确角色（客服 / 运维 / 接手人……），不是「系统」 |
| **什么场景** | 具体的极端条件，不是常态 |
| **因此得到什么** | 可感知的收益或可判定的结果 |

**答不出「谁在什么场景下因此受益」的名称，只是清单项，不是 NF 单元。**

**归属**：NF 项只存在于 **NF 链**（`Feature-<序号>-NF`）内。**NF 链与 F 链同维度、同本体**——它同样有 US、I、UI、SRC，不比 F 链少任何东西。

**与 US 的关系**：同样是**并列**，不是 US 的下游。

**必须可度量**。「系统要快」不合格；「高峰 200 并发下单 P95 ≤ 200ms」合格。无法度量的 NF 项应标记为 `待补充`，不凭想象编造。

**NF 不是约束，是一次完整交付。** 极端场景下的系统表现本身就是可交付能力，因此有完整的 US 与验收标准。详见 `12-design-origin.md` 第三节。

### I 环 · 业务设计

**产出物**：`I-<编号> <类型> <名称>`，三类：

| 编号段 | 内容 | 判据 |
| --- | --- | --- |
| 业务目标 | 该功能要达成的业务结果 | 描述收益，不描述手段 |
| 业务状态 | 业务对象的生命周期状态机 | 状态名 + 允许迁移 |
| 业务步骤 | 达成目标的操作序列 | 步骤 + 参与角色 |

**这一层完全不涉及源码**。判断标准：**换一个人、换一种技术栈来实现，这层设计依然成立**。一旦出现类名、函数名、表名，就越界了。



#### 业务步骤必须展开成元素，不能只写在 description 里（硬规则）

**把步骤写进 `description` 是错的。** `'主干步骤：接收消息 → 检索候选 → 置信度校验 → 生成答复'` 这种写法有三个问题：

1. 视图上只有一个 `I-xxx 业务步骤` 节点，读者看不出有几步、每步做什么
2. 步骤无法参与追溯——没法表达「哪条 US 由哪几步实现」
3. 无法画流程图——泳道时序需要真实的步骤元素才能连消息

**正确做法**：每个业务步骤是一个独立元素，按 `I-<三位编号>` 编号，并**嵌套在对应的 US 元素内部**。

```c4
错  i_step = implStep 'I-003 业务步骤' {
      description '主干步骤：接收消息 → 检索候选 → 置信度校验 → 生成答复'
    }
    // 一个节点，四个步骤全塞进文字，视图与流程图都做不出来

对  us_ask = userStory 'US-001 客户提问获得专业答复' {
      i_ask_normalize = implStep 'I-001 归一化提问' { }
      i_ask_retrieve  = implStep 'I-002 检索候选知识' { }
      i_ask_rank      = implStep 'I-003 候选排序与择优' { }
      i_ask_verify    = implStep 'I-004 置信度校验' { }
      i_ask_compose   = implStep 'I-005 生成答复' { }
      i_ask_deliver   = implStep 'I-006 下发答复' { }
    }
    // 六个元素，嵌在 US 容器内，归属一眼可见
```

**判据**：一个 `implStep` 的 `description` 里如果出现了 `→` 或顿号连接的多个动作，说明该拆了。

#### 归属靠嵌套容器表达，不靠跨层边（硬规则）

**「跨层」不是把两环元素画在同一张图里，而是用嵌套容器让归属可见**：

```text
US[I-001, I-002, I-003]      ← 步骤嵌在 US 容器内
I[UI-001]                    ← 界面嵌在业务步骤内
UI[SRC-001]                  ← 源码单元嵌在交互面内
F[US-001, US-002, US-003]     ← 单元嵌在 F 容器内
```

**注意最后一行是唯一的例外**：F/NF 单元与 US 是**同层并列**关系，不是祖先关系。F/NF 出现在 US 视图里是合法的（US 的直接上层就是 Feature，F/NF 就在那一层），但**不能再往上到 Feature 的兄弟环**。

**视图层**：祖先与目标元素**同时显式 `include`**，让 LikeC4 渲染成嵌套。**只 `include` 上层容器不会自动带出下层元素**（实测，见「最多跨一层」章节）。

```c4
对  view chain001F-i-step {
      include feat_answer_f.us_ask            // 祖先：US 容器
      include feat_answer_f.us_ask.i_normalize   // 目标：I 步骤
      include feat_answer_f.us_ask.i_retrieve
    }
    // 渲染成 US[I-001, I-002]，归属一眼可见

错  view chain001F-i-step {
      include feat_answer_f.us_ask            // ← 只有一个空 US 框，步骤全没画出来
      us_ask -> i_ask_normalize '实现'          // 用边表达归属
      include feat_answer_f.us_ask.i_normalize // 平铺，祖先丢失
    }
```

| 写法 | 效果 | 判定 |
| --- | --- | --- |
| **嵌套**（I 嵌在 US 内） | 归属由容器表达，一眼可见 | **正确** |
| 平铺 + 边 | 归属靠连线解释，图上多一堆箭头 | 冗余 |
| 平铺无关系 | 归属完全丢失 | 错误 |

**嵌套之后不要再连 `US → I` 的边**——包含关系已由嵌套表达。

**粒度按归属划分**：步骤只属于一条 US 就嵌在那条 US 下；被多条 US 共用的可嵌在 Feature 层并在 `description` 注明服务哪些 US。

#### 三类内容各自成图

| 内容 | 视图 | 表达方式 |
| --- | --- | --- |
| 业务目标 | `chain<链>-i-goal` | `element view`，只含目标 |
| 业务状态 | `chain<链>-i-state` | `element view`，状态即元素 + 迁移即关系 |
| 业务步骤 | `chain<链>-i-step` + `seq<链>-i-step-lanes` | 嵌套视图 + **泳道流程图** |

**业务步骤必须有泳道流程图**。步骤之间有责任边界——谁发起、谁编排、谁执行外部调用——平铺的 `element view` 表达不出这个分工。

```c4
views {
  dynamic view seq001F-i-step-lanes {
    variant sequence
    title 'I 环 · 业务步骤泳道流程 · Feature-001-F'
    include feat_answer_f.lane_client.actor_customer
    include feat_answer_f.lane_edge.api_chatCallback
    include feat_answer_f.us_ask.i_ask_normalize      // 嵌套后的真实步骤
    include feat_answer_f.us_ask.i_ask_retrieve
    include feat_answer_f.us_ask.i_ask_rank

    feat_answer_f.lane_client.actor_customer -> feat_answer_f.lane_edge.api_chatCallback '①提出问题'
    feat_answer_f.lane_edge.api_chatCallback -> feat_answer_f.us_ask.i_ask_normalize '②归一化'
    feat_answer_f.us_ask.i_ask_normalize -> feat_answer_f.us_ask.i_ask_retrieve '③检索'
  }
}
```

**`dynamic view` 引用嵌套元素必须用 FQN**（`feat.us_ask.i_ask_normalize`），实测有效。
**为什么单独设 I 层**：业务方评审时看的就是这层。如果业务目标、状态、步骤混在技术方案里，业务方无法评审——这是设计与需求脱节的根因。

### UI 层 · 界面层

**产出物**：`UI-<编号> <类型> <名称>`，两类，缺一不可：

| 类型 | 内容 | 必须回答 |
| --- | --- | --- |
| 交互设计 | 系统对用户操作的响应 | 每个操作触发什么、反馈什么、失败怎么回退、可否撤销 |
| 信息设计 | 系统需要展示的信息 | 字段、列表、可见区域、筛选区域、扩展功能（通知、导出、批量操作） |

**交互设计不等于界面布局**。按钮长什么样、颜色如何是视觉设计；交互设计关注的是**行为与反馈**。

**信息设计的常见遗漏**：空状态、加载状态、错误状态、无权限状态。这四种必须在设计里出现，否则实现时会临时发明，导致不一致。

### SRC 环 · 源码层

**产出物**：`SRC-<编号> <单元名>` + 真实文件路径，以及本环的数据载体与数据流。

**回答的问题**：代码怎么组织，数据怎么流。

**必须绑定真实路径**。`SRC-002 订单服务 → src/services/order-service.js`，而不是「订单服务模块」。没有路径约束的 SRC 层会与实际代码脱节。

**本环可包含**：类设计、组件设计、时序图、数据流图、依赖方向。

**边界**：I 环说「状态如何迁移」，SRC 环说「哪个类的哪个方法执行迁移」。前者不含源码，后者必须含。

#### 数据载体与数据流（SRC 环的独立维度）

SRC 环不只有代码结构。真实工程里业务数据要经过一串**载体**才能落地，这些载体是实现里最容易失控的部分——重复定义、边界模糊、转换散落各处。**SRC 环必须对它们有独立建模与命名。**

**按角色分类，不按语言术语分类。** 术语（PO / VO / POJO / BO / DTO）各语言定义不一，同一术语在不同项目含义可能相反。**归一为角色**：

| 角色 | 职责 | 生命周期 | 常见术语（供参考，不强制） |
| --- | --- | --- | --- |
| **入参载体** | 承接外部请求进入系统 | 单次请求 | DTO / Request / Command |
| **业务载体** | 承载业务规则与状态流转 | 单次用例 | BO / Domain / Model |
| **持久化载体** | 与存储结构对应 | 与记录同寿 | PO / PO / Entity / DO |
| **出参载体** | 面向展示或外部返回 | 单次响应 | VO / View / Response |
| **数据访问单元** | 读写存储的边界 | 常驻 | DAO / Repository / Mapper |
| **转换单元** | 载体之间的映射 | 常驻 | Converter / Mapper / Assembler |

**命名规范（强制）**：

| 角色 | 编号前缀 | 示例 |
| --- | --- | --- |
| 入参载体 | `IN-<三位编号>` | `IN-001 订单提交入参` |
| 业务载体 | `BIZ-<三位编号>` | `BIZ-001 订单业务对象` |
| 持久化载体 | `POD-<三位编号>` | `POD-001 订单持久化实体` |
| 出参载体 | `OUT-<三位编号>` | `OUT-001 订单出参视图` |
| 数据访问单元 | `DAO-<三位编号>` | `DAO-001 订单数据访问` |
| 转换单元 | `CVT-<三位编号>` | `CVT-001 订单载体转换器` |

```c4
model {
  in_orderReq = dto 'IN-001 订单提交入参' {
    description 'src/dto/order-request.dto.ts — 承接下单请求，边界校验后转 BIZ。'
  }
  biz_order = entity 'BIZ-001 订单业务对象' {
    description 'src/domain/order.ts — 承载下单规则与状态流转，不含持久化注解。'
  }
  pod_order = entity 'POD-001 订单持久化实体' {
    description 'src/repository/order-record.ts — 与订单表结构一一对应。'
  }
  out_orderView = vo 'OUT-001 订单出参视图' {
    description 'src/dto/order-view.dto.ts — 面向界面展示，已脱敏。'
  }
  dao_order = dataAccess 'DAO-001 订单数据访问' {
    description 'src/repository/order-repository.ts — 订单表读写。'
  }
  cvt_order = converter 'CVT-001 订单载体转换器' {
    description 'src/convert/order-converter.ts — 四个载体间的映射集中于此。'
  }
}
```

**为什么必须给转换单元独立编号**：载体之间的转换如果散落在各处的 `set` / `copy` 方法里，就没人能回答「字段变更会影响哪些转换」。**转换集中在一处，是数据契约可维护的前提。**

**四类边在本环的分工**：

| 边 | 表达 | 本环用法 |
| --- | --- | --- |
| `.trace` | 为什么连（设计追溯） | US ↔ 载体、转换单元↔ 载体 |
| `.depends` | 运行时怎么走 | SRC 单元之间的调用 |
| `.flow` | 数据往哪走 | UI →载体 → DAO → UI 的完整路径 |
| `.convert` | 在哪一步换了载体 | 相邻载体之间的转换点 |

**`.flow` 与 `.convert` 不可合并**：没有它们，「这个字段从哪来、改它要动几处」在图上无法回答——而这正是实现阶段最频繁的改动。

**三条硬门禁**（都可校验）：

1. **每个持久化载体必须有对应的数据访问单元**，入边为零说明这个载体没人读也没人写，是死代码。
2. **每个转换单元必须写明覆盖哪几个载体之间的映射**（写在 `description`）。转换单元若不写覆盖范围，等于没人知道字段变更要改哪里。
3. **业务载体不得直接连数据访问单元**。业务载体 → 数据访问单元说明持久化细节泄漏进了业务逻辑，中间必须经过持久化载体或转换单元。

> 实测记录（likec4 1.58.0）：以上写法 `✓ Valid`，含数据流全景与载体全景视图，`build` 输出 `✓ all views layouted`。

#### 对外接口与运行时（SRC 环的另两个维度）

SRC 环还承载两个常被遗漏的维度：**系统对外暴露什么接口**，以及**这些接口在什么进程与线程里跑**。

##### 对外接口（API）

接口是 SRC 环的独立元素，**不是 SRC 单元的别名**。`SRC-001 结算路由` 是代码单元，`POST /orders` 是它暴露的契约——一个单元可暴露多个接口，一个接口也可能由多个单元协作实现。

**命名规范**：

| 类型 | 格式 | 示例 |
| --- | --- | --- |
| 接口 | `API-<三位编号> <METHOD> <路径> <名称>` | `API-001 POST /orders 提交订单` |

**METHOD 保留原文大写**（`GET` / `POST` / `PUT` / `DELETE` / `PATCH`），路径原样保留。

```c4
model {
  feat_f = feature 'Feature-001-F 结算下单' {

    // 泳道：按调用方向分组，不是按步骤
    lane_client = feature '客户端' {
      ui_chat = uiSurface 'UI-001 会话界面' { }
    }
    lane_edge = feature '服务端接入' {
      api_placeOrder = apiEndpoint 'API-001 POST /orders 提交订单' {
        description 'src/routes/checkout-routes.js:42'
      }
      api_getOrder = apiEndpoint 'API-002 GET /orders/{id} 查订单' {
        description 'src/routes/checkout-routes.js:58'
      }
    }
    lane_core = feature '领域层' {
      svc_order = srcUnit 'SRC-002 订单服务' { }
    }
    lane_ext = feature '外部依赖' {
      ext_pay = system '支付网关' { }
    }
  }
}
```

**泳道按调用方向划分**，不按操作步骤。这是 `09-likec4-substitutions.md` 里泳道平替方案的延续。

**接口必须绑定真实路由位置**（路径 + 行号写在 `description`）。写不出位置的接口说明尚未实现，标 `待补充`。

##### 进程与线程

进程与线程**属于运行投影，用 `deployment` 表达，不用逻辑模型的 element**。

```c4
deployment {
  environment prod '生产环境' {
    zone appZone '应用区' {
      machine appHost 'app-1 · 4C8G' {
        apiInst = instanceOf feat_f.lane_edge.api_placeOrder
        processNode apiProc 'API 进程 · node src/server.js' {
          threadNode httpPool 'HTTP 线程池 · 16' { }
          threadNode workPool '工作线程池 · 8' { }
        }
        processNode workerProc 'Worker 进程 · node src/worker.js' {
          threadNode timerThread '定时器线程' { }
          threadNode queueThread '消费线程 · 4' { }
        }
      }
    }
  }
}
```

**`processNode` 与 `threadNode` 需在 specification 里声明**，`deployment` 里不会自动生成。

**进程与线程的层级靠嵌套表达，不连边**——包含关系已由嵌套给出，连边报 `Invalid parent-child relationship`。

**关键边界（实测）**：`instanceOf` 节点**内部不能再嵌节点**。所以「接口挂到哪台机器的哪个进程」与「进程里有哪些线程」**只能并列表达，不能嵌套**：

```c4
machine appHost 'app-1' {
  apiInst = instanceOf feat_f.lane_edge.api_placeOrder   // 逻辑挂载：哪个进程承载这个接口
  processNode apiProc 'API 进程' {
    threadNode httpPool 'HTTP 线程池' { }               // 运行时：进程内的线程
  }
}
```

**为什么这样也是可接受的**：进程归属与线程构成是两个正交问题——同一个接口可以在多个进程上部署（多副本），同一个进程的线程池也不因接口而变。

> 实测记录（likec4 1.58.0）：`processNode` 嵌 `threadNode` `✓ Valid`；`instanceOf` 节点内嵌节点报 `Could not resolve reference to Referenceable named 'httpPool'`；两者同级共存 `✓ Valid`；`deployment view` + `include prod.**` `build` 通过。

### 构建与部署（SRC 的运行投影）

**方向是 SRC → 部署，不是上下游环节。** 部署视图的全部内容来自 `instanceOf` 引用 SRC 元素，它是对SRC 的展开，不是 SRC 的后继。

只有当设计落地为代码后才产出：CI 流程、镜像、环境拓扑、发布策略、回滚方案。**在设计阶段不产出构建部署图**——它依赖最终实现，提前画必然返工。

例外：部署形态会影响架构决策（如是否需要跨网络隔离），此时只记录**约束**，不画完整部署图。

---

## 二、命名规范（强制）

| 环 | 格式 | 示例 |
| --- | --- | --- |
| Feature | `Feature-<三位编号>-F|-NF <标题>` | `Feature-001-F 结算下单` |
| US | `US-<三位编号> <标题>` | `US-001 提交订单` |
| F | `F-<三位编号> <功能名>` | `F-001 订单功能` |
| NF | `NF-<三位编号> <场景>下的<系统表现>` | `NF-001 高峰 200 并发下单不卡` |
| I | `I-<三位编号> <类型> <名称>` | `I-002 业务状态 订单状态机` |
| UI | `UI-<三位编号> <类型> <名称>` | `UI-002 信息设计 订单列表信息` |
| SRC | `SRC-<三位编号> <单元名>` | `SRC-002 订单服务` |
| 数据载体 · 入参 | `IN-<三位编号> <名称>` | `IN-001 订单提交入参` |
| 数据载体 · 业务 | `BIZ-<三位编号> <名称>` | `BIZ-001 订单业务对象` |
| 数据载体 · 持久化 | `POD-<三位编号> <名称>` | `POD-001 订单持久化实体` |
| 数据载体 · 出参 | `OUT-<三位编号> <名称>` | `OUT-001 订单出参视图` |
| 数据访问单元 | `DAO-<三位编号> <名称>` | `DAO-001 订单数据访问` |
| 转换单元 | `CVT-<三位编号> <名称>` | `CVT-001 订单载体转换器` |
| 对外接口 | `API-<三位编号> <METHOD> <路径> <名称>` | `API-001 POST /orders 提交订单` |

编号**全局唯一且不复用**。删除元素后编号不回收，避免历史引用失效。

**数据载体编号与 SRC 编号是同一个编号空间**。`SRC-002 订单服务` 与 `POD-002 订单持久化实体` 可以同时存在，二者是不同角色的元素，不是同一条链上的上下游。

**不要用 PO / VO / BO / DTO 作为编号前缀**。这些术语各语言定义不一、同一术语含义可能相反，且 `PO` 与 `POD` 视觉上几乎无法区分。用角色前缀（`IN` / `BIZ` / `POD` / `OUT` / `DAO` / `CVT`）保持跨项目一致。术语可写在显示名里：`POD-001 订单持久化实体 PO`。

**语言**：编号与显示名分隔。编号前缀是英文（跨工具稳定），显示名用中文。依据 `01-likec4-basics.md` 的语言契约。

### 视图命名规范（强制，便于识别与检索）

**视图名必须自带类型信息**，看一眼名字就知道它属于哪一类、聚合了什么。

| 前缀 | 类别 | 格式 | 示例 |
| --- | --- | --- | --- |
| `pano-` | **同类聚合全景** | `pano-<环>` | `pano-f`、`pano-nf`、`pano-us`、`pano-i`、`pano-ui`、`pano-src`、`pano-i-state`、`pano-carrier`、`pano-api` |
| `chain` | **分环视图**（单链单环） | `chain<链>-<环>` | `chain001F-us`、`chain001NF-i-goal` |
| `seq` | 时序 | `seq<链>-<场景>` | `seq001F-answer`、`seq001F-branch-low-confidence` |
| `dfd` | 数据流 | `dfd<链>-<主题>` | `dfd001F-answer` |
| `carrier` | 数据载体 | `carrier<链>` | `carrier001F` |
| `erm` | 数据模型 | `erm<链>-<主题>` | `erm001F-ticket` |
| `srcdir` | SRC 目录 | `srcdir<链>-<主题>` | `srcdir001F-answer` |
| `api` | 接口清单 | `api<链>-<主题>` | `api001F` |
| `proc` | 运行时 | `proc-<环境>` | `proc-prod` |

**两类全景前缀不要混用**：

- `pano-<环>` = **同类聚合**，**跨全部 Feature**，只含一种元素（`pano-f` 收所有 `Feature-NNN-F` 的 F 单元）
- `dfd` / `carrier` / `erm` / `api` / `srcdir` = **单链的 SRC 各维度**，属于某条链的某个维度

`pano-carrier` 与 `carrier001F` 的区别：前者跨全部 Feature 聚合全部载体，后者只看 F 链的载体。

**视图名全局唯一**，不同文件间也不得重名（实测：重名报 `Duplicate view`）。

**视图名可用连字符**（实测：`pano-f`、`seq001F-answer` 均 `✓ Valid`）。

---

## 三、追溯要求（硬门禁）

### 下钻路径只有一条，能力单元清单不是路径环节

```text
下钻路径        US → I → UI → SRC          两条链相同
能力单元清单     F 链 = {F 单元}，NF 链 = {NF 单元}
切面标注        tag: capability / tag: quality
```

**US 下钻到 I，中途不经过 F 或 NF。** 能力单元清单与 US 是 `Feature ⊃ {US, 清单}` 这一个超集里的两个并列子集。

**任一环缺失即为不完整设计**，必须在交付时明确报告缺失哪一环，不能静默跳过。

**为什么必须区分**：把清单画成 `US → F → I` 会误导成「必须经过 F 才能到 I」，且暗示 F 是 US 的下游。实际 US 与 F 是并列的，**Feature 才是 US 的超集**。

### 跨链边是禁止的（硬约束）

```c4
nf_latency .trace feat_f.i_step '约束步骤耗时'   // 错：把 NF 挂进 F 链的 I 环
nf_auditability .trace feat_f.i_state '约束状态迁移' // 错：同上
nf_latency .trace feat_f.us_place '约束验收'     // 错：NF 不指向 F 链的 US
```

**为什么禁止**：跨链边等于在推 F 的过程中「顺手检视一下 NF」。切面一旦进入主链，就会在每次推进时被反复提及，最终把 F 的视图撑爆。

**正确的做法**：NF 链拥有自己的 US 与 I 环。性能切面交付的是「超时能被感知并可操作」这项能力，它有自己的业务逻辑，不需要借用 F 链的。

### 门禁一：路径完整性（两条链各查一遍）

**F 链**（`Feature-001-F`）：

```c4
us_place .trace i_step '落为业务步骤'      // US → I：路径环节
i_step .trace ui_interaction '反馈交互'
ui_interaction .trace src_checkout '触发源码'
```

**NF 链**（`Feature-001-NF`）：

```c4
us_peak .trace i_perf '落为判定逻辑'      // US → I：路径环节
i_perf .trace ui_warning '反馈提示'
ui_warning .trace src_probe '触发埋点'
```

**两条链的门禁形式完全相同**——因为路径相同。任一环缺失即报不完整。

### 门禁二：能力单元清单的对应关系（非路径环节）

能力单元不在路径上，但**清单每一项都要能对应到本链的某条 US**：

**F 链**：

```c4
us_place .trace f_order '要求'      // 清单项 ↔ US：清单的来源
us_pay .trace f_payment '要求'
```

**NF 链**：

```c4
us_peak .trace nf_latency '要求'      // 清单项 ↔ US：清单的来源
us_audit .trace nf_auditability '要求'
```

**这条边的语义是「清单项由哪条 US 要求」，不是「路径上的一步」。** `us_place .trace f_order` 不意味着 US 要先经过 F 才能到 I——它只是说「订单功能这项能力是 US-001 要求的」。

**入边为零即凭空出现的单元**：清单里有某项但没有任何 US 要求它，说明它不属于本次交付范围，必须报告。

> **常见错误**：把「NF-001 落在 US-003 上」只写进 NF 的 `description`。这样对应关系在模型里不存在，门禁形同虚设，`search-element` 也查不出哪个 NF 悬空。

> 实测记录（likec4 1.58.0）：两类链写法一致，均 `✓ Valid` 且 `build` 输出 `✓ all views layouted`。

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

### 每条链的必备视图

两条链**各自必备**下列视图，且**不共用**：

| 视图 | 覆盖范围 | 用途 |
| --- | --- | --- |
| 链路总览 | 本链全部元素 | 架构评审 |
| 业务设计视角 | 本链 US 到 UI，**不含 SRC** | 业务方确认 |
| 源码实现视角 | 本链 I/UI/SRC | I 环如何落到代码 |
| 能力单元视图 | 本链 US + F（或 NF） | 产品与架构 |
| 设计时序 | 本链 I/UI/SRC，`variant sequence` | 工程师 |

### 全量设计时必备：同类聚合全景

**每一环都要有自己的全景视图**，不只 NF。全景是全量设计的产物，增量设计时不出。

**硬规则：全景必须同类聚合，一张全景只放同一种元素。**

| 全景视图 | 只包含 | 回答什么 |
| --- | --- | --- |
| **F 全景** | 所有 `Feature-NNN-F` 的 **F 单元** | 系统对外提供哪些能力 |
| **NF 全景** | 所有 `Feature-NNN-NF` 的 **NF 单元** | 系统承诺哪些场景下的表现 |
| **US 全景** | 所有 Feature 的 **US** | 谁要什么 |
| **I 全景** | 所有 Feature 的 **I 环元素** | 业务怎么流转 |
| **I 状态全景** | 全部链的**业务状态** | 状态有哪些、怎么迁移 |
| **UI 全景** | 所有 Feature 的 **UI 元素** | 用户能看到什么 |
| **SRC 全景** | 所有 Feature 的 **SRC 单元** | 代码怎么组织 |
| **数据载体全景** | 所有 Feature 的**载体**（SRC 维度，非某一环） | 有哪些载体、各自什么角色 |
| **API 全景** | 所有 Feature 的**接口**（SRC 维度，非某一环） | 对外暴露哪些契约 |

**违规示例**（都是实际犯过的错）：

```c4
错  F 全景里 include 了 us_xxx 和 i_step
     「F 全景」这个名字就失去了意义——读者无法判断这张图是干什么的

错  I 全景里 include 了 src_xxx
     SRC 是独立环，不该出现在 I 环全景里
```

**对应的正确做法**：单元与 US 的对应关系放在**各链的能力清单视图**（`chain<链>-f`）里，不放在全景里。

**全景是独立视图，不是链视图的放大版。** 链视图按环聚焦（见下节），全景按同类横向聚合。

#### 聚合单位是 Feature，不是链（硬规则）

**全景的聚合轴是 Feature，不是链。** 这是最容易搞错的一层：

```text
pano-f    收  Feature-001-F 的 F 单元 + Feature-002-F 的 F 单元 + …
pano-nf   收  Feature-001-NF 的 NF 单元 + Feature-002-NF 的 NF 单元 + …
pano-us   收  所有 Feature 的所有 US
```

**链（`Feature-NNN-F` / `Feature-NNN-NF`）是 Feature 内部的实现单位，不是全景的聚合轴。** 一个 Feature 分叉出的两条链，在 `pano-us` 里都算「一个 Feature 的 US」。

**违规示例**（实际犯过的错）：

```c4
错  index 只 include 了 feat_001_f, feat_001_nf
     这是「Feature-001 的总览」，不是导航入口。它会让读者以为项目只有一个 Feature

错  pano-f 只收了 Feature-001-F 的单元，还叫它「全部链的能力单元」
     「全部链」这个说法暗示了跨链聚合，但实际只有一条链，读者无法判断是不是漏了
```

**Feature 数量不足时必须显式声明退化**：

只有一个 Feature 时，`pano-f` 必然等于该链的 F 单元全量。**此时必须在 `description` 里写明**，不能假装这是全景：

```text
pano-f  当前仅 Feature-001 一个 Feature，故本视图等于 Feature-001-F
        的能力单元全量。新增 Feature-002-F 后本视图将自动聚合。
```

**不写这句的代价**：读者会把单链视图误当全景，看不出横向对比的基准是什么，也看不出项目是否只交付了一次。

**全景是导航入口的前提**：它回答「项目一共交付了哪些 Feature，每条链各自交付了什么」。

**为什么每环都要全景**：单链视图只覆盖一次交付的局部。跨 Feature 的横向认知只能靠全景获得——比如「这个状态被哪几条链读写」「这个能力被哪些场景绑定」「两个 Feature 是否做了重复的事」。

**为什么不在每张链视图里检视其他环**：那会让每张图都重复承载其他维度，视图被撑爆。**聚合发生在全景层，不发生在链视图层。**

### 链视图必须按环聚焦（硬规则）

**一张链视图只承载一个环的内容，禁止 `include *`。**

`include *` 会把六个环加上数据载体、泳道全部塞进一张图——这是"视图跨层"的真正来源，不是全景命名的问题。

| 视图 | 只包含 |
| --- | --- |
| `chain<链>-us` | 本链的 US |
| `chain<链>-f` / `chain<链>-nf` | 本链的能力/场景清单 + 对应 US（**唯一允许同图出现 US 的例外**） |
| `chain<链>-i-goal` | **只**有业务目标 |
| `chain<链>-i-state` | **只**有业务状态与迁移 |
| `chain<链>-i-step` | **只**有业务步骤 |
| `chain<链>-ui` | 本链的交互面与信息设计 |

**I 环必须按内容子类拆图**：业务目标、状态流转、业务步骤是三种不同的内容，混在一张图里读者要自己分辨。状态流转用「状态即元素 + 迁移即关系」，业务步骤用流程图——**步骤有责任边界时要带泳道**。

```c4
错  view chain001F-chain of feat_f { include * }        六环全塞

对  view chain001F-i-goal of feat_f { include feat_f.i_goal }
    view chain001F-i-state { include st_a, st_b, st_c }  状态即元素
    view chain001F-i-step-lanes { ... 泳道流程图 ... }     按责任分区
```

**能力清单视图可以同时出现 US**——它的目的就是展示单元与 US 的对应关系。这是有意的例外，要在 `description` 里写明，避免被误读成 US 视图。

### 最多跨一层（硬规则，实测校正）

**一张视图最多出现「本环 + 直接上一层」。出现第三层及以上就是错的。**

层级链是**固定**的，不因某张图方便而改变：

```text
产品愿景  →  Feature-001-F  →  US  →  I  →  UI  →  SRC  →  构建部署
              └ F/NF 单元 ┘        └ 业务步骤 ┘
```

**每一层的直接上层是固定的**：

| 本环 | 直接上层（唯一合法的锚） | 上层的上层（越层，禁止） |
| --- | --- | --- |
| US | Feature（含 F/NF 单元） | — |
| I | US | Feature |
| UI | I | US、Feature |
| SRC | UI | I、US、Feature |
| 构建部署 | SRC | UI 及以上 |

**推论一：SRC 视图里不允许出现 F / NF 单元，也不允许以 Feature 为容器。** SRC 的上层是 UI，UI 的上层是 I，Feature 已是第三层祖先。这条最常被违反——因为 SRC 视图的 `include` 顺手就把 Feature 元素带进去了。

**推论二：UI 视图里不允许出现 F / NF 单元。** UI 的上层是 I，不是 Feature。

**推论三：I 视图里不允许出现 F / NF 单元。** I 的直接上层是 US。F/NF 是 Feature 层的清单，与 US 并列，不在 I 的祖先路径上。

**跨层 ≠ 平铺**。「跨一层」的正确表达是**嵌套**：本环元素嵌在上层容器内部，视图渲染成 `上层容器[本环元素]`。

#### 关键实测：`include` 容器不会带出子元素

这一条纠正了一个常见误解。**嵌套写在模型里，不等于视图里会自动画出来。**

```c4
model {
  featA = feature '甲' {
    us1 = userStory 'US-001' {
      i1 = implStep 'I-001 步骤一' {
        ui1 = uiSurface 'UI-001 交互面' {
          src1 = srcUnit 'SRC-001 源码单元' { }
        }
      }
    }
  }
}
```

| 视图写法 | 实际渲染 | 判定 |
| --- | --- | --- |
| `include featA.us1` | 只有 `us1` 一个空框，**I 步骤一个都没出现** | **错误**——看起来像嵌套了，其实没画 |
| `include featA.us1.i1.ui1.src1` | 只有 `src1` 平铺，**US/I/UI 三个祖先全丢** | **错误**——归属完全丢失 |
| `include featA.us1.i1.ui1` + `include featA.us1.i1.ui1.src1` | `ui1[src1]` | **正确** |
| `include featA.us1` + `include featA.us1.i1` + `include featA.us1.i1.ui1` | `us1[i1[ui1]]` | 正确（但**已跨三层**，仅在导航类视图可用） |

**规则：想显示某层，就必须把祖先链与目标元素全部显式列出。** 少列一层 → 归属丢失；多列两层 → 越层。

#### 视图写法对照表

| 视图 | 允许出现 | 正确写法 |
| --- | --- | --- |
| `chain<链>-us` | Feature 容器 + US | `include feat_f` + `include feat_f.us_x` |
| `chain<链>-f` | Feature 容器 + F/NF 单元 + US（唯一例外） | 同上，按需列 |
| `chain<链>-i-goal` | US 容器 + 业务目标 | `include feat_f.us_x` + `include feat_f.us_x.i_goal` |
| `chain<链>-i-step` | US 容器 + I 步骤 | `include feat_f.us_x` + `include feat_f.us_x.i_normalize` |
| `chain<链>-ui` | I 容器 + UI 面 | `include feat_f.us_x.i_normalize` + `include feat_f.us_x.i_normalize.ui_y` |
| `srcdir<链>` | UI 容器 + SRC 单元 | `include feat_f...ui_y` + `include feat_f...ui_y.src_z` |
| `carrier<链>` | SRC 维度同层平铺 | 只 `include` 载体元素，**不 include Feature** |
| `api<链>` | 泳道容器 + API | 只 `include` 泳道容器及其 API |

**载体类视图（`carrier` / `erm` / `pano-carrier`）是例外**：数据载体是 SRC 环内部的横向维度，不属于 `UI → SRC` 这条纵向路径，因此可以平铺，不强制带 UI 容器。

#### 视图内容校验（实测校正）

**`validate` 与 `build` 都只检查语法和布局，不检查「该显示的元素有没有显示」。** 元素漏画、归属丢失、越层三类错误全部静默通过。必须导出 JSON 核对实际渲染结果：

```bash
likec4 export json -o out.json
node -e "
const d=require('./out.json');
for(const id of Object.keys(d.views)){
  const v=d.views[id];
  if(v._type!=='element') continue;
  const ns=v.nodes||[];
  const flat=ns.filter(n=>n.level===0).length;
  // 平铺率：全平铺说明没有嵌套容器，归属靠什么表达？
  console.log(id+'  节点='+ns.length+'  L0='+flat+'  L1='+ns.filter(n=>n.level>1).length);
}"
```

判据：

| 现象 | 含义 | 判定 |
| --- | --- | --- |
| `L1 = 0` 且视图宣称有嵌套归属 | 子元素**根本没画出来** | **错误**——最常见缺陷 |
| `L1 > 0` 且容器是直接上层 | 归属正确 | 正确 |
| `L1 > 0` 且容器是祖父层 | 越层 | **错误** |
| 有 `level ≥ 2` 的节点 | 跨了两层以上 | **错误** |

> **实测坑（务必知道）**：`include` 容器**不会**自动带出子元素。`include feat.us_x` 渲染出来就是一个**空 US 框**，里面的 I 步骤一个都不显示。这会让「I 环业务步骤视图」看起来配好了，实际是空的。必须**祖先与目标元素同时显式 `include`**。

> **注意**：不要用「节点的祖先链是否在视图里」来判定归属错位——LikeC4 渲染嵌套时节点 id 保持完整 FQN，容易误判。判定归属是否正确应看**容器的 `children` 数组里每个元素的 id 是否以容器 id 为前缀**。

#### 与「全景同类聚合」的关系

两条规则不冲突，约束的是不同维度：

- **同类聚合**管「这张图放什么种类的元素」——只放一种环的元素。
- **最多跨一层**管「这些元素的容器嵌套多深」——容器最多到直接上一层。

一条全景视图的元素全部平铺在 L0（`level: 0`）就是同时满足两条。**一旦某元素出现 `level > 0`，就必须检查它的祖先是不是合法锚。**

#### LikeC4 会自动补齐断层（实测，最容易踩）

**祖先与目标之间若有未 `include` 的中间层，LikeC4 会把它自动补上并展开，导致越层。**

```text
模型嵌套：US → I → UI → SRC（四层）

include ui                  → ui                    0 层  ✓
include ui + ui.src         → ui[src]               1 层  ✓ 只取下两层
include us + i + ui + src   → us[i[ui[src]]]        3 层  ✗ 显式补齐了全链
include src                 → src                   0 层  ✓ 但归属全丢
```

**规则：只 `include` 目标层的直接上层与目标元素本身，不要往上补。** 想显示两层就只列两层，多列一层就多渲染一层。

#### 元素分属不同父容器时必须拆视图（实测）

一条视图里 include 的元素如果**分属不同的父容器**（例如 NF 链的 `ui_status` 挂在 `us_kbEmpty` 下、`ui_notice` 挂在 `us_llmDown` 下），LikeC4 会把每个父容器都提为根并展开其中间层，产生越层。

**修法：按父容器拆成多张视图**，视图名加后缀区分（`srcdir001NF` / `srcdir001NFnotice`）。这与「一条分支一张图」是同一条原则的延伸。

> 实测记录（likec4 1.58.0）：以上全部写法 `✓ Valid` 且 `✓ built`，包括越层写法——**越层不是语法错误，工具不会拦，只能靠规则与自检**。

### SRC 环额外必备：六张视图

SRC 环比其他环多四层要求：**它对应真实磁盘资产，业务数据要流过它，系统对外暴露接口，且接口跑在具体进程与线程里。**

| 视图 | 范围 | 含源码路径 | 回答 | 视图类型 |
| --- | --- | --- | --- | --- |
| **SRC 目录视图** | 本链 | **是** | 源码文件怎么组织，每个单元对应哪个文件 | `view of <feature>` |
| **SRC DFD 全景** | 本链 | 否 | 数据从入口到落库经过哪些载体、在哪里转换 | `dynamic view variant sequence` |
| **数据载体全景** | 本链 | 否 | 有哪些载体、各自什么角色 | `element view` |
| **数据模型全景** | 本链 | 否 | 持久化实体与关系 | `element view`（`store` 承载实体） |
| **API 清单** | 本链 | 否（带路由位置） | 对外暴露哪些接口 | `element view` |
| **API 泳道时序** | 本链 | 否 | 一次调用穿过哪些泳道 | `dynamic view variant sequence` |
| **进程与线程视图** | 环境级 | 否 | 接口跑在哪个进程的哪个线程 | `deployment view` |
| SRC 全景 | **跨全部链** | 否 | 源码单元全貌 | `element view` |

SRC 单元是**唯一带真实文件路径**的环（路径写在 `description` 里）。没有目录视图，实现方拿到的是一堆抽象单元，看不到实际的文件布局。

目录视图的读法：**按嵌套层级展开，每个单元标出它对应的源码路径**。子单元是父单元所在文件内的拆分，父子不连边（包含关系已由嵌套表达）。

**DFD 全景是数据维度的唯一视图**。没有它，「这个字段从哪来」「改这个字段要动几个地方」无法回答——而这正是实现阶段最频繁的改动。

**API 清单回答「有什么」，API 泳道时序回答「怎么走」**。只有清单时，接口之间的调用关系要靠读者自己拼。

**进程与线程视图是环境级的，不属于单条链**——同一接口在生产与预发的进程结构可能不同。它的命名不带链序号。

**API 泳道时序的泳道按调用方向划分**（客户端 / 服务端接入 / 领域层 / 外部依赖），不按操作步骤。详见 `09-likec4-substitutions.md` 的泳道平替。

> 实测记录（likec4 1.58.0）：`dynamic view` **不支持 `of <容器>` 作用域语法**（报 `Expecting token of type '}' but found 'of'`），`view of <feature>` 支持。DFD 全景与 API 泳道时序因此不能写 `of`，归属靠 `description` 与元素嵌套表达。

> `views` 块内**不支持 `//` 行注释**，会报 `Expecting token of type 'EOF'`。注释写在块外。

> `dynamic view` 与 `element view` 不能混在同一 `views` 块，拆成两个文件。

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
| SRC | `element view` + `variant sequence` + `dynamic view`（DFD） | element + dynamic + deployment | 工程师 | 嵌套引用需 FQN；数据载体、数据流、接口、进程线程都要建模 |
| 数据载体 | `element view`（载体全景） | element | 工程师 | 按角色编号，不绑语言术语 |
| 对外接口 | `element view`（API 清单）+ `dynamic view`（泳道时序） | element + dynamic | 工程师 + 前端 | 泳道按调用方向划分 |
| 构建部署 | `deployment view` | deployment | 运维 | 交付后才产出 |

### 为什么这样分配

- **Feature / US / F / NF 是静态结构**，用 `element view` 表达「谁包含谁、谁要求谁」。
- **I 环的核心是步骤与状态**。步骤序列用 `dynamic view`（diagram 变体）；**状态机用「状态即元素 + 迁移即关系」表达**，见 `09-likec4-substitutions.md`。
- **UI 环是静态面 + 动态反馈的组合**：交互面用 element view 表达「哪个界面触发哪个行为」，信息设计（字段、列表、筛选区、通知）用表格更清晰，硬塞进图会失焦。
- **SRC 环是唯一需要多种视图的环**：组件结构用 element view，调用时序用 `variant sequence`，数据流向用 element view 的依赖关系表达。
- **构建部署用 `deployment view`**，且只在交付落地后产出。

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

1. **交付边界与切分维度**（一句话 + F 链 / NF 链 + 配对链编号）
2. **两条链各自完整**（F 链与 NF 链的链路完整性分别核对）
3. **无跨链边**，两条链各占一个 model 文件
4. 覆盖的 US 清单，以及每条 US 的链路是否完整（缺哪一环）
5. 各环产出物位置（全部在 LikeC4 模型内）
6. **各环使用的视图类型**，以及是否与本 SOP 第五节的对应表一致
7. LikeC4 版本与 `likec4 validate` **及 `build`** 结果（两者都要，只 validate 会漏掉布局错误）
8. 哪些图使用了平替方案及其代价
9. SRC 的源码文件路径是否已核对真实代码
10. **嵌套元素的 FQN 使用情况**（架构设计 FQN，与源码路径引用是两回事）
11. NF 链中无法度量的条目
12. **全量设计时是否出了 NF 全景视图**（而非在每个 F 视图里检视 NF）
13. 构建部署图是否产出（应说明为何未产出或已产出）
14. 主干与分支的视图分工（见 `11-trunk-first-design.md`）
15. **数据载体清单**：按角色（`IN` / `BIZ` / `POD` / `OUT` / `DAO` / `CVT`）列出，附真实文件路径
16. **DFD 全景是否产出**，数据从入口到落库的完整链路与转换点
17. **数据载体三条门禁的校验结果**：持久化载体有对应 DAO、转换单元写明覆盖范围、业务载体未直连 DAO
18. **API 清单**：编号、METHOD、路径、路由位置（文件 + 行号）
19. **API 泳道时序是否产出**，泳道是否按调用方向划分而非按步骤
20. **进程与线程视图是否产出**，`processNode` / `threadNode` 是否已在 specification 声明

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
