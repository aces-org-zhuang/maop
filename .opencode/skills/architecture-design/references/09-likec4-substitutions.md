# SOP 09 - 全部图形的 LikeC4 表达（禁止降级）

## 目的

**所有架构图必须用 LikeC4 表达，不允许降级到 Mermaid、PlantUML 或其他工具。**

本 SOP 提供每种图在 LikeC4 1.58.0 下的表达方式。**每种平替都有代价——代价写在这里，使用者知情后再选，而不是被静默降级到另一套工具。**

选 LikeC4 的理由只有一个，但足够充分：**单一真源、可校验、可 diff、可被 AI 经 MCP 查询。** 一旦引入第二套工具，架构真相就会分裂成两份，且无法互相验证。

## 能力事实（官方规格 + 1.58.0 实测）

### LikeC4 没有的语法

查证官方 `llms-full.txt` 与 1.58.0 实测，以下语法**不存在**：

```text
swimlane    lane    participant    column
```

**不要写这些关键字。** 它们不会报错为"未知关键字"，而是会产生难以理解的解析错误。

### LikeC4 1.58.0 不可用的流程控制块

已复测确认：`opt` `loop` `break` `alt` `when` `else` `try` `catch` `finally` **在 1.58.0 全部不可用**，报错形如：

```text
Line 11: Expecting token of type '}' but found `alt`.
Line 15: Expecting token of type 'EOF' but found `else`.
```

**注意**：官方 `llms-full.txt` 描述了这些块，那是更新版本的能力。写进去会让 `validate` 失败。可用的只有 `parallel` / `par`，且**不可嵌套**。

---

## 一、泳道（Swimlane）

### 结论：LikeC4 无泳道语法，用嵌套容器实现

**做法**：泳道建成一个容器元素，泳道内的步骤作为其子元素。

```c4
model {
  lane_customer = stage '客户侧' {
    s_browse = step '浏览商品'
    s_order = step '提交订单'
  }

  lane_system = stage '系统侧' {
    s_validate = step '校验订单'
    s_pay = step '发起支付'
  }

  // 跨泳道关系在容器作用域外声明
  s_order -> s_validate '提交至'
  s_validate -> s_pay '通过后'
}
```

```c4
views {
  view swimlane {
    title '下单流程泳道'
    include user
    include lane_customer, lane_system
  }
}
```

`stage` 的 style 应强化视觉分组：

```c4
specification {
  element stage {
    style {
      shape rectangle
      color blue
    }
  }
}
```

### 代价与必须注意

| 项 | 说明 |
| --- | --- |
| **不是真泳道** | 渲染为带边框的分组盒子，布局**不保证竖列排列**。不要在描述里承诺"泳道对齐" |
| 跨泳道引用 | 视图里引用子元素需 FQN：`include lane_customer.s_browse` |
| 时序图限制 | `variant sequence` 只连叶子元素，须引子元素而非容器 |
| 强化视觉 | 靠 `color` / `shape` / `opacity` 区分泳道，别只靠边框 |

### 各层怎么组织泳道

| 场景 | 泳道划分依据 |
| --- | --- |
| I 层业务流程 | 按参与角色（客户侧 / 系统侧 / 运营侧） |
| SRC 层调用链 | 按层（入口层 / 业务层 / 适配层 / 外部） |
| UI 层交互 | 按界面（管理台 / 用户端 / 移动端） |
| NF 约束 | 按质量维度（性能 / 安全 / 可用性） |

**优先用"按角色"和"按层"**，避免按"按步骤"建泳道——后者会让每个泳道只有一个元素，失去分组意义。

---

## 二、状态机

### 结论：状态即元素，迁移即关系

```c4
model {
  st_start = terminal '开始'
  st_draft = state '草稿'
  st_validated = state '已校验'
  st_paying = state '支付中'
  st_done = state '已确认'
  st_cancelled = state '已取消'
  st_end = terminal '结束'

  st_start -> st_draft '创建'
  st_draft -> st_validated '校验通过'
  st_validated -> st_paying '发起支付'
  st_paying -> st_done '支付成功'
  st_paying -> st_cancelled '支付失败或超时'
  st_done -> st_end '完成'
  st_cancelled -> st_end '终止'
}
```

