# SOP 02 - 多文件组织与 FQN 规则

## Goal

在多文件 `.c4` 项目中正确共享元素、扩展模型，并避免跨文件引用导致的高频校验失败。

## When Required

**主要是 SRC 源码层。** 源码层元素天然嵌套（系统 → 容器 → 组件 → 类），跨文件引用嵌套元素时必须用 FQN，这是本 SOP 的核心场景。

US / F / NF / I / UI 五层通常是扁平设计，跨文件引用顶层元素用 short name 即可，不需要 FQN。详见下方「FQN 规则的真正适用范围」。

## FQN 规则的真正适用范围（1.58.0 实测）

**short name 不跨文件继承容器作用域**——但这只针对**嵌套元素**。

| 场景 | short name | FQN | 说明 |
| --- | --- | --- | --- |
| 跨文件引用**顶层**元素 | ✅ 可用 | 可用 | `us_a` 直接写 |
| 跨文件引用**嵌套**元素 | ❌ 解析失败 | ✅ 必须 | `nested` 不行，须写 `sys_a.nested` |
| 跨文件关系指向顶层 | ✅ 可用 | 可用 | `us_a -> sys_a` |
| 跨文件关系指向嵌套 | ❌ 解析失败 | ✅ 必须 | `us_a -> sys_a.nested` |
| `import` 后引用顶层 | ✅ 可用 | 可用 | import 后顶层 short name 生效 |
| `import` 后引用容器内 | ❌ 解析失败 | ✅ 必须 | short name 不因 import 而继承 |

解析失败的典型报错：

```text
Line 3: Could not resolve reference to Referenceable named 'nested'.
Line 3: Validation failed: Element "nested" is not resolved
```

**因此 FQN 的必要性来自嵌套结构，不来自「跨文件」这件事本身。** 把规则写成「跨文件一律用 FQN」是过度要求，会让扁平设计被迫写冗长全名，也掩盖了真正的规则。

## 共享元素：import

```c4
// shared.c4
model {
  saas = system 'SaaS' {
    api = component 'API'
  }
}
```

```c4
// views/context.c4
import { saas } from '../model/shared.c4'

views {
  view ctx {
    include saas        // 合法：顶层元素，import 后 short name 可用
  }
}
```

要点：

- `import { name } from '<相对路径>'`
- 顶层元素 import 后可用 short name
- **进入容器内部后 short name 仍不继承**：

```c4
import { saas } from '../model/shared.c4'

views {
  view bad {
    include api        // ⛔ 错误：api 是 saas.api，不是顶层元素
  }

  view good {
    include saas.api   // ✅ 正确：嵌套元素必须 FQN
  }
}
```

## 扩展元素与关系：extend

```c4
// extend.c4
extend saas {
  queue = component 'Message Queue' {
    style { shape queue }
  }

  worker = component 'Async Worker'
}

extend saas.api -> saas.db {
  metadata {
    note 'Batch write path'
  }
}
```

规则：

- `extend <element> { ... }` 往已有元素上追加子元素
- `extend a -> b { }` 往已有关系上追加 metadata
- 重复键在 metadata 中会变成数组，不是覆盖
- 追加子元素必须有明确 owner 决策，避免两个文件同时往同一元素加同名子元素

## 视图分组：用文件而非文件夹

**1.58.0 实测不支持视图文件夹分组。** 官方文档中的 `views 'Label' { ... }` 在当前版本解析失败（`Line 1: Expecting '}' but found 'views'`）。

替代方案：**按用途拆分文件**，用文件名表达分组。分组维度应对应七层设计链的层，见 `07-seven-layer-design.md`。

```text
views/
  chain-us.c4           # US 层视图
  chain-framework.c4    # F / NF 层视图
  chain-business.c4     # I + UI 层视图（排除 SRC）
  chain-source.c4       # SRC 层视图
  sequences.c4          # 时序视图
  deployment-views.c4   # deployment view
```

其他要点：

- **所有块都可跨文件合并**，包括 `model`、`views`、`specification`、`deployment`
- **视图名全局唯一**，不同文件间也不能重名，否则报 `Duplicate view`

## 组织建议：按层而非按技术域

在七层设计链项目里，**先按层分文件，层内再按需拆分**。这比传统的「按技术域拆」更贴合设计链的可追溯要求。

```text
src/
  specification.c4
  model/
    us.c4               # US 层
    framework.c4        # F + NF 层
    implementation.c4   # I 层
    ui.c4               # UI 层
    src.c4              # SRC 层（可再按子系统拆）
      checkout.c4
      payment.c4
  views/
    chain-overview.c4
    chain-business.c4
    chain-source.c4
    sequences.c4
  deployment/
    prod.c4
```

要点：

- `model/` 定义什么，图就画什么；不要在 `views/` 里新建模型元素冒充模型事实
- **只有 SRC 层会继续细分**（子系统、模块、类），也只有它需要 FQN
- 上五层保持单文件或少量文件，避免过度拆分
- 图按层分文件，文件名体现层归属
- 部署视图写在 `views/` 下的文件里，与部署模型（`deployment` 块）分开

## 校验

```bash
likec4 validate
likec4 build
```

多文件项目尤其必须跑：单文件能过的写法在合并后可能因 FQN 冲突或重复定义失败。`build` 不可省略——dynamic view 的布局错误只有 `build` 才能发现。

## 常见失败模式

- **跨文件引用嵌套元素却用 short name** → 必须 FQN。这是最高频失败
- **误以为所有跨文件引用都要 FQN** → 顶层元素用 short name 即可，不必强行写全名
- 两个文件各自 `extend` 同一元素并创建同名子元素 → 冲突
- 把模型事实藏在 `views/` 里 → 架构真源错误，后续无法被查询
- 文件切分按技术域而非按设计层 → 追溯链断裂，跨层引用时才暴露 FQN 问题
- 未跑 `validate` / `build` 就交付多文件模型
