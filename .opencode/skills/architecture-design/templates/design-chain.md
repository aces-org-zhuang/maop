# 设计链落盘骨架

> 本文件是设计链的最小可运行骨架。所有 `.c4` 代码块均经 likec4 1.58.0 实测通过。
> 规则、边界与追溯门禁见 `references/07-design-chain.md`；起点与 Feature 分类见 `references/12-design-origin.md`。
> **主干先行**：所有视图先只画主干，主干确认后再逐条展开分支，见 `references/11-trunk-first-design.md`。
> 业务状态机（I 环核心产出）用 LikeC4「状态即元素 + 迁移即关系」表达，不降级到 Mermaid。

## 文件布局

**一个 Feature 分叉出两条链**，各占一个文件，物理隔离；两条链在构建与部署处收敛：

```text
Feature-001 一次可交付增量
   ↓ 分叉：这次交付的性质是什么
   ├─ Feature-001-F   能力链（按业务能力切）→ 各有自己的 US-00x
   └─ Feature-001-NF  极端场景链（按极端场景切）→ 各有自己的 US-10x
   ↓ 收敛
构建与部署    两条链的 SRC 同处一个制品与运行时
```

```text
src/
  specification.c4element kind 与 relationship kind 定义
  model/
    feature-001-f-checkout.c4      Feature-001-F 结算下单（按业务能力切）
    feature-001-nf-perf.c4         Feature-001-NF 极端场景保障（按极端场景切）
  views/
    feature-001-f.c4               F 链视图（view of，自动带归属容器）
    feature-001-nf.c4              NF 链视图
    dfd-001-f.c4                   DFD 全景（dynamic view，不写 of）
    carrier-001-f.c4               数据载体全景
    apiseq-001-f.c4                API 泳道时序（dynamic view，不写 of）
    api-001-f.c4                   API 清单（element view）
    panorama.c4                    各环全景（全量设计时）
  deployment/
    prod.c4                        进程与线程（deployment view）
```

**为什么物理隔离而不是同一个 Feature 下双侧**：文件嵌套本身就是一种「顺便检视」的暗示。只要 NF 住在 F 的目录里，AI 和人在推 F 时都会忍不住去看它。平级分文件比口头约定可靠。

**编号用序号关联交付主题**：`Feature-<序号>-F` 与 `Feature-<序号>-NF` 成对，靠序号说明它们服务于同一次交付。

**`dynamic view` 不支持 `of <容器>`**（实测报 `Expecting token of type '}' but found 'of'`）。DFD 与 API 泳道时序的归属靠 `description` 与元素嵌套表达。

**`views` 块内不要写 `//` 注释**（实测解析失败）。注释写在块外。

**`dynamic view` 与 `element view` 不能混在同一 `views` 块**（实测报 `Expecting token of type '}' but found 'view'`）。拆成两个文件。

---

## src/specification.c4

```c4
specification {
  element feature {
    style {
      shape rectangle
    }
  }
  element userStory {
    style {
      shape document
    }
  }
  element function {
    style {
      shape rectangle
    }
  }
  element nonFunction {
    style {
      shape mobile
    }
  }
  element implStep {
    style {
      shape rectangle
    }
  }
  element uiSurface {
    style {
      shape browser
    }
  }
  element srcUnit {
    style {
      shape component
    }
  }
  element state {
    style {
      shape rectangle
    }
  }

  // 数据载体：按角色而非语言术语分类。PO / VO / BO / DTO 各语言定义不一，
  // 归一为角色后跨项目一致。命名与门禁见 references/07-design-chain.md。
  element dto {
    style {
      shape rectangle
    }
  }
  element vo {
    style {
      shape rectangle
    }
  }
  element entity {
    style {
      shape rectangle
    }
  }
  element dataAccess {
    style {
      shape cylinder
    }
  }
  element converter {
    style {
      shape mobile
    }
  }

  // 对外接口：独立元素，不是 SRC 单元的别名
  element apiEndpoint {
    style {
      shape rectangle
    }
  }
  element person {
    style {
      shape person
    }
  }

  element system

  // 进程与线程：1.58.0 不自带，必须自定义 deploymentNode
  deploymentNode environment {
    style {
      shape rectangle
    }
  }
  deploymentNode zone {
    style {
      shape rectangle
    }
  }
  deploymentNode machine {
    style {
      shape rectangle
    }
  }
  deploymentNode processNode {
    style {
      shape rectangle
    }
  }
  deploymentNode threadNode {
    style {
      shape rectangle
    }
  }

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
  relationship flow {
    notation '数据流'
    line solid
    color blue
  }
  relationship convert {
    notation '转换'
    line dashed
    color muted
  }
}
```

`shape` 合法值仅限：`rectangle` `component` `storage` `cylinder` `browser` `mobile` `person` `queue` `bucket` `document`。**无 `hexagon`**（转换单元用 `mobile`）。

`color` 合法值仅限已知色名。**无 `purple`**——用 `muted` / `secondary` / `green` / `blue` 等。

**四类边必须分开**：

| 边 | 表达 | 语法 |
| --- | --- | --- |
| `trace` | 为什么连（设计追溯） | `a .trace b '标签'` |
| `depends` | 运行时怎么走（调用依赖） | `a .depends b '标签'` |
| `flow` | 数据往哪走（数据流） | `a .flow b '标签'` |
| `convert` | 在哪一步换了载体 | `a .convert b '标签'` |

**没有 `flow` / `convert` 就无法回答「这个字段从哪来、改它要动几处」。** 四者用同一箭头时数据流信息完全丢失。

语法是 `a .kind b`（点号在两端之间），`line` / `color` 写在块**顶层**，不写 `style { }`。

```c4
feat.us_place .trace feat.i_step '落为业务步骤'
feat.i_step .trace feat.src_checkout '落到实现'
feat.src_checkout .depends feat.paymentClient '调用支付网关'
```

**父子之间不可连边**——包含关系已由嵌套表达，`parent .depends parent.child` 报 `Invalid parent-child relationship`。

---

## src/model/feature-001-f-checkout.c4（F 链）