```c4
views {
  view orderState {
    title '订单状态机'
    description '状态用元素表达，迁移用关系表达。'
    include st_start, st_draft, st_validated
    include st_paying, st_done, st_cancelled, st_end
  }
}
```

### 代价

| 项 | 说明 |
| --- | --- |
| **不能自环** | `st_draft -> st_draft` 报 `Invalid parent-child relationship`。自反迁移写在 `description` 里，或单独建一个重试视图 |
| 无 UML 状态机外观 | 渲染为普通关系图，不是经典状态机样式。可读性依赖关系标签 |
| 视图需逐个列元素 | `include st_*` 通配符不支持（见 `02-multifile-and-fqn.md`） |

### 自反迁移的替代

```c4
st_draft = state '草稿' {
  description '校验失败时回退到本状态，形成自反迁移。'
}
```

---

## 三、条件分支、循环、异常

`opt` `alt` `loop` `try` 均不可用。**平替方式是拆成多个视图，每个视图表达一条路径。**

### 条件分支

```c4
// 支付成功路径
dynamic view paySuccess {
  variant sequence
  title '支付成功路径'
  include s_order, s_validate, s_pay, st_done
  s_order -> s_validate '提交'
  s_validate -> s_pay '校验通过'
  s_pay -> st_done '支付成功'
}

// 支付失败路径
dynamic view payFailed {
  variant sequence
  title '支付失败路径'
  include s_order, s_validate, s_pay, st_cancelled
  s_order -> s_validate '提交'
  s_validate -> s_pay '校验通过'
  s_pay -> st_cancelled '支付失败或超时'
}
```

**视图标题必须写清路径条件**，否则读者无法判断该看哪个。

### 循环

拆为「单次迭代视图」+「迭代关系视图」：

```c4
view retryOnce {
  title '单次重试'
  include s_retry, s_pay
  s_retry -> s_pay '重试支付'
}

view retryLoop {
  title '重试循环（最多 N 次）'
  description 's_retry 在 st_failed 状态下可重复触发，直到超过重试上限。'
  include s_pay, st_failed, st_done
  s_pay -> st_failed '再次失败'
  s_pay -> st_done '成功'
}
```

### 异常

独立成视图，并把异常路径与正常路径分开：

```c4
dynamic view payException {
  variant sequence
  title '支付异常处理'
  include s_pay, ragflow, st_cancelled
  s_pay -> ragflow '异常上报'
  ragflow -> st_cancelled '记录并终止'
}
```

---

## 四、类图与继承

### 结论：嵌套表达包含，关系表达依赖

```c4
model {
  src_orderService = srcUnit 'SRC-002 订单服务' {
    src_repository = srcUnit 'SRC-002-1 订单仓储' {
      description 'src/repositories/order-repository.js'
    }
    src_validator = srcUnit 'SRC-002-2 订单校验器' {
      description 'src/validators/order-validator.js'
    }
  }

  src_paymentClient = srcUnit 'SRC-003 支付客户端' {
    description 'src/services/payment-client.js'
  }

  // 依赖关系（不是继承）
  src_orderService.src_validator -> src_paymentClient '调用'
}
```

| UML 概念 | LikeC4 表达 |
| --- | --- |
| 类 / 组件 | 元素（按层定义 kind，如 `srcUnit`） |
| 组合 / 包含 | 嵌套（子元素在父元素内） |
| 依赖 / 调用 | 关系 + 标签 |
| 继承 / 泛化 | **无对应**。用 `description` 写明"继承自 X" |

### 代价

继承关系无法用图形表达。这是 LikeC4 的真实短板，不是可以绕过的——**如果项目重度依赖继承体系，需要在 `description` 中显式记录，并在评审时人工核对。**

---

## 五、ER 图与数据模型

### 结论：`store` 或实体元素承载实体，关系承载引用

```c4
model {
  entity_order = store '订单' {
    description '主键 order_id；状态字段引用订单状态机；金额与时间字段由 I 层定义。'
  }
  entity_customer = store '客户' {
    description '主键 customer_id。'
  }
  entity_item = store '商品' {
    description '主键 item_id。'
  }

  entity_order -> entity_customer '归属'
  entity_order -> entity_item '包含明细'
}
```

