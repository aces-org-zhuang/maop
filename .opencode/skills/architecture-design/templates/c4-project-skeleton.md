// C4 项目骨架模板
//
// 语法经 likec4 1.58.0 实机 validate 验证通过。
// 语言约定：显示名、描述、关系标签用中文；标识符用英文；技术专有名词保留原文。
// 详见 SKILL.md 的「语言契约」。
//
// 注意：不同版本特性差异很大（尤其 dynamic view 流程控制块），升级后必须重新验证。

/* ---------- likec4.config.ts ---------- */
/*
项目级设计仓不需要此文件。LikeC4 会直接递归扫描 src/**/*.c4。

只有聚合层（同时收纳多个项目仓）才需要它，因为那里必须显式限定
sources，以免各项目的 specification 与顶层元素合并后产生
duplicate kind / duplicate element 冲突。
*/

/* ---------- package.json ---------- */
/*
{
  "name": "design-<project>",
  "private": true,
  "scripts": {
    "dev": "likec4 serve",
    "build": "likec4 build -o ./dist",
    "validate": "likec4 validate",
    "format": "likec4 format",
    "format:check": "likec4 format --check"
  },
  "devDependencies": {
    "likec4": "1.58.0"
  }
}
*/

// 注意：likec4 1.58.x 要求 Node >= 22.22.3（实测 22.22.2 会报 EBADENGINE 并可能崩溃）。
// 保守做法：本地与 CI 都用 Node 22.22.3 以上或 24 LTS。

/* ---------- src/specification.c4 ---------- */

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

  // 部署节点类型必须在这里声明，否则 deployment 块会解析失败
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

/* ---------- src/model/core.c4 ---------- */

model {
  user = actor '用户' {
    description '通过企业微信咨询的终端用户'
  }

  platform = system '业务平台' {
    description '本项目的架构真源'

    web = component '前端页面' {
      description '浏览器端应用'
      style {
        shape browser
      }
    }

    api = component '后端接口' {
      description 'HTTP 入口'
    }

    worker = component '异步任务' {
      description '后台任务处理器'
    }

    jobs = storage '任务队列' {
      style {
        shape queue
      }
    }

    db = storage '主存储'

    web -> api '发起请求'
    api -> db '读写数据'
    api -> jobs '入队任务'
    worker -> jobs '消费任务'
    worker -> db '更新状态'
  }

  user -> web '打开页面'
}

/* ---------- src/views/context.c4 ---------- */

views {
  view index {
    title '系统总览'
    description '顶层系统、参与者与外部平台'
    include *
  }

  view apiDetail of platform.api {
    title '后端接口组成'
    include *
  }

  // 跨文件引用容器内元素必须用 FQN，不能写 api
  view externalDeps {
    title '外部依赖'
    include user, platform
    exclude platform.worker, platform.jobs
  }

  view base {
    include platform
  }

  view detail extends base {
    title '在总览基础上展开细节'
    style user {
      color muted
    }
    include platform.db
  }
}

/* ---------- src/views/use-cases.c4 ---------- */

views {
  // 场景流程图（默认 diagram 变体）
  dynamic view checkout {
    title '下单流程'

    user -> platform.web '提交订单'
    platform.web -> platform.api '创建订单'
    platform.api -> platform.db '写入订单'
    platform.api -> platform.jobs '投递后续任务'
  }

  // 经典时序图。1.58.0 实测：sequence 变体只接受叶子元素之间的连接
  dynamic view jobSequence {
    variant sequence
    title '异步任务生命周期'

    platform.api -> platform.jobs '入队'
    platform.worker -> platform.jobs '出队'
    platform.worker -> platform.db '更新状态'
  }

  // 并发：1.58.0 仅 parallel / par 可用，且不可嵌套
  dynamic view parallelReads {
    variant sequence
    title '并发读取'

    platform.api -> platform.db '加载主数据'
    parallel {
      platform.api -> platform.jobs '查看队列'
      platform.api -> platform.db '加载配置'
    }
  }

  // 固定参与者顺序
  dynamic view orderedActors {
    variant sequence
    title '参与者顺序'

    platform.api -> platform.jobs '入队'
    platform.worker -> platform.db '更新状态'
    include platform.worker, platform.api, platform.db
  }

  // 步骤备注
  dynamic view withNotes {
    title '带备注的步骤'
    platform.api -> platform.jobs '入队' {
      notes '''
        **入口**：请求处理器
        - 重试次数有上限
      '''
    }
  }

  // 下钻
  dynamic view drill {
    title '分层下钻'
    platform.web -> platform.api {
      navigateTo jobSequence
    }
  }

  // 1.58.0 不支持视图文件夹分组（views 'Label'），如需分组需升级版本后重新验证
}

/* ---------- src/deployment/prod.c4 ---------- */

deployment {
  environment prod '生产环境' {
    zone appTier '应用层' {
      vm appVm '应用节点' {
        api = instanceOf platform.api {
          title '接口实例'
        }
        worker = instanceOf platform.worker {
          title '任务实例'
        }
      }
    }

    zone dataTier '数据层' {
      vm dbVm '数据库节点' {
        db = instanceOf platform.db {
          title '主数据库'
        }
      }
    }

    appTier.appVm.api -> dataTier.dbVm.db '读写数据'
  }
}

/* ---------- src/views/deployment-views.c4 ---------- */

views {
  deployment view prodDeployment {
    title '生产部署'
    link https://likec4.dev
    include prod.**
  }
}

注意：
- 部署视图必须写成 `deployment view <name> { include <env>.** }`，单独一个 `views { deployment view ... }` 是对的。
- 部署视图复用逻辑模型的谓词语法，但过滤的是部署节点与实例。
- 部署模型自动继承逻辑模型的关系，无需重复声明；部署特有关系（如主从复制）才在 deployment 里加。
- 部署视图内不使用 global style 与 global predicate，用局部 `style` 规则。