```c4
model {
  feat_checkout_f = feature 'Feature-001-F 结算下单' {
    description '按业务能力切分。交付边界：客服能确认产品与数量、完成下单并把订单号发给客户。可观察：下单流程可端到端走通。所属愿景：让交易更顺。'

    us_place = userStory 'US-001 提交订单' {
      description '作为客服，我能确认产品与数量并为客户下单，以便当场完成交易。验收：订单已创建，且订单号已送达客户端。'
    }
    us_pay = userStory 'US-002 完成支付' {
      description '作为客服，我能在下单后发起支付并把结果告知客户，以便客户当场付清。验收：支付结果已回显在会话中。'
    }

    f_order = function 'F-001 订单功能' {
      description '承载订单创建、校验与确认。'
    }
    f_payment = function 'F-002 支付功能' {
      description '承载支付发起与结果处理。'
    }

    // **I 环步骤嵌套在 US 容器内**：归属靠嵌套表达，不用跨层边。
    us_place = userStory 'US-001 提交订单' {
      description '作为客服，我能确认产品与数量并为客户下单。验收：订单已创建且订单号已送达。'

      i_of_normalize = implStep 'I-001 归一化请求' { }
      i_of_validate = implStep 'I-002 校验库存' { }
      i_of_create = implStep 'I-003 创建订单' { }
    }

    // ---- I 环 · 业务目标：每条链恰好一个 ----
    //
    // **I 环固定包含三类内容，缺一不可**：业务目标 / 业务状态 / 业务步骤。
    // 三类各用独立编号段：目标 I-G<n>、状态 S-xxx、步骤 I-<三位编号>。

    i_goal = implStep 'I-G0 业务目标' {
      description '目标：客户在一次会话内完成下单。'
    }

    // ---- I 环 · 业务状态：状态即元素，迁移即关系 ----
    //
    // 每条链都必须有业务状态，至少 2 个且有迁移。
    // 「本链无状态」几乎总是漏做而非事实——真实系统总有状态。

    st_draft = state 'S-000 草稿'
    st_validated = state 'S-001 已校验'
    st_paying = state 'S-002 支付中'
    st_done = state 'S-003 已确认'
    st_cancelled = state 'S-004 已取消'

    st_draft -> st_validated '校验通过'
    st_validated -> st_paying '发起支付'
    st_paying -> st_done '支付成功'
    st_validated -> st_cancelled '校验失败或超时'

    // 对外接口与泳道。泳道按调用方向划分，不按操作步骤。
    // **泳道只是 API 时序的分组手段，不是新的存放位置**——UI 与 SRC 单元保持平铺，
    // 泳道内只放接口、外部系统，以及泳道内独立的环节。
    actor_cs = person '客服'

    lane_edge = feature '服务端接入泳道' {
      api_placeOrder = apiEndpoint 'API-001 POST /orders 提交订单' {
        description 'src/routes/checkout-routes.js:42'
      }
      api_getOrder = apiEndpoint 'API-002 GET /orders/{id} 查订单' {
        description 'src/routes/checkout-routes.js:58'
      }
    }
    lane_core = feature '领域层泳道' {
      // **泳道不得自造编号**。环节用真实的 I 步骤元素，
      // 由流程图 include 真实 FQN 表达；此处只写 description 说明范围。
      description '领域层负责校验与下单。具体环节见 us_pay 下的 I-0xx，此处不重复定义'
    }
    lane_ext = feature '外部依赖泳道' {
      ext_pay = system '支付网关' {
        description '第三方支付渠道。'
      }
    }

    ui_interaction = uiSurface 'UI-001 交互设计' {
      description '提交后按钮置灰并显示进度；失败时回退到可编辑状态。'
    }
    ui_information = uiSurface 'UI-002 信息设计' {
      description '字段：订单号、金额、状态、时间。覆盖空 / 加载 / 错误 / 无权限四种状态。'
    }

    src_checkout = srcUnit 'SRC-001 结算入口' {
      description 'src/routes/checkout-routes.js — 接收下单请求并派发。'

      routes = srcUnit 'SRC-001-1 结算路由' {
        description 'src/routes/checkout-routes.js — 路由注册。'
      }
      validate = srcUnit 'SRC-001-2 订单校验器' {
        description 'src/services/checkout-validator.js — 订单校验。'
      }
    }
    src_orderService = srcUnit 'SRC-002 订单服务' {
      description 'src/services/order-service.js — 订单状态机与校验。'
    }
    src_paymentClient = srcUnit 'SRC-003 支付客户端' {
      description 'src/services/payment-client.js — 调用支付网关。'
    }

    // 数据载体：按角色命名，不绑语言术语。详见 references/07-design-chain.md
    in_orderReq = dto 'IN-001 订单提交入参' {
      description 'src/dto/order-request.dto.ts — 承接下单请求，边界校验后转 BIZ。'
    }
    biz_order = entity 'BIZ-001 订单业务对象' {
      description 'src/domain/order.ts — 承载下单规则与状态流转，无持久化注解。'
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
      description 'src/convert/order-converter.ts — 覆盖 POD→BIZ 与 POD→OUT 两组映射。'
    }

    // 清单对应：清单项的来源，不是路径环节
    us_place .trace f_order '要求'
    us_pay .trace f_payment '要求'

    // 下钻路径：US → I → UI → SRC，中途不经过 F
    us_place .trace i_step '落为业务步骤'
    us_pay .trace i_goal '落为业务目标'
    i_step .trace ui_interaction '反馈交互'
    i_state .trace ui_information '展示状态'
    ui_interaction .trace src_checkout '触发源码'
    ui_information .trace src_orderService '读取状态'

    // 依赖边：运行时怎么走
    src_checkout .depends src_orderService '调用'
    src_orderService .depends src_paymentClient '支付'

    // 数据流：业务数据从入口到落库再到展示的完整路径
    ui_interaction .flow in_orderReq '提交下单'
    in_orderReq .convert biz_order '转换为业务对象'
    biz_order .convert pod_order '落为持久化实体'
    pod_order .flow dao_order '写入订单表'
    dao_order .flow out_orderView '查询返回'
    out_orderView .flow ui_information '渲染展示'

    // 转换单元的覆盖范围：必须写成两条独立边。
    // 链式写法 cvt .trace a .trace b 会被LikeC4 当成链式路径 a→b，
    // 报 Invalid parent-child relationship
    cvt_order .trace pod_order '负责 POD→BIZ 映射'
    cvt_order .trace biz_order '负责 POD→OUT 映射'
  }
}
```

**注意四组边的语义不同**：

| 边组 | 语义 | 是否路径环节 |
| --- | --- | --- |
| `us_place .trace f_order '要求'` | 清单项由哪条 US 要求 | **否** |
| `us_place .trace i_step '落为业务步骤'` | US 下钻到 I | **是** |

前者是清单对应关系，后者才是下钻路径。**混为一谈就会读成「US 必须先经过 F 才能到 I」。**

**链内没有任何 NF 元素。**

---

## src/model/feature-001-nf-perf.c4（NF 链 · 极端场景链）

**NF 链与 F 链同维度、同本体**——它同样有 US、I、UI、SRC，不比 F 链少任何东西。

**NF 单元是场景，不是角度。** 「性能」「可审计性」只是观察角度，必须落到具体场景才成为交付物——角度名答不出「谁在什么场景下因此受益」，不是 NF 单元。

