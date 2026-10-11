# 七层设计链落盘骨架

> 本文件是七层设计链的最小可运行骨架。所有 `.c4` 代码块均经 likec4 1.58.0 实测通过。
> 规则、边界与追溯门禁见 `references/07-seven-layer-design.md`。
> 业务状态机（I 层核心产出）走 Mermaid `stateDiagram-v2`，LikeC4 不支持状态机。

## 文件布局

按层拆分，**只有 SRC 层会继续细分**（也只有它需要 FQN）：

```text
src/
  specification.c4       六层 element kind 定义
  model/
    us.c4                US 层
    framework.c4         F 功能框架 + NF 非功能框架
    implementation.c4    I 实现层：业务目标 / 状态 / 步骤
    ui.c4                UI 界面层：交互设计 + 信息设计
    src.c4               SRC 源码层（子系统多时可拆 src/checkout.c4 等）
  views/
    chain-overview.c4    链路总览（跨层）
    chain-business.c4    业务设计视角（排除 SRC）
    chain-source.c4      源码实现视角
    chain-frame.c4       F 与 NF 框架
    chain-sequence.c4    设计时序
  states/                I 层业务状态机（Mermaid，非 LikeC4）
    <us-id>-state.md
```

**FQN 规则归属**：上五层（US / F / NF / I / UI）是扁平设计，跨文件引用顶层元素用 short name 即可。只有 SRC 层大量嵌套，跨文件引用嵌套元素时才必须 FQN。

详见 `references/02-multifile-and-fqn.md`。

---

## src/specification.c4

```c4
specification {
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
  element system
}
```

`shape` 合法值仅限：`rectangle` `component` `storage` `cylinder` `browser` `mobile` `person` `queue` `bucket` `document`。**无 `hexagon`**。

---

## src/model/us.c4

```c4
model {
  us_checkout = userStory 'US-001 结算下单' {
    description '作为客户，我希望完成一次可追踪的结算下单，以便获得明确的订单确认。'
  }
}
```

编号格式 `US-<三位编号> <标题>`，全局唯一，不复用。

---

## src/model/framework.c4

```c4
model {
  f_order = function 'F-001 订单功能' {
    description '承载订单创建、校验与确认的功能框架。'
  }
  f_payment = function 'F-002 支付功能' {
    description '承载支付发起与结果处理的功能框架。'
  }
  nf_auditability = nonFunction 'NF-001 可审计性' {
    description '所有状态变更留痕，可按订单号回溯。'
  }
  nf_latency = nonFunction 'NF-002 响应时延' {
    description '下单请求 P95 不超过既定阈值。'
  }

  us_checkout -> f_order '要求'
  us_checkout -> f_payment '要求'
  us_checkout -> nf_auditability '要求'
  us_checkout -> nf_latency '要求'
}
```

NF 项必须可度量。无法度量的写 `待补充`，不编造指标。

---

## src/model/implementation.c4

```c4
model {
  i_goal = implStep 'I-001 业务目标' {
    description '目标：客户在一次会话内完成下单，且状态可回溯。'
  }
  i_state = implStep 'I-002 业务状态' {
    description '状态：草稿 → 已校验 → 支付中 → 已确认 / 已取消。详见 states/US-001-state.md'
  }
  i_step = implStep 'I-003 业务步骤' {
    description '步骤：提交订单 → 校验库存 → 发起支付 → 确认或回滚。'
  }

  f_order -> i_goal '实现目标'
  f_order -> i_state '实现状态'
  f_order -> i_step '实现步骤'
  nf_auditability -> i_state '约束状态迁移'
  nf_latency -> i_step '约束步骤耗时'
}
```

**本层禁止出现**类名、函数名、表名、文件名。一旦出现即越界到 SRC 层。

判据：换个人、换技术栈，这层设计依然成立。

---

## src/model/ui.c4

```c4
model {
  ui_interaction = uiSurface 'UI-001 交互设计' {
    description '提交后按钮置灰并显示进度；失败时回退到可编辑状态；支付结果可撤销。'
  }
  ui_information = uiSurface 'UI-002 信息设计' {
    description '字段：订单号、金额、状态、时间。列表区展示历史订单，筛选区按状态与时间过滤，通知区提示支付结果。'
  }

  i_step -> ui_interaction '反馈'
  i_state -> ui_information '展示状态'
}
```

交互设计与信息设计**两类都要有**，缺一即为不完整。

信息设计必须覆盖四种状态：空状态、加载状态、错误状态、无权限状态。

---

## src/model/src.c4

SRC 层是唯一会嵌套的层。下例中 `src_checkout` 内含子组件，因此**跨文件引用 `src_checkout.routes` 必须写 FQN**：

```c4
model {
  src_checkout = srcUnit 'SRC-001 结算入口' {
    description 'src/routes/checkout-routes.js — 接收下单请求并派发。'

    routes = srcUnit 'SRC-001-1 结算路由' {
      description 'src/routes/checkout-routes.js — 路由注册。'
    }
    validate = srcUnit 'SRC-001-2 校验器' {
      description 'src/services/checkout-validator.js — 订单校验。'
    }
  }
  src_orderService = srcUnit 'SRC-002 订单服务' {
    description 'src/services/order-service.js — 订单状态机与校验。'
  }
  src_paymentClient = srcUnit 'SRC-003 支付客户端' {
    description 'src/services/payment-client.js — 调用支付网关。'
  }

  ui_interaction -> src_checkout '触发'
  ui_information -> src_orderService '读取'
  src_checkout -> src_orderService '调用'
  src_orderService -> src_paymentClient '支付'
}
```

