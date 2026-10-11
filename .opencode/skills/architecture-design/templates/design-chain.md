# 设计链落盘骨架

> 本文件是设计链的最小可运行骨架。所有 `.c4` 代码块均经 likec4 1.58.0 实测通过。
> 规则、边界与追溯门禁见 `references/07-design-chain.md`；起点与 Feature 分类见 `references/12-design-origin.md`。
> **主干先行**：所有视图先只画主干，主干确认后再逐条展开分支，见 `references/11-trunk-first-design.md`。
> 业务状态机（I 环核心产出）用 LikeC4「状态即元素 + 迁移即关系」表达，不降级到 Mermaid。

## 文件布局

**一个 Feature 一个 model 文件**，各环元素嵌套在所属 Feature 之下：

```text
src/
  specification.c4         element kind 与 relationship kind 定义
  model/
    feature-checkout.c4    Feature-001（F 类），含其下 US / F / NF / I / UI / SRC
    feature-perf.c4        Feature-004（NF 类）
  views/
    feature-001.c4         作用域指向 Feature，自动带上归属容器
    feature-004.c4
  deployment/
    prod.c4                交付后才产出
```

**归属关系由嵌套表达，不靠跨文件边。** 因此视图打开就能看出每个元素属于哪个 Feature。FQN 规则见 `references/02-multifile-and-fqn.md`。

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

`shape` 合法值仅限：`rectangle` `component` `storage` `cylinder` `browser` `mobile` `person` `queue` `bucket` `document`。**无 `hexagon`**。

**两类边必须分开**：`trace` 是追溯（为什么连），`depends` 是运行时依赖（怎么走）。语法是 `a .kind b`（点号在两端之间），`line` / `color` 写在块**顶层**，不写 `style { }`。

```c4
feat.us_place .trace feat.i_step '落为业务步骤'
feat.i_step .trace feat.src_checkout '落到实现'
feat.src_checkout .depends feat.paymentClient '调用支付网关'
```

**父子之间不可连边**——包含关系已由嵌套表达，`parent .depends parent.child` 报 `Invalid parent-child relationship`。

---

## 两条链的文件布局

F 链与 NF 链是**平级的独立 Feature**，各占一个文件，物理隔离：

```text
src/
  specification.c4                 element kind 与 relationship kind 定义
  model/
    feature-001-f-checkout.c4      Feature-001-F 结算下单（按业务能力切）
    feature-001-nf-perf.c4         Feature-001-NF 支付性能（按质量属性切）
  views/
    feature-001-f.c4               F 链视图
    feature-001-nf.c4              NF 链视图
    nf-panorama.c4                 NF 全景（全量设计时，一次看全部质量属性）
  deployment/
    prod.c4                        交付后才产出
```

**为什么物理隔离而不是同一个 Feature 下双侧**：文件嵌套本身就是一种「顺便检视」的暗示。只要 NF 住在 F 的目录里，AI 和人在推 F 时都会忍不住去看它。平级分文件比口头约定可靠。

**编号用序号关联交付主题**：`Feature-<序号>-F` 与 `Feature-<序号>-NF` 成对，靠序号说明它们服务于同一次交付。

---

## src/model/feature-001-f-checkout.c4（F 链）

```c4
model {
  feat_checkout_f = feature 'Feature-001-F 结算下单' {
    description '按业务能力切分。交付边界：客服在对话中可直接完成下单。可观察：下单转化率提升 15%。所属愿景：让交易更顺。'

    us_place = userStory 'US-001 提交订单' {
      description '作为客服，我能在对话中直接为客户下单，以便当场完成交易。验收：提交后 2 秒内返回订单号。'
    }
    us_pay = userStory 'US-002 完成支付' {
      description '作为客服，我能在下单后立即发起支付，以便客户当场付清。验收：支付结果实时反馈，无需手工刷新。'
    }

    f_order = function 'F-001 订单功能' {
      description '承载订单创建、校验与确认。'
    }
    f_payment = function 'F-002 支付功能' {
      description '承载支付发起与结果处理。'
    }

    i_goal = implStep 'I-001 业务目标' {
      description '目标：客户在一次会话内完成下单。'
    }
    i_state = implStep 'I-002 业务状态' {
      description '状态：草稿 → 已校验 → 支付中 → 已确认 / 已取消。'
    }
    i_step = implStep 'I-003 业务步骤' {
      description '主干步骤：提交订单 → 校验库存 → 发起支付 → 确认。'
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

    // US → 能力：有 US 要求这项能力
    us_place .trace f_order '要求'
    us_pay .trace f_payment '要求'

    // 能力 → I 逻辑
    f_order .trace i_goal '实现目标'
    f_order .trace i_state '实现状态'
    f_order .trace i_step '实现步骤'

    // I → UI → SRC
    i_step .trace ui_interaction '反馈交互'
    i_state .trace ui_information '展示状态'
    ui_interaction .trace src_checkout '触发源码'
    ui_information .trace src_orderService '读取状态'

    // 依赖边：运行时怎么走
    src_checkout .depends src_orderService '调用'
    src_orderService .depends src_paymentClient '支付'
  }
}
```