```c4
model {
  feat_perf_nf = feature 'Feature-001-NF 极端场景保障' {
    description '按极端场景切分。交付边界：高峰与故障两类场景下，客服能察觉、能行动、不丢数据。所属愿景：让交易更顺。'

    us_peak = userStory 'US-003 高峰期下单不卡' {
      description '作为客服，月末高峰同时处理 20 个会话时，提交订单后无需切出等待，以便不会卡住对话。验收：20 并发下单 P95 ≤ 200ms 且无需手工刷新。'
    }
    us_audit = userStory 'US-004 出问题后能查清' {
      description '作为客服，客户投诉订单异常时，我能查到这次下单的完整经过，以便向客户解释。验收：输入订单号可见完整调用链与各段耗时。'
    }

    nf_peak = nonFunction 'NF-001 高峰 200 并发下单不卡' {
      description '场景：月末高峰 200 并发。表现：下单链路 P95 ≤ 200ms，超出即触发 US-003 的提示路径。角色：客服。'
    }
    nf_trace = nonFunction 'NF-002 客户投诉时可查清经过' {
      description '场景：客户投诉订单异常。表现：完整调用链与各段耗时留痕，可按订单号回溯。对应 US-004。角色：客服。'
    }

    i_perf = implStep 'I-101 高峰判定与提示逻辑' {
      description '主干步骤：计时 → 判定是否超 200ms → 超时则生成可操作提示 → 留痕。'
    }
    i_audit = implStep 'I-102 投诉查询逻辑' {
      description '主干步骤：读取留痕 → 按订单号聚合 → 输出调用链与耗时。'
    }

    ui_warning = uiSurface 'UI-101 高峰超时提示' {
      description '超时弹出层：说明原因、给出重试与取消、错误 / 重试中 / 成功三态。'
    }
    ui_trace = uiSurface 'UI-102 经过查询' {
      description '按订单号展示调用链与各段耗时，覆盖空态（无记录）与错误态（查询失败）。'
    }

    src_probe = srcUnit 'SRC-101 计时探针' {
      description 'src/services/perf-probe.js — 埋点与阈值判定。'

      timer = srcUnit 'SRC-101-1 计时器' {
        description 'src/services/perf-timer.js — 分段计时。'
      }
    }
    src_auditStore = srcUnit 'SRC-102 审计存储' {
      description 'src/repositories/audit-repository.js — 按订单号回溯。'
    }

    // NF 链自己的数据载体：审计数据的入参与持久化。
    // 编号用1xx 段，与 F 链的 0xx 段区分，避免阅读混淆。
    in_auditQuery = dto 'IN-101 审计查询入参' {
      description 'src/dto/audit-query.dto.ts — 承接耗时查询请求。'
    }
    pod_auditRecord = entity 'POD-101 审计留痕实体' {
      description 'src/repository/audit-record.ts — 耗时与结果留痕，与审计表结构对应。'
    }
    out_auditView = vo 'OUT-101 审计出参视图' {
      description 'src/dto/audit-view.dto.ts — 调用链与各段耗时，已脱敏。'
    }
    dao_audit = dataAccess 'DAO-101 审计数据访问' {
      description 'src/repository/audit-repository.ts — 审计表按订单号读取。'
    }
    cvt_audit = converter 'CVT-101 审计载体转换器' {
      description 'src/convert/audit-converter.ts — 覆盖 POD→OUT 映射。'
    }

    // 清单对应：清单项由哪条 US 要求
    us_peak .trace nf_peak '要求'
    us_audit .trace nf_trace '要求'

    // 下钻路径：同样不经过 NF
    us_peak .trace i_perf '落为判定逻辑'
    us_audit .trace i_audit '落为查询逻辑'
    i_perf .trace ui_warning '反馈提示'
    i_audit .trace ui_trace '展示结果'
    ui_warning .trace src_probe '触发提示'
    ui_trace .trace src_auditStore '读取留痕'

    // NF 链的数据流：审计留痕的写入与查询是两条独立路径
    src_probe .flow pod_auditRecord '写入耗时留痕'
    pod_auditRecord .flow dao_audit '落库'
    ui_trace .flow in_auditQuery '提交订单号'
    dao_audit .flow out_auditView '查询返回'
    out_auditView .flow ui_trace '渲染调用链'
    cvt_audit .trace pod_auditRecord '负责 POD→OUT 映射'
  }
}
```

**NF 链的清单对应边与下钻路径边，语义同样要分清**——`us_peak .trace nf_peak` 是清单来源，`us_peak .trace i_perf` 才是路径。

**NF 链与 F 链结构同构**：

| 位置 | NF 链的内容 | 对应 F 链的 | 是什么 |
| --- | --- | --- | --- |
| 路径环节 | US-003 高峰下单不卡、US-004 出问题后能查清 | US-001 / US-002 | **在路径上** |
| 能力单元清单 | NF-001 高峰 200 并发下单不卡、NF-002 客户投诉时可查清经过 | F-001 / F-002 | **不在路径上** |
| 路径环节 | I-101 高峰判定与提示、I-102 投诉查询 | I-001 / I-003 | **在路径上** |
| 路径环节 | UI-101 高峰超时提示、UI-102 经过查询 | UI-001 / UI-002 | **在路径上** |
| 路径环节 | SRC-101 计时探针、SRC-102 审计存储 | SRC-001 / SRC-002 | **在路径上** |
| 数据载体 | IN-101 / POD-101 / OUT-101 / DAO-101 / CVT-101 | IN-001 / POD-001 等 | SRC 环内部维度 |

**两条链的 US 是分别识别的**，不是共享的。US 来源不同、编号段不同、内容完全不同。

**NF 单元写场景不写角度**：「高峰 200 并发下单不卡」是交付物，「性能」只是观察角度。命名判据见 `references/12-design-origin.md`。

**下钻路径两条链完全相同**：`US → I → UI → SRC`。差别在切分维度、US 来源、清单内容与编号段：F 链用 `F-` / `I-0xx` / `SRC-0xx`，NF 链用 `NF-` / `I-1xx` / `SRC-1xx`。

**收敛在构建与部署**：两条链的 SRC 最终进同一个制品、同一个运行时。**分出去的是关注点，合回来的是运行现实。**

---

## 禁止的边

**把清单挂进路径，或跨链引用**：

```c4
nf_peak .trace feat_checkout_f.i_step '约束步骤耗时'      // 错：NF 挂进路径环节
nf_peak .trace feat_checkout_f.us_place '约束验收标准'    // 错：NF 指向 F 链的 US
us_place .trace f_order .trace i_step '串联'                  // 错：把清单串进下钻路径
```

**为什么错**：前两条是在推 F 的过程中「顺手检视 NF」；第三条是把旁挂的清单挤进了必经路径，读起来像「US 必须先经过 F 才能到 I」。

**正确写法**：清单对应与下钻路径是**两组独立的边**，共享同一个 US 端点：

```c4
us_place .trace f_order  '要求'          // 清单对应：清单项的来源
us_place .trace i_step   '落为业务步骤'   // 下钻路径：US → I
```

**注意**：模板中两条链虽然引用了同一个 `specification` 的 element kind，但**互不引用对方的元素**。两条链的编号段不同（F 链 `F-`/`I-0xx`，NF 链 `NF-`/`I-1xx`），避免阅读时混淆。

---

## src/views/feature-001-f.c4

```c4
views {
  view feat001FOverview of feat_checkout_f {
    title 'US 环 · Feature-001-F · 用户故事'
    description '按业务能力切分的完整链路。链内不含任何 NF 元素。'
    include *
  }

  view feat001FBusiness of feat_checkout_f {
    title 'I 环 · Feature-001-F · 业务逻辑'
    description 'US 到 UI 环的业务设计，供业务方确认。'
    include *
    exclude feat_checkout_f.src_checkout
    exclude feat_checkout_f.src_orderService
    exclude feat_checkout_f.src_paymentClient
  }

  dynamic view feat001FSequence {
    variant sequence
    title 'SRC 环 · Feature-001-F · 主干时序'
    description '从提交订单到支付确认的必经步骤。'
    include feat_checkout_f.us_place, feat_checkout_f.i_step
    include feat_checkout_f.ui_interaction, feat_checkout_f.src_checkout.routes
    include feat_checkout_f.src_orderService

    feat_checkout_f.us_place -> feat_checkout_f.i_step '提出下单'
    feat_checkout_f.i_step -> feat_checkout_f.ui_interaction '反馈交互'
    feat_checkout_f.ui_interaction -> feat_checkout_f.src_checkout.routes '触发源码'
    feat_checkout_f.src_checkout.routes -> feat_checkout_f.src_orderService '调用'
  }
}
```