### 代价

| 项 | 说明 |
| --- | --- |
| **无字段级表达** | 字段写在 `description` 里，图上看不到字段清单 |
| 无基数标注 | 一对多等基数需在关系标签写明「一对多」 |
| 层次靠嵌套 | 实体间的从属可用嵌套表达 |

**字段清单仍应写在 I 层或技术设计中**，模型只表达实体与关系。这个分工要明确，不要试图用图承载字段定义。

---

## 六、信息设计（字段、列表、筛选）

### 结论：界面作为容器，字段作为元素

```c4
model {
  ui_orderList = uiSurface 'UI-002 订单列表' {
    f_orderNo = field '订单号'
    f_amount = field '金额'
    f_status = field '状态'
    f_createdAt = field '创建时间'

    area_filter = uiArea '筛选区' {
      filter_status = field '按状态筛选'
      filter_time = field '按时间筛选'
    }

    area_list = uiArea '列表区' {
      list_default = uiArea '默认排序'
    }

    area_notify = uiArea '通知区' {
      notify_pay = field '支付结果通知'
    }
  }

  f_status -> f_amount '状态影响显示'
  f_orderNo -> f_amount '展示'
}
```

四种状态作为独立元素挂在界面上：

```c4
ui_orderList.state_empty = uiArea '空状态'
ui_orderList.state_loading = uiArea '加载状态'
ui_orderList.state_error = uiArea '错误状态'
ui_orderList.state_forbidden = uiArea '无权限状态'
```

### 代价

字段多时图会变宽。字段超过 12 个时，应把字段清单写在 I 层或 UI 设计文档里，模型只表达**区域划分与关键字段**。

---

## 七、汇总：平替代价表

| 原本诉求 | LikeC4 做法 | 代价 |
| --- | --- | --- |
| 状态机 | 状态即元素，迁移即关系 | 不能自环；非经典外观 |
| 条件分支 | 拆成多个视图 | 视图数量增加 |
| 循环 | 单次迭代视图 + 循环关系视图 | 需人工拆分 |
| 异常 | 独立异常路径视图 | 需人工拆分 |
| 类图 | 嵌套 + 依赖关系 | **继承无对应** |
| ER 图 | store 承载实体 | 无字段级、无基数标注 |
| 泳道 | 嵌套容器 | 非真泳道，不保证竖列 |
| 条件（`opt`） | 拆视图 | 视图数量增加 |
| 用例图 | `actor` 元素 + 关系 | 无 use case 椭圆、无 `<<extend>>` |

**没有一条路径是零代价的。** 这是选择 LikeC4 的真实成本，写在这里而不是假装不存在。

---

## 八、强制规则

1. **不降级**。需要 Mermaid 或 PlantUML 才能表达的图，说明 LikeC4 表达不了，**告知用户代价并让其选择**，不得静默换工具。
2. **代价先说清**。交付时说明哪些图用了平替方案及其代价（如"自反迁移写在 description 中"）。
3. **拆分视图时标题写清条件**。多路径视图的 title 必须包含路径条件，否则读者无从选择。
4. **继承关系必须显式记录**。模型无法表达时，在 `description` 中写明并在交付时列为待人工核对项。
5. **泳道按角色或层划分**，不按步骤划分。
6. **字段清单不塞进模型**。模型表达区域与关键字段，清单写在 I 层或设计文档。
7. **每个新增视图都要跑 `build`**。拆分出的多个视图容易出现只有 `include` 没有消息的问题（validate 发现不了）。
8. **追溯边与依赖边分开**。用 `.trace`（为什么连）与 `.depends`（运行时怎么走）两种 relationship kind，详见 `07-design-chain.md` 第三节。
9. **父子之间不连边**。嵌套已表达包含关系，补边会报 `Invalid parent-child relationship`。
10. **各环元素嵌套在所属 Feature 之下**。归属由嵌套表达，不靠视图层手工画框，详见 `12-design-origin.md` 第四节。