**链内没有任何 NF 元素。**

---

## src/model/feature-001-nf-perf.c4（NF 链）

**NF 链与 F 链同维度、同本体**——它同样有 US、I、UI、SRC，不比 F 链少任何东西。NF 交付的是「性能感知上的确定性」，这是一项可交付能力。

```c4
model {
  feat_perf_nf = feature 'Feature-001-NF 支付性能' {
    description '按质量属性切分。交付边界：下单超 200ms 时系统明确提示异常，客服可立即重试。可观察：月末高峰客服不需手工刷新。所属愿景：让交易更顺。'

    us_peak = userStory 'US-003 超时提示可操作' {
      description '作为客服，下单超过 200ms 时系统明确提示异常，以便我能立刻判断是重试还是放弃。验收：提示文案说明原因并给出「重试」操作。'
    }
    us_audit = userStory 'US-004 操作可回溯' {
      description '作为客服，我能按订单号查到这次下单的耗时与结果，以便向客户解释。验收：输入订单号可见完整调用链与耗时。'
    }

    nf_latency = nonFunction 'NF-001 支付响应时延' {
      description '支付链路 P95 ≤ 200ms；超出即触发 US-003 的提示路径。'
    }
    nf_auditability = nonFunction 'NF-002 可审计性' {
      description '每次下单的耗时与结果留痕，可按订单号回溯。对应 US-004。'
    }

    i_perf = implStep 'I-101 性能判定逻辑' {
      description '主干步骤：计时 → 判定是否超 200ms → 超时则生成可操作提示 → 留痕。'
    }
    i_audit = implStep 'I-102 审计查询逻辑' {
      description '主干步骤：读取留痕 → 按订单号聚合 → 输出调用链与耗时。'
    }

    ui_warning = uiSurface 'UI-101 超时提示' {
      description '超时弹出层：说明原因、给出重试与取消、错误 / 重试中 / 成功三态。'
    }
    ui_trace = uiSurface 'UI-102 耗时查询' {
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

    // US → 质量属性：有 US 要求这项能力
    us_peak .trace nf_latency '要求'
    us_audit .trace nf_auditability '要求'

    // 质量属性 → I 逻辑
    nf_latency .trace i_perf '实现判定'
    nf_auditability .trace i_audit '实现查询'

    // I → UI → SRC
    i_perf .trace ui_warning '反馈提示'
    i_audit .trace ui_trace '展示结果'
    ui_warning .trace src_probe '触发提示'
    ui_trace .trace src_auditStore '读取留痕'
  }
}
```

**NF 链同样完整闭环**：

| 环 | NF 链的内容 | 对应 F 链的 |
| --- | --- | --- |
| US | US-003 超时提示、US-004 操作可回溯 | US-001 / US-002 |
| 能力单元 | NF-001 时延、NF-002 可审计 | F-001 / F-002 |
| I 逻辑 | I-101 性能判定、I-102 审计查询 | I-001 / I-003 |
| UI | UI-101 超时提示、UI-102 耗时查询 | UI-001 / UI-002 |
| SRC | SRC-101 计时探针、SRC-102 审计存储 | SRC-001 / SRC-002 |

**结构完全同构。** 差别只在切分维度与编号段：F 链用 `F-` / `I-0xx` / `SRC-0xx`，NF 链用 `NF-` / `I-1xx` / `SRC-1xx`。

---

## 禁止的边

**跨链边是硬错误**：

```c4
nf_latency .trace feat_checkout_f.i_step '约束步骤耗时'      // 错：NF 挂进 F 链
nf_latency .trace feat_checkout_f.us_place '约束验收标准'    // 错：NF 指向 F 链的 US
```

**为什么错**：跨链边等于在推 F 的过程中「顺手检视一下 NF」。切面一旦进入主链，就会在每次推进时被反复提及，最终把 F 的视图撑爆。

**注意**：模板中两条链虽然引用了同一个 `specification` 的 element kind，但**互不引用对方的元素**。两条链的编号段不同（F 链 `F-`/`I-0xx`，NF 链 `NF-`/`I-1xx`），避免阅读时混淆。