**NF 链视图同构**，见下文实测记录。

---

## 视图命名：id 与 title 都受约束

**`title` 不是自由文本。** 只规范 id 而不管 title，标题就会各写各的，读者无法从标题回推它属于哪个环——「这张图为什么不是 SRC 层的」这类问题就是这么来的。

**title 必须三段式：`<环代号> · <范围> · <编号路径 + 主题>`**。**id 是机器键，title 是人读键，两者必须双射**——从 id 能机械推导 title，反之亦然。

| 视图类别 | title 格式 | 示例 |
| --- | --- | --- |
| `chain<链>-i-<阶段>` | `I 环 · Feature-<链> · I-<阶段> <阶段性目标>` | `I 环 · Feature-001-F · I-001 取得可靠候选知识` |
| `seq<链>-i-<阶段>-lanes` | `I 环 · Feature-<链> · I-<阶段> 泳道流程` | `I 环 · Feature-001-F · I-001 泳道流程` |
| `ui<链>-<单元>` | `UI 环 · Feature-<链> · I-<阶段>-UI-<单元> <单元名>` | `UI 环 · Feature-001-F · I-001-UI-001 会话输入` |
| `ui<链>-<单元>-info-<n>` | `UI 环 · Feature-<链> · UI-<单元>-信息设计-<0n> <名称>` | `UI 环 · Feature-001-F · UI-001-信息设计-001 提问输入信息` |
| `ui<链>-<单元>-act-<n>` | `UI 环 · Feature-<链> · UI-<单元>-交互设计-<0n> <名称>` | `UI 环 · Feature-001-F · UI-001-交互设计-001 提交提问` |
| `pano-src-<链>` | `SRC 环 · Feature-<链> · 模块目录全览` | `SRC 环 · Feature-001-F · 模块目录全览` |
| `dfd<链>-src<模块>-<n>` | `SRC 环 · Feature-<链> · SRC-<模块>-DFD-<0n> <数据流名>` | `SRC 环 · Feature-001-F · SRC-001-DFD-001 提问进入数据流` |
| `api<链>-src<模块>-<n>` | `SRC 环 · Feature-<链> · SRC-<模块>-API-<编号> <METHOD> <路径> <名称>` | `SRC 环 · Feature-001-F · SRC-001-API-001 POST /orders 提交订单` |
| `carrier<链>` | `SRC 环 · Feature-<链> · 数据载体全景` | `SRC 环 · Feature-001-F · 数据载体全景` |
| `erm<链>-<主题>` | `SRC 环 · Feature-<链> · 数据模型全景 · <主题>` | `SRC 环 · Feature-001-F · 数据模型全景 · 工单` |
| `pano-<环>` | `<环代号> · 全部 Feature · <主题>` | `I 环 · 全部 Feature · 业务状态` |
| `proc-<环境>` | `构建部署 · <环境> · 进程与线程` | `构建部署 · 生产环境 · 进程与线程` |

**SRC 四维度一律以 `SRC 环 ·` 开头**——最容易漏的就是这条。

```c4
错  title '数据模型全景 · Feature-001-F 工单结构'
     看不出属于 SRC 环，读者会以为它是独立的一层
对  title 'SRC 环 · Feature-001-F · 数据模型全景 · 工单'

错  title '能力清单'
     看不出是 F 环还是 US 环
对  title 'F 环 · Feature-001-F · 业务能力单元清单'

错  title 'I 环 · Feature-001-F · 阶段 I-001 取得候选知识'
     编号路径不加类别词，「阶段」二字必删——编号前缀已表意
对  title 'I 环 · Feature-001-F · I-001 取得候选知识'
```

**视图 id 只能用九个既定前缀，禁止驼峰与自造前缀**。要区分用连字符后缀（`srcdir001NF-notice`），不改前缀本身。链编号段 `001F` 里的 `F` 是体系既定写法，不算驼峰。

```c4
错  view panoSrc001F / view srcdir001NFnotice / view stateMain
对  view pano-src-001F / view srcdir001NF-notice / view chain001F-i-state-main
```

**编号按 Feature 分段**：`Feature-001` 用 `0xx`，`Feature-002` 用 `2xx`；链内同环连续，跳号要在文件头说明理由（预留给后续增量）。

**泳道不自造编号**：

```c4
错  lane_core = feature '领域层泳道' {
      i_stepLane = implStep 'I-201 应答编排（泳道引用）'   // 自造，同一环节出现两次
    }
对  lane_core = feature '领域层泳道' {
      description '具体环节见 US-001 下的 I-001~I-006，此处不重复定义'
    }
```

**交付前必跑机械校验**（这类错误 `validate` 与 `build` 都拦不住）：

```bash
likec4 export json -o out.json
node scripts/check-naming.mjs out.json
```

---

## 分环视图：一张图只承载一个环，且最多跨一层

**两条硬规则同时生效**：

1. **禁止 `include *`。** 它会把六个环加上数据载体、泳道全部塞进一张——这是"视图跨层"的真正来源。
2. **最多跨一层。** 视图里出现的层只能是「本环 + 直接上一层」。

### 层级链与合法锚

```text
产品愿景 → Feature-001-F → US → I → UI → SRC → 构建部署
            └ F/NF 单元 ┘
```

| 本环 | 合法锚（直接上层） | 越层禁止 |
| --- | --- | --- |
| US / F / NF | Feature | — |
| I | US | Feature、F/NF 单元 |
| UI | I | US、Feature、F/NF 单元 |
| SRC | UI | I、US、Feature、F/NF 单元 |

**最常被违反的一条：SRC 视图里不能出现 F 单元，也不能用 Feature 当容器。** SRC 的上层是 UI，UI 的上层是 I，Feature 已是第三层祖先。

### `include` 容器不会带出子元素（实测）

嵌套写在模型里**不等于**视图里会画出来。这一条纠正了常见误解：

| 视图写法 | 实际渲染 | 判定 |
| --- | --- | --- |
| `include feat_f.us_ask` | 一个**空 US 框**，I 步骤一个都没出现 | **错误** |
| `include feat_f.us_ask.i_normalize` | 只有 I 步骤平铺，US 丢失 | **错误** |
| `include feat_f.us_ask` + `include feat_f.us_ask.i_normalize` | `US[I-001]` | **正确** |

**规则：祖先与目标元素必须同时显式 `include`。**

### 各视图写法

| 视图 | 只包含 |
| --- | --- |
| `chain<链>-us` | Feature 容器 + 本链的 US |
| `chain<链>-f` / `chain<链>-nf` | Feature 容器 + F/NF 单元 + US（**唯一允许同图出现 US 的例外**） |
| `chain<链>-i-goal` | US 容器 + **只**有业务目标 |
| `chain<链>-i-state` | **只**有业务状态与迁移 |
| `chain<链>-i-step` | US 容器 + **只**有业务步骤 |
| `chain<链>-ui` | I 容器 + 本链的交互面与信息设计 |
| `srcdir<链>` | UI 容器 + SRC 单元 |
| `carrier<链>` / `erm<链>` | 载体平铺（SRC 内部横向维度，不强制带容器） |

