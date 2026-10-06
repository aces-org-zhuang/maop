# SOP 02 - 多文件组织与 FQN 规则

## Goal

在多文件 `.c4` 项目中正确共享元素、扩展模型，并避免跨文件引用导致的高频校验失败。

## When Required

设计仓包含多个 `.c4` 文件、需要复用共享元素、或需要把某元素扩展出更多子元素时。

## 最高频失败原因

> **short name 不跨文件继承容器作用域。**

在 `views/` 中引用 `model/` 里定义的 `saas.api`，不能只写 `api`，必须写完整限定名 `saas.api`。

这是 AI 生成 LikeC4 代码后 `validate` 失败的首要原因。任何跨文件引用都必须按本文件的 FQN 规则处理。

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
    include saas        // 合法：import 后顶层 short name 可用
  }
}
```

要点：

- `import { name } from '<相对路径>'`。
- 顶层元素 import 后可用 short name。
- **但进入容器内部后，short name 仍然不继承**：

```c4
import { saas } from '../model/shared.c4'

views {
  view bad {
    include api        // ⛔ 错误：api 是 saas.api，不是顶层元素
  }

  view good {
    include saas.api   // ✅ 正确：使用 FQN
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

- `extend <element> { ... }` 往已有元素上追加子元素。
- `extend a -> b { }` 往已有关系上追加 metadata。
- 重复键在 metadata 中会变成数组，不是覆盖。
- 追加子元素必须有明确 owner 决策，避免两个文件同时往同一元素加同名子元素。

## 视图分组：用文件而非文件夹

**1.58.0 实测不支持视图文件夹分组。** 官方文档中的 `views 'Label' { ... }` 在当前版本解析失败（`Line 1: Expecting '}' but found 'views'`）。

```c4
# ⛔ 1.58.0 不可用
views {
  views 'Use Cases' {
    dynamic view checkout { ... }
  }
}
```

替代方案：**按用途拆分文件**，用文件名表达分组。

```text
views/
  context.c4           # 系统级静态视图
  use-cases.c4         # 动态视图（场景流程）
  sequences.c4         # 时序图
  deployment-views.c4  # deployment view
```

其他要点：

- **所有块都可跨文件合并**，包括 `model`、`views`、`specification`、`deployment`。
- **视图名全局唯一**，不同文件间也不能重名，否则报 `Duplicate view`。

## 组织建议

```text
src/
  specification.c4
  model/
    core.c4            # 核心共享元素
    domain-a.c4
    domain-b.c4
  views/
    context.c4         # 静态视图
    use-cases.c4       # 动态视图
    sequences.c4       # 时序图
  deployment/
    prod.c4            # 部署模型
```

- `model/` 定义什么，图就画什么；不要在 `views/` 里新建模型元素冒充模型事实。
- 共享基类放独立文件，供各域 `import`。
- 图按用途分文件，而不是按页面分文件。
- 部署视图（`deployment view`）写在 `views/` 下的文件里，与部署模型（`deployment` 块）分开。

## 校验

```bash
likec4 validate
```

多文件项目尤其必须跑：单文件能过的写法在合并后可能因 FQN 冲突或重复定义失败。

## 常见失败模式

- 跨文件用 short name 引用容器内元素 → 必须 FQN。
- 两个文件各自 `extend` 同一元素并创建同名子元素 → 冲突。
- 把模型事实藏在 `views/` 里 → 架构真源错误，后续无法被查询。
- 文件切分按功能而非按模型/视图职责，导致 model 与 view 混杂。
- 未跑 `validate` 就交付多文件模型。