**嵌套元素跨文件引用必须 FQN**：`include src_checkout.routes` 合法，`include routes` 报 `Could not resolve reference to Referenceable named 'routes'`。

顶层元素跨文件仍可用 short name——`include src_orderService` 无需写前缀。FQN 的必要性来自嵌套，不来自「跨文件」这件事本身。

**每个 SRC 单元必须绑定真实文件路径**。写不出路径说明该单元尚未实现，标 `待补充`。

反向检查：每个 SRC 单元应能回答「它服务于哪个 I 步骤或 UI 元素」。答不上即为超范围实现。

---

## src/views/chain.c4

视图按层组织。**注意 `chainSource` 引用嵌套元素时用了 FQN**（`src_checkout.routes`），而引用顶层元素直接用 short name：

```c4
views {
  view chainOverview {
    title '设计链路总览'
    description '一个用户故事贯穿功能框架、实现层、界面层与源码层的完整设计链。'
    include *
  }

  view chainBusiness {
    title '业务设计视角（不含源码）'
    description 'US 到 UI 层的业务设计，供业务方确认。不含任何源码元素。'
    include us_checkout
    include f_order, f_payment
    include nf_auditability, nf_latency
    include i_goal, i_state, i_step
    include ui_interaction, ui_information
  }

  view chainSource {
    title '源码实现视角'
    description 'I 层落到 SRC 层的映射，每个源码单元对应真实文件路径。'
    include i_goal, i_state, i_step
    include ui_interaction, ui_information
    include src_checkout.routes
    include src_orderService, src_paymentClient
  }

  view chainFrame {
    title '功能与非功能框架'
    description 'US 驱动的 F 与 NF 框架。'
    include us_checkout
    include f_order, f_payment
    include nf_auditability, nf_latency
  }

  dynamic view chainSequence {
    variant sequence
    title '下单设计时序'
    description '从用户提交到支付确认的步骤序列。'
    include us_checkout, f_order, i_step, ui_interaction
    include src_checkout.routes
    include src_orderService, src_paymentClient

    us_checkout -> f_order '提出下单'
    f_order -> i_step '执行业务步骤'
    i_step -> ui_interaction '反馈交互'
    ui_interaction -> src_checkout.routes '触发源码'
    src_checkout.routes -> src_orderService '调用'
    src_orderService -> src_paymentClient '支付'
  }
}
```

**三条实测约束**：

1. `include f_*` 通配符**不支持** → 必须逐个列出
2. `dynamic view` 若只有 `include` 没有消息 → 布局报 `actors array must not be empty`，且 **`likec4 validate` 仍通过**。必须跑 `build` 才能发现
3. `variant sequence` **只可连接叶子元素** → 上例用的是 `src_checkout.routes`（无子元素的子组件），不是 `src_checkout`（含子元素的容器）
3. `variant sequence` 只可连接叶子元素

---

## states/US-001-state.md（I 层状态机，Mermaid）

```mermaid
stateDiagram-v2
    [*] --> 草稿
    草稿 --> 已校验 : 提交并通过校验
    已校验 --> 支付中 : 发起支付
    支付中 --> 已确认 : 支付成功
    支付中 --> 已取消 : 支付失败或超时
    已校验 --> 草稿 : 校验失败回退
    已确认 --> [*]
    已取消 --> [*]
```

LikeC4 1.58.0 不支持状态机（`opt` `loop` `alt` `try` 均不可用）。业务状态机是 I 层核心产出，必须走 Mermaid。

状态迁移条件必须可审计：每个迁移标注触发条件，满足 NF-001 可审计性要求。

---

## 交付检查

**追溯完整性**

- [ ] 每个 US 链路完整：US → F/NF → I → UI → SRC
- [ ] 缺失层已明确报告，未静默跳过
- [ ] 关系标签说明了「为什么连接」，不是笼统的「关联」
- [ ] 每个 SRC 单元能回答「服务于哪个 I 步骤或 UI 元素」

**命名与层级**

- [ ] 编号格式正确：`US-` `F-` `NF-` `I-` `UI-` `SRC-` + 三位数字
- [ ] 编号全局唯一，删除元素后未回收编号
- [ ] I 层无源码元素（无类名、函数名、表名、文件名）
- [ ] SRC 层每个单元绑定真实文件路径
- [ ] UI 层同时产出交互设计与信息设计
- [ ] 信息设计覆盖空/加载/错误/无权限四种状态
- [ ] NF 项均可度量，不可度量者标 `待补充`

**FQN 与多文件**

- [ ] SRC 层的嵌套元素跨文件引用使用 FQN
- [ ] 上五层（US / F / NF / I / UI）未被无谓地强制 FQN，顶层元素用 short name
- [ ] 文件按层拆分，仅 SRC 层继续细分
- [ ] 视图文件按层命名，视图名全局唯一

**视图类型**

- [ ] 各层使用的视图类型与 `references/07-seven-layer-design.md` 第五节一致
- [ ] I 层步骤用 `dynamic view`，状态机走 Mermaid
- [ ] SRC 层时序用 `variant sequence`
- [ ] 存在业务设计视角且已排除 SRC
- [ ] `dynamic view` 含有显式消息（仅 `include` 会导致 build 布局失败）

**工具路由**

- [ ] 业务状态机走 Mermaid `stateDiagram-v2`
- [ ] 类设计走 PlantUML，未在 LikeC4 中伪造
- [ ] 走轨道二/三的部分已向用户说明原因
- [ ] 构建部署图未产出，或已说明为何此时产出

**校验**

- [ ] `likec4 validate` 通过
- [ ] `likec4 build` 通过（validate 不足以发现布局错误）
- [ ] `likec4 format --check` 通过