**I 环必须按内容子类拆图**：业务目标、状态流转、业务步骤是三种不同内容。状态用「状态即元素 + 迁移即关系」，步骤有责任边界时用**泳道流程图**。

```c4
views {
  view chain001F-us of feat_f {
    title 'US 环 · Feature-001-F · 用户故事'
    description '只承载本链的用户故事。不含能力单元、I 环与源码。'
    include feat_f                    // 上层容器：Feature
    include feat_f.us_ask, feat_f.us_pay
  }

  view chain001F-f of feat_f {
    title 'F 环 · Feature-001-F · 业务能力单元清单'
    description '本链的业务能力单元与对应 US。US 在此仅用于展示对应关系。'
    include feat_f                    // 上层容器：Feature
    include feat_f.us_ask, feat_f.us_pay
    include feat_f.f_order, feat_f.f_payment
  }

  view chain001F-i-goal of feat_f {
    title 'I 环 · Feature-001-F · 业务目标'
    description '只承载业务目标。状态流转与业务步骤各自成图。'
    include feat_f.us_ask             // 上层容器：US（I 的直接上层）
    include feat_f.us_ask.i_goal
  }

  view chain001F-i-step of feat_f {
    title 'I 环 · Feature-001-F · 业务步骤'
    description '只承载业务步骤。归属靠 US 容器表达，不画 US→I 的边。'
    include feat_f.us_ask             // 上层容器：US
    include feat_f.us_ask.i_normalize, feat_f.us_ask.i_retrieve
    include feat_f.us_pay, feat_f.us_pay.i_confirm
  }

  view chain001F-ui of feat_f {
    title 'UI 环 · Feature-001-F · 交互面与信息设计'
    description '只承载交互面与信息设计。上层容器是 I 步骤，不是 Feature。'
    include feat_f.us_ask.i_normalize          // 上层容器：I 步骤（UI 的直接上层）
    include feat_f.us_ask.i_normalize.ui_input
  }

  view srcdir001F of feat_f {
    title 'SRC 环 · Feature-001-F · 代码结构'
    description '只承载源码单元。上层容器是 UI 面，SRC 的直接上层不是 Feature。'
    include feat_f.us_ask.i_normalize.ui_input        // 上层容器：UI 面
    include feat_f.us_ask.i_normalize.ui_input.src_route
  }
}
```

**三条不可省的写法**（都是实测踩过的坑）：

1. **祖先与目标元素同时显式 `include`**。只 `include` 容器不会自动带出子元素——实测 `include feat_f.us_ask` 渲染出来是一个**空 US 框**，I 步骤一个都没有。
2. **上层容器必须是直接上一层**。UI 视图锚在 I 步骤，SRC 视图锚在 UI 面。**不得用 Feature 当容器**——那是跳了两层。
3. **跨层用嵌套，不用边**。渲染出 `US[I-001, I-002]` 就够了，再画 `US -> I` 是冗余。

业务步骤的责任边界用泳道表达：

```c4
views {
  dynamic view seq001F-i-step-lanes {
    variant sequence
    title 'I 环 · Feature-001-F · 业务步骤泳道流程'
    description '按责任分区：角色发起、接入层归一化、领域层检索、领域层校验。'
    include feat_f.lane_client.actor_customer
    include feat_f.lane_edge.api_placeOrder
    include feat_f.us_pay.i_normalize, feat_f.us_pay.i_validate
    include feat_f.us_pay.i_create

    feat_f.lane_client.actor_customer -> feat_f.lane_edge.api_placeOrder '①提出问题'
    feat_f.lane_edge.api_placeOrder -> feat_f.us_pay.i_normalize '②归一化请求'
    feat_f.us_pay.i_normalize -> feat_f.us_pay.i_validate '③校验库存'
    feat_f.us_pay.i_validate -> feat_f.us_pay.i_create '④创建订单'
  }
}
```

---

## 全景视图：同类聚合

**一张全景只放一种元素，且聚合单位是 Feature 而非链。**

`pano-f` 收所有 `Feature-NNN-F` 的 F 单元；`pano-nf` 收所有 `Feature-NNN-NF` 的 NF 单元。**链是 Feature 内部的实现单位，不是聚合轴。**

只有一个 Feature 时，`pano-f` 必然等于该链全量——**必须在 description 里声明退化**，不能假装是全景。「F 全景」混入 US 同样会让名字失去意义。

| 全景视图 | 只包含 | 回答什么 |
| --- | --- | --- |
| `pano-us` | **所有 Feature** 的 **US** | 谁要什么 |
| `pano-f` | **所有 `Feature-NNN-F`** 的 **F 单元** | 系统对外提供哪些能力 |
| `pano-nf` | **所有 `Feature-NNN-NF`** 的 **NF 单元** | 系统承诺哪些场景下的表现 |
| `pano-i` | **所有 Feature** 的 **I 环元素** | 业务怎么流转 |
| `pano-i-state` | **所有 Feature** 的**业务状态** | 有哪些状态、怎么迁移 |
| `pano-ui` | **所有 Feature** 的 **UI 元素** | 用户能看到什么 |
| `pano-src` | **所有 Feature** 的 **SRC 单元** | 代码怎么组织 |
| `pano-carrier` | **所有 Feature** 的**载体**（SRC 维度） | 有哪些载体、各自什么角色 |
| `pano-api` | **所有 Feature** 的**接口**（SRC 维度） | 对外暴露哪些契约 |

```c4
views {
  view pano-f {
    title 'F 环 · 全部 Feature-NNN-F · 业务能力单元'
    description '所有链的 F 单元，只含业务能力。刻意不含 US——对应关系见各链的能力清单视图。'
    include feat_f.f_order, feat_f.f_payment
    include feat_nf.f_degrade
  }

  view pano-nf {
    title 'NF 环 · 全部 Feature-NNN-NF · 极端场景单元'
    description '所有链的 NF 单元，只含场景化表现。'
    include feat_nf.nf_peak, feat_nf.nf_trace
  }
}
```

**违规示例**（都是实际犯过的错）：

```c4
错  view pano-f { include feat_f.us_ask, feat_f.f_order }
     「F 全景」里出现 US——名字失去意义，读者无法判断这张图回答什么

错  view pano-i { include feat_f.i_step, feat_f.src_orderService }
     SRC 是独立环，不该出现在 I 环全景里

错  view srcdir001F { include feat_f, feat_f.src_route }
     SRC 的直接上层是 UI，不是 Feature。用 Feature 当容器跨了两层。
```

**`pano-*` 渲染出 `Feature[元素]` 是正确的，不是错位。** 跨 Feature 聚合时 LikeC4 会自动把 Feature 提为容器，这是归属的正确表达。**判定标准是嵌套深度，不是「有没有出现 Feature 框」。**

**必须导出 JSON 核对实际渲染**——`validate` 与 `build` 都拦不住漏画与越层：