---

## src/views/feature-001-f.c4

```c4
views {
  view feat001FOverview of feat_checkout_f {
    title 'Feature-001-F 链路总览'
    description '按业务能力切分的完整链路。链内不含任何 NF 元素。'
    include *
  }

  view feat001FBusiness of feat_checkout_f {
    title 'Feature-001-F 业务设计视角（不含源码）'
    description 'US 到 UI 环的业务设计，供业务方确认。'
    include *
    exclude feat_checkout_f.src_checkout
    exclude feat_checkout_f.src_orderService
    exclude feat_checkout_f.src_paymentClient
  }

  dynamic view feat001FSequence {
    variant sequence
    title 'Feature-001-F 主干时序'
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

## 全量设计时必备：各环全景

**每一环都有全景视图**，不只 NF。全景是全量设计的产物，增量设计时不出。

| 全景视图 | 覆盖范围 | 回答什么 |
| --- | --- | --- |
| **F 全景** | 全部 F 链的能力单元 + US + I 逻辑 | 系统对外提供哪些能力 |
| **NF 全景** | 全部 NF 链的质量属性 + US + I 逻辑 | 系统承诺哪些质量水平 |
| **US 全景** | 全部链的 US，按交付主题分组 | 谁要什么 |
| **I 全景** | 全部链的业务状态与步骤 | 业务怎么流转 |
| **UI 全景** | 全部链的界面面 | 用户能看到什么 |
| **SRC 全景** | 全部链的源码单元 | 代码怎么组织 |

**聚合发生在全景层，不发生在链视图层。**

### SRC 环额外必备：源码文件目录视图

SRC 是唯一带真实磁盘资产的环，**必须有目录视图**——否则实现方只拿到抽象单元，看不到实际文件布局。

```c4
views {
  view srcDirectory of feat_checkout_f {
    title 'SRC 目录视图 · Feature-001-F'
    description '本链源码单元与真实文件路径的对应，含嵌套子单元。'
    include *
  }

  view srcDirectoryNF of feat_perf_nf {
    title 'SRC 目录视图 · Feature-001-NF'
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
    title 'F 全景 · 系统对外能力'
    description '全部 F 链的能力单元。一次性呈现，不分散在各链视图里。'
    include feat_checkout_f.f_order
    include feat_checkout_f.f_payment
  }

  view nfPanorama {
    title 'NF 全景 · 系统质量承诺'
    description '全部 NF 链的质量属性。一次性呈现，不在每个 F 视图里检视。'
    include feat_perf_nf.nf_latency
    include feat_perf_nf.nf_auditability
  }

  view usPanorama {
    title 'US 全景 · 谁要什么'
    description '全部链的用户故事，按交付主题分组。'
    include feat_checkout_f.us_place, feat_checkout_f.us_pay
    include feat_perf_nf.us_peak, feat_perf_nf.us_audit
  }

  view iPanorama {
    title 'I 全景 · 业务流转'
    description '全部链的业务逻辑，按编号段区分 F 链与 NF 链。'
    include feat_checkout_f.i_step, feat_checkout_f.i_state
    include feat_perf_nf.i_perf, feat_perf_nf.i_audit
  }

  view srcPanorama {
    title 'SRC 全景 · 源码单元全貌'
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
   ↓ 链内完整推演（US → NF → I → UI → SRC）
   ↓ 关联查询：本次 NF 单元在 SRC 层触达了哪些组件？
   ↓ 起第二条推演：在关联的 F 链上重跑红绿循环
   ↓ F 链推演完，再查关联 NF → 还有未覆盖的质量属性？

起点：F 链
   ↓ 链内完整推演
   ↓ 关联查询：本次改动破坏了哪些质量属性？
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

---

## I 环状态机（LikeC4：状态即元素 + 迁移即关系）

主干状态与分支状态分视图表达，与主干优先一致：

```c4
model {
  st_draft = state '草稿'
  st_validated = state '已校验'
  st_paying = state '支付中'
  st_done = state '已确认'
  st_cancelled = state '已取消（分支）'

  st_draft -> st_validated '提交并通过校验'
  st_validated -> st_paying '发起支付'
  st_paying -> st_done '支付成功'
  st_paying -> st_cancelled '支付失败或超时'
}

views {
  view implStateMain {
    title '订单主干状态'
    description '必经状态链路，不含取消与异常状态。'
    include st_draft, st_validated, st_paying, st_done
  }

  view implStateBranchCancel {
    title '订单分支：取消与失败'
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

- [ ] F 链完整：US → F → I → UI → SRC
- [ ] NF 链完整：US → NF → I → UI → SRC
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