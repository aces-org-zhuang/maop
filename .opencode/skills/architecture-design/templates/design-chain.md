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

## src/model/feature-checkout.c4（F 类 Feature）

```c4
model {
  feat_checkout = feature 'Feature-001 结算下单' {
    description '本次做到：客服在对话中可直接完成下单。可观察：下单转化率提升 15%。所属愿景：让交易更顺。'

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
    nf_auditability = nonFunction 'NF-001 可审计性' {
      description '所有状态变更留痕，可按订单号回溯。落在 US-002 上。'
    }
    nf_latency = nonFunction 'NF-002 响应时延' {
      description '下单请求 P95 不超过 200ms。落在 US-001 上：客服提交后无需切换页面等待。'
    }

    i_goal = implStep 'I-001 业务目标' {
      description '目标：客户在一次会话内完成下单，且状态可回溯。'
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

    // 追溯边：为什么连
    f_order .trace i_goal '实现目标'
    f_order .trace i_state '实现状态'
    f_order .trace i_step '实现步骤'
    nf_auditability .trace i_state '约束状态迁移'
    nf_latency .trace i_step '约束步骤耗时'
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

**要点**：

- 编号格式 `Feature-` `US-` `F-` `NF-` `I-` `UI-` `SRC-` + 三位数字，全局唯一不复用
- **NF 项必须可度量**，且**必须落在至少一条 US 的验收标准上**，否则是空悬约束
- **I 环禁止出现**类名、函数名、表名、文件名。判据：换个人、换技术栈，这环设计依然成立
- **SRC 单元必须绑定真实源码路径**（写在 `description` 里），写不出路径说明尚未实现，标 `待补充`
- **父子之间不连边**——`src_checkout` 与 `src_checkout.routes` 是嵌套关系，不写 `depends` 边
- **注意区分两种引用**：`feat_checkout.src_checkout` 是架构设计 FQN（给 LikeC4 定位），`src/routes/checkout-routes.js` 是源码路径（供人工核对），两者并列

---

## src/model/feature-perf.c4（NF 类 Feature）

**NF 类不得跳过 US 环**。质量目标必须落到可感知收益上，否则无人能验收。

```c4
model {
  feat_perf = feature 'Feature-004 支付性能提升' {
    description '本次做到：月末结算高峰，客服不用再手工刷新状态。可观察：20 并发下单 P95 ≤ 200ms。所属愿景：让交易更顺。'

    us_peak = userStory 'US-005 高峰下单不卡' {
      description '作为一线客服，月末高峰同时处理 20 个会话时，提交订单后无需切出等待。验收：20 并发下单 P95 ≤ 200ms，且客服侧无需手工刷新。'
    }

    // NF 类：F 侧显式声明无需新增，不沉默跳过
    f_note = function 'F-005 本次无需新增功能单元' {
      description '对外可见能力不变，本次仅提升既有支付链路的响应时延。'
    }

    nf_latency = nonFunction 'NF-003 支付响应时延' {
      description '支付链路 P95 ≤ 200ms。落在 US-005 上。'
    }
    nf_consistency = nonFunction 'NF-004 数据一致性' {
      description '优化后仍保证支付状态最终一致，不出现超卖。落在 US-005 上。'
    }

    i_step = implStep 'I-004 业务步骤' {
      description '主干步骤：提交订单 → 批量预取 → 发起支付 → 确认。'
    }

    src_paymentClient = srcUnit 'SRC-004 支付客户端（优化）' {
      description 'src/services/payment-client.js — 增加批量预取与连接复用。'
    }

    nf_latency .trace i_step '约束步骤耗时'
    i_step .trace src_paymentClient '落到实现'
  }
}
```

**两类 Feature 走同一条链，只在产出重心上不同**：

| | F 类 | NF 类 |
| --- | --- | --- |
| US | 有 | **必须有** |
| F 侧 | 有新增单元 | **显式声明「无需新增」** |
| NF 侧 | 附带约束 | **本次主要产出** |
| I / UI / SRC | 照常 | 照常 |

---

## src/views/feature-001.c4

视图按 Feature 组织，**作用域指向 Feature 即自动带上归属容器**：

```c4
views {
  view feat001Overview of feat_checkout {
    title 'Feature-001 链路总览'
    description '本次交付贯穿 US、I、UI、SRC 的完整链路。'
    include *
  }

  view feat001Business of feat_checkout {
    title 'Feature-001 业务设计视角（不含源码）'
    description 'US 到 UI 环的业务设计，供业务方确认。不含任何源码元素。'
    include *
    exclude feat_checkout.src_checkout
    exclude feat_checkout.src_orderService
    exclude feat_checkout.src_paymentClient
  }

  view feat001Frame of feat_checkout {
    title 'Feature-001 功能与非功能框架'
    description 'F 与 NF 的对照，NF 项均落在 US 验收标准上。'
    include feat_checkout.us_place, feat_checkout.us_pay
    include feat_checkout.f_order, feat_checkout.f_payment
    include feat_checkout.nf_auditability, feat_checkout.nf_latency
  }

  view feat001Source of feat_checkout {
    title 'Feature-001 源码实现视角'
    description 'I 环落到 SRC 的映射，每个源码单元对应真实文件路径。'
    include feat_checkout.i_step, feat_checkout.ui_interaction
    include feat_checkout.src_checkout.routes
    include feat_checkout.src_orderService, feat_checkout.src_paymentClient
  }

  dynamic view feat001Sequence {
    variant sequence
    title 'Feature-001 主干时序'
    description '从提交订单到支付确认的必经步骤，不含异常与可选分支。'
    include feat_checkout.us_place, feat_checkout.i_step
    include feat_checkout.ui_interaction, feat_checkout.src_checkout.routes
    include feat_checkout.src_orderService

    feat_checkout.us_place -> feat_checkout.i_step '提出下单'
    feat_checkout.i_step -> feat_checkout.ui_interaction '反馈交互'
    feat_checkout.ui_interaction -> feat_checkout.src_checkout.routes '触发源码'
    feat_checkout.src_checkout.routes -> feat_checkout.src_orderService '调用'
  }
}
```

**跨作用域引用嵌套元素一律用 FQN**（`feat_checkout.src_checkout.routes`）。写 `include routes` 报 `Could not resolve reference to Referenceable named 'routes'`。

**四条实测约束**：

1. `include f_*` 通配符**不支持** → 必须逐个列出
2. `dynamic view` 若只有 `include` 没有消息 → 布局报 `actors array must not be empty`，且 **`likec4 validate` 仍通过**。必须跑 `build` 才能发现
3. `variant sequence` **只可连接叶子元素** → 上例用 `src_checkout.routes`（无子元素的子组件），不用 `src_checkout`
4. **父子不可连边** → `src_checkout .depends src_checkout.routes` 报 `Invalid parent-child relationship`

---

## 主干视图与分支视图的分离（主干优先）

**所有视图先只画主干，主干确认后再逐条展开分支**。规则见 `references/11-trunk-first-design.md`。

主干命名 `*-main`，分支命名 `*-branch-<条件>`，成对出现：

```c4
views {
  dynamic view feat001Main {
    variant sequence
    title '主干：下单必经路径'
    description '从提交订单到支付确认的必经步骤，不含异常与可选分支。'
    include feat_checkout.us_place, feat_checkout.i_step
    include feat_checkout.src_checkout.routes
    feat_checkout.us_place -> feat_checkout.i_step '提出下单'
    feat_checkout.i_step -> feat_checkout.src_checkout.routes '执行下单'
  }

  dynamic view feat001BranchStockShort {
    variant sequence
    title '分支：库存不足'
    description '自「业务步骤」节点岔出，合流至「下单失败」节点。'
    include feat_checkout.i_step, feat_checkout.src_checkout.validate
    feat_checkout.i_step -> feat_checkout.src_checkout.validate '库存校验'
    feat_checkout.src_checkout.validate -> feat_checkout.i_step '库存不足则终止'
  }
}
```

静态结构视图用 `exclude` 把分支元素从主干视图剔除（同样实测通过）：

```c4
views {
  view feat001Trunk {
    title '主干：功能框架'
    description '主干必需的功能单元，不含可选与增强类功能。'
    include *
    exclude feat_perf.f_note
  }
}
```

**容量上限**：element view ≤ 12 元素、dynamic view ≤ 8 步 / 10 条消息、状态视图 ≤ 8 状态。超限即拆。

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

状态迁移条件必须可审计：每个迁移标注触发条件，满足 NF-001 可审计性要求。**主干状态视图 ≤ 8 个状态，超出即按分支拆分。**

---

## 交付检查

**交付边界与 Feature 类型**

- [ ] 交付边界已写成一句话，且业务方能说「不是」
- [ ] Feature 类型已判定（F 类 / NF 类），判据是对外可见能力是否变化，非占比
- [ ] NF 类 Feature 已建立 US 体系，验收含可感知收益
- [ ] NF 类 Feature 的 F 侧已显式声明「无需新增」
- [ ] 每个 NF 项都落在至少一条 US 的验收标准上，无空悬 NF

**追溯完整性**

- [ ] 链路完整：Feature → US → I → UI → SRC
- [ ] 缺失环已明确报告，未静默跳过
- [ ] 每条追溯边都用 `.trace`，未与 `.depends` 混用
- [ ] 每个 SRC 单元能回答「服务于哪个 I 环步骤或 UI 元素」；纯依赖节点已标注而非判为超范围

**命名与归属**

- [ ] 编号格式正确：`Feature-` `US-` `F-` `NF-` `I-` `UI-` `SRC-` + 三位数字
- [ ] 编号全局唯一，删除元素后未回收
- [ ] 各环元素嵌套在所属 Feature 之下，视图打开即见归属
- [ ] I 环无源码元素（无类名、函数名、表名、文件名）
- [ ] SRC 单元绑定真实源码路径，无路径者标 `待补充`
- [ ] UI 环同时产出交互设计与信息设计
- [ ] 信息设计覆盖空 / 加载 / 错误 / 无权限四种状态
- [ ] NF 项均可度量，不可度量者标 `待补充`

**FQN 与多文件**

- [ ] 跨作用域引用嵌套元素使用 FQN（`feat_checkout.us_place`）
- [ ] 父子之间未连边
- [ ] 一个 Feature 一个 model 文件
- [ ] 视图名全局唯一

**视图类型**

- [ ] 各环视图类型与 `references/07-design-chain.md` 第五节一致
- [ ] I 环步骤用 `dynamic view`，状态机用「状态即元素 + 迁移即关系」
- [ ] SRC 环时序用 `variant sequence`
- [ ] 存在业务设计视角且已排除 SRC
- [ ] `dynamic view` 含有显式消息（仅 `include` 会导致 build 布局失败）
- [ ] 主干视图与分支视图已分离，分支命名 `*-branch-<条件>`，只画增量与接缝锚点
- [ ] 各视图容量未超限（元素 ≤ 12 / 步骤 ≤ 8 / 状态 ≤ 8）

**校验**

- [ ] `likec4 validate` 通过
- [ ] `likec4 build` 通过（validate 不足以发现布局错误）