```bash
likec4 export json -o out.json
node -e "
const d=require('./out.json');
for(const id of Object.keys(d.views)){
  const v=d.views[id];
  if(v._type!=='element') continue;
  const ns=v.nodes||[];
  console.log(id+'  节点='+ns.length+'  L0='+ns.filter(n=>n.level===0).length+'  L1='+ns.filter(n=>n.level>1).length);
}"
```

| 现象 | 判定 |
| --- | --- |
| 视图宣称有嵌套归属，但 `L1 = 0` | **错误**——子元素根本没画出来 |
| `L1 > 0`，容器是直接上层 | 正确 |
| `L1 > 0`，容器是祖父层 | **错误**——越层 |
| 存在 `level ≥ 2` 的节点 | **错误**——跨了两层以上 |

**归属是否正确看容器的 `children` 前缀，不要用祖先链判定**（LikeC4 渲染时保留完整 FQN，用祖先链会误判为错位）。

**聚合发生在全景层，不发生在链视图层。**

### SRC 环额外必备：六张视图

SRC 环比其他环多四层要求：**它对应真实磁盘资产，业务数据要流过它，系统对外暴露接口，且接口跑在具体进程与线程里。**

| 视图 | 范围 | 含源码路径 | 回答 |
| --- | --- | --- | --- |
| SRC 目录视图 | 本链 | **是** | 文件怎么组织 |
| DFD 全景 | 本链 | 否 | 数据怎么流、在哪转换 |
| 数据载体全景 | 本链 | 否 | 有哪些载体、什么角色 |
| 数据模型全景 | 本链 | 否 | 存储结构与实体关系 |
| **API 清单** | 本链 | 否（带路由位置） | 对外暴露哪些接口 |
| **API 泳道时序** | 本链 | 否 | 一次调用穿过哪些泳道 |
| **进程与线程视图** | 环境级 | 否 | 接口跑在哪台机器的哪个进程的哪个线程 |
| SRC 全景 | **跨全部链** | 否 | 源码单元全貌 |

**DFD 全景是数据维度的唯一视图。** 没有它，「这个字段从哪来」「改这个字段要动几处」无法回答——而这正是实现阶段最频繁的改动。

```c4
views {
  dynamic view dfd001F {
    variant sequence
    title 'SRC 环 · Feature-001-F · 数据流 · 订单'
    description '从界面提交到持久化落库再回显的完整数据流，含载体与转换点。不写 of —— dynamic view 不支持容器作用域。'

    include feat_checkout_f.ui_interaction
    include feat_checkout_f.in_orderReq, feat_checkout_f.biz_order
    include feat_checkout_f.pod_order, feat_checkout_f.dao_order
    include feat_checkout_f.out_orderView

    feat_checkout_f.ui_interaction -> feat_checkout_f.in_orderReq '提交下单'
    feat_checkout_f.in_orderReq -> feat_checkout_f.biz_order '转换为业务对象'
    feat_checkout_f.biz_order -> feat_checkout_f.pod_order '落为持久化实体'
    feat_checkout_f.pod_order -> feat_checkout_f.dao_order '写入订单表'
    feat_checkout_f.dao_order -> feat_checkout_f.out_orderView '查询返回'
    feat_checkout_f.out_orderView -> feat_checkout_f.ui_information '渲染展示'
  }

  view carrier001F of feat_checkout_f {
    title 'SRC 环 · Feature-001-F · 数据载体'
    description '本链所有数据载体的角色定位与转换关系。'
    include feat_checkout_f.in_orderReq, feat_checkout_f.biz_order
    include feat_checkout_f.pod_order, feat_checkout_f.out_orderView
    include feat_checkout_f.dao_order, feat_checkout_f.cvt_order
  }
}
```

**命名**（强制，视图名必须自带类型信息）：`pano-<环>` 同类聚合全景 / `chain<链>-<环>` 分环视图 / `seq<链>-<场景>` 时序 / `dfd<链>-<主题>` / `carrier<链>` / `erm<链>-<主题>` / `srcdir<链>-<主题>` / `api<链>-<主题>` / `proc-<环境>` 运行时。**视图名全局唯一**，重名报 `Duplicate view`。连字符可用。

**`pano-carrier` 与 `carrier001F` 的区别**：前者跨全部链聚合全部载体，后者只看F 链的载体。两者不要混用前缀。

**NF 链同理**，用1xx 段载体编号。DFD 视图里两条链的数据流互不引用。

> 实测：`✓ Valid`，`build` 输出 `✓ all views layouted`。
> 坑：`dynamic view` 不支持 `of`；`views` 块内 `//` 注释会导致解析失败；`dynamic view` 与 `element view` 不能同块。

### API 清单与API 泳道时序

**接口是独立元素，不是 SRC 单元的别名。** 一个单元可暴露多个接口，一个接口也可能由多个单元协作实现。

**泳道按调用方向划分，不按操作步骤**。**泳道只是分组手段，不是新的存放位置**——UI 与 SRC 单元保持平铺，泳道内只放接口、外部系统与泳道内独立环节。

```c4
views {
  view api001F {
    title 'SRC 环 · Feature-001-F · 对外接口'
    description '本链对外接口清单，含方法、路径与路由位置。**逐个 include 接口元素**——只 include lane_edge 容器不会带出子元素，图上只剩一个空的「服务端接入泳道」框。'
    include feat_checkout_f.lane_edge.api_placeOrder
    include feat_checkout_f.lane_edge.api_getOrder
  }
}
```

```c4
views {
  dynamic view apiseq001F {
    variant sequence
    title 'SRC 环 · Feature-001-F · 接口泳道时序 · 提交订单'
    description '泳道按调用方向：接入 → 领域 → 外部。dynamic view 不支持 of。'

    include feat_checkout_f.actor_cs
    include feat_checkout_f.lane_edge.api_placeOrder
    include feat_checkout_f.us_pay.i_of_validate
    include feat_checkout_f.us_pay.i_of_create
    include feat_checkout_f.lane_ext.ext_pay

    feat_checkout_f.actor_cs -> feat_checkout_f.lane_edge.api_placeOrder 'POST /orders'
    feat_checkout_f.lane_edge.api_placeOrder -> feat_checkout_f.us_pay.i_of_validate '校验并创建订单'
    feat_checkout_f.us_pay.i_of_create -> feat_checkout_f.lane_ext.ext_pay '调用支付网关'
    feat_checkout_f.lane_ext.ext_pay -> feat_checkout_f.us_pay.i_of_create '返回支付结果'
  }
}
```

**API 清单回答「有什么」，泳道时序回答「怎么走」。** 只有清单时，接口之间的调用关系要靠读者自己拼。

**接口必须绑定真实路由位置**（路径 + 行号写在 `description`）。写不出位置的接口说明尚未实现，标 `待补充`。

**编号**：`API-<三位编号> <METHOD> <路径> <名称>`，METHOD 保留原文大写，路径原样保留。例：`API-001 POST /orders 提交订单`。

### 进程与线程视图

进程与线程**属于运行投影，用 `deployment` 表达，不用逻辑模型的 element**。

