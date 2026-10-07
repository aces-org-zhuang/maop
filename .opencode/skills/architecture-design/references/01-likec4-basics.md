# SOP 01 - LikeC4 DSL 基础

## Goal

掌握写 `specification`、`model`、静态视图和部署视图所需的最小完整 DSL 子集，保证模型可被 `likec4 validate` 通过。

## When Required

任何新建架构模型、扩展模型或新增静态视图时读取本文件。

## 语言约定

**默认中文**。架构图是给人评审的，面向人的文本一律用中文；标识符与技术专有名词除外。完整规则见 `SKILL.md` 的「语言契约」。

```c4
model {
  user = actor '用户' {                        // 显示名：中文
    description '通过企业微信咨询的终端用户'    // 描述：中文
  }
  beauty = system '美妆客服服务' {
    api = component '后端接口'                  // 显示名：中文
  }
  user -> beauty '打开页面'                     // 关系标签：中文
}
```

要点：

- 标识符（`user`、`answerOrchestrator`、`answerPath`）用英文——它决定导出文件名与分享 URL。
- `RAGFlow`、`LLM Wiki`、`Node.js`、`HTTP`、`JSON`、文件路径、端口保留原文。
- 中文标识符（视图名、元素名）不影响编译，已在 likec4 1.58.0 实机验证。

## 前置条件

- **Node.js >= 22.22.3**。likec4 1.58.x 实测在 22.22.2 下报 `EBADENGINE` 并可能因缺失依赖崩溃。低于此版本先升级 Node，不要降级工具。
- 工作区存在 `likec4.config.ts`，或按 `references/04-project-integration.md` 建立。

## 版本敏感性（重要）

LikeC4 的 DSL 与特性**跨版本差异较大**。本文件语法经 **likec4 1.58.0 实机验证**。

- 官方文档描述的是**最新版本**，可能包含当前锁定版本尚不支持的特性（例：`opt` `loop` `alt` `try` `break` 在 1.58.0 全部不可用，详见 `references/03-dynamic-views.md`）。
- 升级 LikeC4 版本后，**必须重新跑 `likec4 validate` 验证本文件与模板中的示例**，不要假设旧示例继续有效。
- 报告能力时必须声明所用版本。

## 文件结构

```text
src/
  specification.c4      # 元素类型、部署节点类型与全局样式
  model/
    <domain>.c4         # 按领域拆分模型
  views/
    context.c4          # 系统级视图
    use-cases.c4        # 动态视图
    deployment-views.c4 # deployment view 放在 views 块内
  deployment/
    <env>.c4            # 部署模型
```

扩展名 `.c4` 或 `.likec4`。CLI 递归搜索这两种文件；同名视图会报 `Duplicate view`。

## specification

```c4
specification {
  element actor {
    style {
      shape person
    }
  }
  element system
  element component
  element storage {
    style {
      shape storage
    }
  }

  deploymentNode environment {
    notation 'Environment'
    style {
      color gray
    }
  }
  deploymentNode zone {
    notation 'Zone'
  }
  deploymentNode vm {
    notation 'VM'
  }
}
```

### shape 合法值（实测枚举，务必遵守）

```text
rectangle（默认）  component  storage  cylinder
browser  mobile  person  queue  bucket  document
```

**不存在的值**（写错直接解析失败）：`database`、`cloud`、`disk`。

注意区分两个概念：`element database` 是你自定义的**元素类型名**，而 `shape database` 是**图形值**，两者互不相通。数据库应写 `shape cylinder` 或 `shape storage`。

### color 合法值

```text
primary（默认）  secondary  muted  amber  gray
green  indigo  red  sky  slate
```

**不存在**：`teal`、`d2`。

### 其他要点

- 元素类型可任意命名（`service`、`queue`、`db` 均可）。
- 常用属性：`notation`（图例标注）、`technology`、`description`、`style`。
- **部署节点类型必须用 `deploymentNode` 声明**，否则 `deployment` 块解析失败。
- 若需要关系类型，`relationship` 块的样式语法与其他 style 块不同，**1.58.0 实测未能直接写 `style { lineStyle dashed }`**；异步关系优先通过视图层表达，不要在 specification 里硬写。

## model

```c4
model {
  user = actor 'User' {
    description 'Primary end user'
  }

  platform = system 'Platform' {
    description 'Single source of architectural truth'

    web = component 'Web Frontend' {
      style {
        shape browser
      }
    }

    api = component 'Backend API'
    db = storage 'Primary Store'

    web -> api 'requests via HTTPS'
    api -> db 'reads and writes'
  }

  user -> web 'opens in browser'
}
```

规则：

- 标识符用小驼峰或下划线；显示名用单引号，可含中文与空格。
- 嵌套即层级：`platform` 是 system，`platform.api` 是 component。
- `description` 支持 Markdown，三引号写多行。
- 允许自调用 `api -> api 'process'`。
- **关系上不要挂 `style { }` 块**（1.58.0 实测报错）。关系样式请在视图层用局部 `style` 规则表达。

