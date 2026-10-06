// C4 项目骨架模板
// 语法经 likec4 1.58.0 实机 validate 验证通过。
// 注意：不同版本特性差异很大（尤其 dynamic view 流程控制块），升级后必须重新验证。

/* ---------- likec4.config.ts ---------- */
/*
import { defineConfig } from 'likec4';

export default defineConfig({
  projects: {
    '<project-id>': {
      sources: ['src/**/*.c4'],
    },
  },
});
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
  user = actor 'User' {
    description 'Primary end user'
  }

  platform = system 'Platform' {
    description 'Single source of architectural truth'

    web = component 'Web Frontend' {
      description 'Browser application'
      style {
        shape browser
      }
    }

    api = component 'Backend API' {
      description 'HTTP entry point'
    }

    worker = component 'Async Worker' {
      description 'Background job processor'
    }

    jobs = storage 'Job Queue' {
      style {
        shape queue
      }
    }

    db = storage 'Primary Store'

    web -> api 'requests via HTTPS'
    api -> db 'reads and writes'
    api -> jobs 'enqueues jobs'
    worker -> jobs 'consumes jobs'
    worker -> db 'updates state'
  }

  user -> web 'opens in browser'
}

/* ---------- src/views/context.c4 ---------- */

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

  // 跨文件引用容器内元素必须用 FQN，不能写 api
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
}

/* ---------- src/views/use-cases.c4 ---------- */

views {
  // 场景流程图（默认 diagram 变体）
  dynamic view checkout {
    title 'Checkout Flow'

    user -> platform.web 'submits order'
    platform.web -> platform.api 'POST /checkout'
    platform.api -> platform.db 'writes order'
    platform.api -> platform.jobs 'enqueue followup'
  }

  // 经典时序图。1.58.0 实测：sequence 变体只接受叶子元素之间的连接
  dynamic view asyncJobSequence {
    variant sequence
    title 'Async Job Lifecycle'

    platform.api -> platform.jobs 'enqueue'
    platform.worker -> platform.jobs 'dequeue'
    platform.worker -> platform.db 'update'
  }

  // 并发：1.58.0 仅 parallel / par 可用，且不可嵌套
  dynamic view seqParallel {
    variant sequence
    title 'Concurrent Reads'

    platform.api -> platform.db 'load profile'
    parallel {
      platform.api -> platform.jobs 'peek queue'
      platform.api -> platform.db 'load settings'
    }
  }

  // 固定参与者顺序
  dynamic view seqOrdered {
    variant sequence
    title 'Actor Order'

    platform.api -> platform.jobs 'enqueue'
    platform.worker -> platform.db 'update'
    include platform.worker, platform.api, platform.db
  }

  // 步骤备注
  dynamic view withNotes {
    title 'Notes Example'
    platform.api -> platform.jobs 'enqueue' {
      notes '''
        **Entry point**: request handler
        - bounded retries
      '''
    }
  }

  // 下钻
  dynamic view drill {
    title 'Drill Down'
    platform.web -> platform.api {
      navigateTo asyncJobSequence
    }
  }

  // 1.58.0 不支持视图文件夹分组（views 'Label'）；如需分组请升级版本后重新验证
}

/* ---------- src/deployment/prod.c4 ---------- */

deployment {
  environment prod 'Production' {
    zone appTier 'Application Tier' {
      vm appVm 'app-1' {
        api = instanceOf platform.api {
          title 'API Instance'
        }
        worker = instanceOf platform.worker {
          title 'Worker Instance'
        }
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

/* ---------- src/views/deployment-views.c4 ---------- */

views {
  deployment view prodDeployment {
    title 'Production Deployment'
    link https://likec4.dev
    include prod.**
  }
}

注意：
- 部署视图必须写成 `deployment view <name> { include <env>.** }`，单独一个 `views { deployment view ... }` 是对的。
- 部署视图复用逻辑模型的谓词语法，但过滤的是部署节点与实例。
- 部署模型自动继承逻辑模型的关系，无需重复声明；部署特有关系（如复制）才在 deployment 里加。