```c4
deployment {
  environment prod '生产环境' {
    zone appZone '应用区' {
      machine appHost 'app-1 · 4C8G' {
        apiInst = instanceOf feat_checkout_f.lane_edge.api_placeOrder
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
    zone dataZone '数据区' {
      machine dbHost 'db-1' {
        processNode dbProc 'PostgreSQL 进程' { }
      }
    }
  }
}

views {
  deployment view procProd {
    title '构建部署 · 生产环境 · 进程与线程'
    description '进程与线程的层级归属。逻辑挂载与线程树并列——instanceOf 节点内不可再嵌节点。'
    include prod.**
  }
}
```

**`processNode` 与 `threadNode` 必须先在 specification 里声明**，1.58.0 不自带。

**进程与线程的层级靠嵌套，不连边**——包含关系已由嵌套给出，连边报 `Invalid parent-child relationship`。

**`instanceOf` 节点内部不能再嵌任何节点**（实测报 `Could not resolve reference to Referenceable named 'httpPool'`）。所以逻辑挂载与线程树只能并列：

```c4
machine appHost 'app-1' {
  apiInst = instanceOf feat_checkout_f.lane_edge.api_placeOrder   // 这个进程承载哪个逻辑元素
  processNode apiProc 'API 进程' {
    threadNode httpPool 'HTTP 线程池' { }                        // 进程内有哪些线程
  }
}
```

**这样也是可接受的**：进程归属与线程构成是两个正交问题——同一接口可部署到多个进程（多副本），同一进程的线程池也不因接口而变。

> 实测：全部`✓ Valid (5 files)` + `build` → `✓ all views layouted`。

### SRC 环额外必备：源码文件目录视图

SRC 是唯一带真实磁盘资产的环，**必须有目录视图**——否则实现方只拿到抽象单元，看不到实际文件布局。

```c4
views {
  view srcdir001F of feat_checkout_f {
    title 'SRC 环 · Feature-001-F · 代码结构'
    description '本链源码单元与真实文件路径的对应，含嵌套子单元。'
    include *
  }

  view srcdir001NF of feat_perf_nf {
    title 'SRC 环 · Feature-001-NF · 代码结构'
    description 'NF 链的源码单元与真实文件路径对应。'
    include *
  }
}
```

**读法**：按嵌套层级展开，每个单元标出其 `description` 里的源码路径。子单元是父单元所在文件内的拆分，**父子不连边**（包含关系已由嵌套表达）。

**目录视图与 SRC 全景的区别**：

| | SRC 目录视图 | SRC 全景 |
| --- | --- | --- |
| 范围 | 本链 | 全部链 |
| 含源码路径 | **含** | 不含路径细节 |
| 回答 | 文件怎么组织 | 源码单元全貌 |

### 全景视图示例

```c4
views {
  view fPanorama {
    title 'F 环 · 全部 Feature-NNN-F · 业务能力单元'
    description '全部 F 链的能力单元。一次性呈现，不分散在各链视图里。'
    include feat_checkout_f.f_order
    include feat_checkout_f.f_payment
  }

  view nfPanorama {
    title 'NF 环 · 全部 Feature-NNN-NF · 极端场景单元'
    description '全部 NF 链的场景单元。一次性呈现，不在每个 F 视图里检视。'
    include feat_perf_nf.nf_peak
    include feat_perf_nf.nf_trace
  }

  view usPanorama {
    title 'US 环 · 全部 Feature · 用户故事'
    description '全部链的用户故事，按交付主题分组。'
    include feat_checkout_f.us_place, feat_checkout_f.us_pay
    include feat_perf_nf.us_peak, feat_perf_nf.us_audit
  }

  view iPanorama {
    title 'I 环 · 全部 Feature · 业务目标与步骤'
    description '全部链的业务逻辑，按编号段区分 F 链与 NF 链。'
    include feat_checkout_f.i_step, feat_checkout_f.i_state
    include feat_perf_nf.i_perf, feat_perf_nf.i_audit
  }

  view srcPanorama {
    title 'SRC 环 · 全部 Feature · 代码结构'
    description '跨全部链的源码单元。文件路径详见各链的 SRC 目录视图。'
    include feat_checkout_f.src_checkout
    include feat_checkout_f.src_orderService, feat_checkout_f.src_paymentClient
    include feat_perf_nf.src_probe, feat_perf_nf.src_auditStore
  }
}
```

**注意**：全景视图可以同时 `include` 两条链的元素——**这是唯一允许跨链的地方**，因为全景的职责就是横向聚合。链视图仍然禁止跨链。

---

## 跨链接力推演

**链内推演闭环不等于推演结束。** 两条链之间存在关联，必须沿关联起第二条推演。

```text
起点：NF 链
   ↓ 链内完整推演（下钻路径 US → I → UI → SRC）
   ↓ 关联查询：本次 NF 单元在 SRC 层触达了哪些组件？
   ↓ 起第二条推演：在关联的 F 链上重跑红绿循环
   ↓ F 链推演完，再查关联 NF → 还有未覆盖的质量属性？

起点：F 链
   ↓ 链内完整推演
   ↓ 关联查询：本次改动破坏了哪些场景下的表现？
   ↓ 起第二条推演：在关联的 NF 链上重跑红绿循环

直到两侧都无法再起新推演，才算推演结束。
```

**关键区别**：

| 做法 | 是否重跑红绿循环 | 结果 |
| --- | --- | --- |
| 在 NF 链里检视 F | 否 | F 的红点从未被验证，且 F 链视图被撑爆 |
| **起 F 链的新推演** | 是 | F 链独立验证自己的红点，NF 链保持干净 |

**任何一方都无法单独证明跨链影响**——质量承诺要作用在功能上，这个作用能否成立只在 F 链的上下文里能验证；反过来同理。这是两条链独立闭环的必然代价。

**「无关联」也要显式说明**，空白会让读者以为忘了这一步。

---

## F / NF 链内门禁（两条链各查一遍）

| 检查项 | 判定 |
| --- | --- |
| 每个能力单元至少有一条来自 US 的入追溯边 | **入边为零 = 凭空出现的单元**，必须报告 |
| 每条链各自的 `US → 能力` 边未写成 `约束` 类标签 | 两条链的门禁形式相同，都是「US 要求这项能力」 |
| 链内未出现对方链的元素 | F 链无 NF 元素，NF 链无 F 元素 |
| 编号段区分 | F 链 `F-`/`I-0xx`/`SRC-0xx`；NF 链 `NF-`/`I-1xx`/`SRC-1xx` |
| NF 项可度量 | 「系统要快」不合格；「P95 ≤ 200ms」合格；无法度量标 `待补充` |

### 数据载体门禁（SRC 环内，每条链各查一遍）

| 检查项 | 判定 |
| --- | --- |
| 每个持久化载体有对应的数据访问单元 | **入边为零 = 没人读也没人写的死代码**，必须报告 |
| 每个转换单元写明覆盖哪几个载体之间的映射 | 写在 `description`；不写等于字段变更时无人知道改哪里 |
| 业务载体未直连数据访问单元 | 直连说明持久化细节泄漏进业务逻辑，中间须经持久化载体或转换单元 |
| 载体编号按角色前缀 | `IN` / `BIZ` / `POD` / `OUT` / `DAO` / `CVT`，**不用** PO / VO / BO / DTO |
| 载体绑定真实文件路径 | 路径写在 `description`，与 SRC 单元同一要求 |
| 两条链的载体编号段区分 | F 链用 0xx，NF 链用 1xx |
| DFD 全景已产出 | 数据流有 `.flow` 边，转换点有 `.convert` 边 |