## 静态视图

```c4
views {
  view index {
    title 'System Overview'
    description 'Top-level systems and external actors'
    include *
  }

  view apiDetail of platform.api {
    title 'Backend API Components'
    include *
  }

  view crossSystem {
    title 'External Dependencies'
    include user, platform
    exclude platform.worker, platform.jobs
  }

  view base {
    include platform
  }

  view detail extends base {
    title 'Same as base, with more detail'
    style user {
      color muted
    }
    include platform.db
  }

  view tagged {
    #next, #epic-12
    title 'Tagged View'
    include *
  }

  view linked {
    title 'Linked'
    link https://likec4.dev 'Homepage'
    include *
  }

  view overridden {
    include platform, user
    include user with {
      color amber
      title 'Client'
    }
  }
}
```

要点：

- `view of <element>` 获得作用域，其内可用 short name。
- **无 `of` 的视图内引用容器内元素必须用 FQN**（见 `references/02-multifile-and-fqn.md`）。
- 视图属性（`title`、`description`、`tags`、`link`）**必须写在任何 predicate 之前**，否则解析失败。
- `include` / `exclude` 支持通配：`*`、`platform.*`、`* -> platform`。
- `include x with { ... }` 可按视图覆盖属性。
- 具名视图是导出文件名与分享 URL 的一部分，必须命名；未命名视图无法被 `navigateTo` 引用。
- **视图名全局唯一**，重名报 `Duplicate view`。

### 视图继承

祖先的 predicate 与 style 先应用，被继承者后应用；作用域也被继承。

## 部署模型与部署视图

部署是独立的一层，语法与逻辑模型不同。

```c4
deployment {
  environment prod 'Production' {
    zone appTier 'Application Tier' {
      vm appVm 'app-1' {
        api = instanceOf platform.api {
          title 'API Instance'
        }
        worker = instanceOf platform.worker
      }
    }

    zone dataTier 'Data Tier' {
      vm dbVm 'db-1' {
        db = instanceOf platform.db {
          title 'Primary Database'
        }
      }
    }

    appTier.appVm.api -> dataTier.dbVm.db 'reads and writes'
  }
}
```

```c4
views {
  deployment view prodDeployment {
    title 'Production Deployment'
    include prod.**
  }
}
```

要点：

- **运算符是 `instanceOf`（驼峰），不是 `instance of`。**
- 节点种类来自 specification 的 `deploymentNode` 声明（`environment` / `zone` / `vm` 等可自定义）。
- 节点可写属性：`title`、`#tag`、`technology`、`description`（支持 Markdown）、`link`、`style`。
- **命名实例** `api = instanceOf platform.api` 用于同一元素有多个副本；单实例可写匿名 `instanceOf platform.worker`。
- 部署模型**自动继承逻辑模型的关系**，无需重复声明；部署特有关系（如主从复制）才在 `deployment` 里追加。
- `instanceOf` 可部署到任意层级，不限叶子节点（共享数据库常用）。
- 部署视图复用逻辑模型的谓词语法，但过滤的是部署节点与实例。
- 标签语义：实例标签 = 逻辑标签 + 部署标签；子节点标签不自动继承。
- 部署视图内**不要使用 global style / global predicate**，用局部 `style` 规则。

## 样式作用域

按优先级选择最小作用面：

```c4
// 1. 类型级（同类统一）
specification {
  element actor { style { shape person } }
}

// 2. 元素内联
db = storage 'Store' { style { shape cylinder } }

// 3. 视图内覆盖
view v of platform {
  include *
  style platform.db { color muted }
}
```

## 校验

```bash
likec4 validate        # 语法 + 重复视图 + 引用解析 + 布局漂移
likec4 format --check  # 格式检查；未格式化时退出码 1
likec4 format          # 就地格式化
```

`validate` 通过时输出 `✓ Valid (N files)`，退出码 0。提交前两项都要过。

## 常见失败模式（均为实测确认）

| 现象 | 根因 | 修正 |
| --- | --- | --- |
| `Could not resolve reference to ElementKind named 'database'` | `shape database` 不是合法值 | 改 `shape cylinder` 或 `shape storage` |
| 关系后 `Expecting token of type '}' but found 'style'` | 关系上不能挂 `style` 块 | 移视图层局部 style |
| `Duplicate view 'index'` | 视图名全局重复 | 改名或删除重复定义 |
| 视图属性后解析失败 | 属性未前置 | title/description/tags/link 写在 predicate 前 |
| 跨文件容器元素找不到 | 用了 short name | 改 FQN |
| deployment 块 `Line 1` 解析失败 | 用了 `instance of` | 改 `instanceOf` |
| EBADENGINE / ERR_MODULE_NOT_FOUND | Node 版本低于要求 | 升级到 >= 22.22.3 |