**为什么转换单元必须独立编号**：转换散落在各处的 `set` / `copy` 方法里，就没人能回答「字段变更会影响哪些转换」。转换集中在一处是数据契约可维护的前提。

---

## 数据流与数据模型的区别

两者都是SRC 环的数据维度，**不可互相替代**。

| | 数据模型全景（ER） | DFD 全景 |
| --- | --- | --- |
| 元素 | 持久化实体（`store`） | 全部数据载体 + UI 边界 |
| 关系 | 从属、引用 | `.flow` 数据流、`.convert` 载体转换 |
| 回答 | 存储长什么样 | 这个字段从哪来、改它要动几处 |
| 视图类型 | `element view` | `dynamic view variant sequence` |

**ER 用 `store` 承载实体**（`shape database` 非法，用 `cylinder` / `storage`）。字段清单写在 `description`，图上不承载字段定义——不要试图用图表达字段。

---

## I 环状态机（LikeC4：状态即元素 + 迁移即关系）

主干状态与分支状态分视图表达，与主干优先一致：

```c4
model {
  st_draft = state 'S-000 草稿'
  st_validated = state 'S-001 已校验'
  st_paying = state 'S-002 支付中'
  st_done = state 'S-003 已确认'
  st_cancelled = state 'S-004 已取消'

  st_draft -> st_validated '提交并通过校验'
  st_validated -> st_paying '发起支付'
  st_paying -> st_done '支付成功'
  st_paying -> st_cancelled '支付失败或超时'
}

views {
  view implStateMain {
    title 'I 环 · Feature-001-F · 业务状态 · 主干'
    description '必经状态链路，不含取消与异常状态。'
    include st_draft, st_validated, st_paying, st_done
  }

  view implStateBranchCancel {
    title 'I 环 · Feature-001-F · 业务状态 · 分支取消与失败'
    description '自「支付中」节点岔出，合流至「已取消」节点。'
    include st_paying, st_cancelled
  }
}
```

**代价**：不能自环（`已校验 -> 草稿` 这类回退写在 `description` 中）；非经典状态机外观；视图需逐个列元素（`include st_*` 通配符不支持）。

**主干状态视图 ≤ 8 个状态，超出即按分支拆分。**

---

## 交付检查

**交付边界与切分维度**

- [ ] 交付边界已写成一句话，且业务方能说「不是」
- [ ] F 链与 NF 链各自有独立交付边界，序号配对（`Feature-001-F` / `Feature-001-NF`）
- [ ] **F 与 NF 同维度处理**，未被建模为「功能 vs 约束」
- [ ] 增量设计一次只推了一条链，未把另一条链拽进来
- [ ] 全量设计出了 NF 全景视图，而非在每个 F 视图里检视 NF

**两条链各自闭环**

- [ ] F 链下钻路径完整：US → I → UI → SRC
- [ ] NF 链下钻路径完整：US → I → UI → SRC
- [ ] **链内未出现对方链的元素**
- [ ] **无跨链边**（`nf → F 链元素` 一律禁止）
- [ ] 每个能力单元有来自 US 的入追溯边
- [ ] NF 链的 US 有角色、场景、期望与可判定验收，与 F 链 US 同构

**命名与归属**

- [ ] 编号格式：`Feature-<序号>-F|NF`、`US-`、`F-`、`NF-`、`I-`、`UI-`、`SRC-`
- [ ] **编号段区分**：F 链 `I-0xx`/`SRC-0xx`，NF 链 `I-1xx`/`SRC-1xx`
- [ ] 编号全局唯一，删除元素后未回收
- [ ] 两条链各占一个 model 文件，物理隔离
- [ ] I 环无源码元素（无类名、函数名、表名、文件名）
- [ ] SRC 单元绑定真实源码路径，无路径者标 `待补充`
- [ ] UI 环同时产出交互设计与信息设计，覆盖四种状态
- [ ] NF 项均可度量，不可度量者标 `待补充`

**数据载体与数据流（SRC 环）**

- [ ] 数据载体按角色编号：`IN` / `BIZ` / `POD` / `OUT` / `DAO` / `CVT`，**未用** PO / VO / BO / DTO 作为前缀
- [ ] 每个持久化载体有对应的数据访问单元
- [ ] 每个转换单元在 `description` 写明覆盖哪几组映射
- [ ] 业务载体未直连数据访问单元
- [ ] 载体绑定真实文件路径
- [ ] **DFD 全景已产出**，数据从入口到落库的路径完整，转换点有 `.convert` 边
- [ ] 数据载体全景与数据模型全景已产出
- [ ] 两条链的载体编号段区分：F 链 0xx，NF 链 1xx
- [ ] 四类边未混用：`trace` / `depends` / `flow` / `convert` 各自语义清晰

**对外接口与运行时（SRC 环）**

- [ ] 接口按 `API-<编号> <METHOD> <路径> <名称>` 编号，METHOD 大写、路径原样
- [ ] 每个接口绑定真实路由位置（文件 + 行号），无位置者标 `待补充`
- [ ] **API 清单已产出**
- [ ] **API 泳道时序已产出**，泳道按**调用方向**划分而非按步骤
- [ ] 泳道只是分组手段，UI 与 SRC 单元未因此被搬进泳道
- [ ] **进程与线程视图已产出**，`processNode` / `threadNode` 已在 specification 声明
- [ ] `instanceOf` 与 `processNode` / `threadNode` 为**兄弟关系**，未把节点嵌进 `instanceOf`
- [ ] 进程与线程之间未连边（包含关系由嵌套表达）
- [ ] 进程视图为环境级，命名不带链序号

**视图聚焦与命名**

- [ ] **每张全景只含一种元素**（`pano-f` 只有 F 单元，无 US / I / SRC）
- [ ] **无任何视图使用 `include *`**
- [ ] 每张链视图只承载一个环
- [ ] **I 环按内容子类拆图**：业务目标 / 状态流转 / 业务步骤各自成图
- [ ] 业务步骤有责任边界时用泳道流程图
- [ ] 能力清单视图同时含 US 是有意例外，`description` 已写明
- [ ] 全景用 `pano-<环>`，分环用 `chain<链>-<环>`，时序用 `seq<链>-<场景>`
- [ ] SRC 各维度用 `dfd` / `carrier` / `erm` / `api` / `srcdir` / `proc` 前缀
- [ ] 视图名全局唯一

**FQN 与多文件**

- [ ] 跨作用域引用嵌套元素使用 FQN（`feat_checkout_f.src_checkout`）
- [ ] 父子之间未连边
- [ ] 视图名全局唯一

**视图**

- [ ] 各环视图类型与 `references/07-design-chain.md` 第五节一致
- [ ] `dynamic view` 含有显式消息（仅 `include` 会导致 build 布局失败）
- [ ] 主干视图与分支视图已分离，分支命名 `*-branch-<条件>`
- [ ] 各视图容量未超限（元素 ≤ 12 / 步骤 ≤ 8 / 状态 ≤ 8）

**校验**

- [ ] `likec4 validate` 通过
- [ ] `likec4 build` 通过（validate 不足以发现布局错误）