# POC工单模板 - IPO结构 v1.0

## 基本信息

**工作流名称**: {{WORKFLOW_NAME}}
**工作流类型**: {{WORKFLOW_TYPE}}
**项目目录**: {{PROJECT_CWD}}
**创建时间**: {{CREATE_TIME}}
**负责人**: {{OWNER}}
**工作流文件路径**: {{WORKFLOW_PATH}}
**本工作流是否有效**: true

## 工单目标
**目标**: 基于选型结果，验证技术方案的可行性

## Input（输入）
- **输入来源**: 上游工单（选型工单）
- **输入内容**: 推荐技术方案、实施建议
- **触发条件**: 选型工单完成，需要技术验证

## 执行步骤

### Stage 1: POC功能验证
[ ] Task: POC功能验证
    操作(必选)：
        Step1: 完成POC功能验证代码开发
        Step2: 实现功能可观测web-show

### Stage 2: 创建下游工单
[ ] Task: 验证当前工单是否符合[交付物](##交付物)要求和[目录结构](##目录结构)
    操作(必选)：
        Step1: 验证交付物
        Step2: 验证目录结构
[ ] Task: 创建下游工单
    操作(必选)：
        Step1: 使用ticket-management技能创建下游工单(开发工单)

## Output（输出）
- **输出内容**: 验证结果、可行性报告、改进建议
- **下游工单**: 开发工单
- **触发条件**: 验证完成，可行性确定

## 异常场景和处理方式

| 错误代码 | 异常描述 | 处理动作 | 负责人 |
|----------|----------|----------|--------|
| ERROR:001 | 依赖包安装失败 | 检查网络连接，重试安装，如失败则切换镜像源 | 开发人员 |
| ERROR:002 | POC功能无法实现 | 分析技术限制，记录失败原因，调整方案 | 开发人员 |
| ERROR:003 | 运行环境不兼容 | 检查环境配置，调整运行环境或修改代码 | 开发人员 |
| ERROR:004 | 性能指标不达标 | 记录性能数据，评估是否可优化 | 开发人员 |
| ERROR:005 | 第三方API不可用 | 检查API状态，寻找替代方案 | 开发人员 |

## 决策场景

| 触发条件 | 决策动作 | 预期结果 | 回退方案 |
|----------|----------|----------|----------|
| WHEN: 多个POC方案均可行 | THEN: **权衡复杂度**：选择实现简单、维护成本低的方案 | POC验证高效完成 | 保留备选方案，后续迭代评估 |
| WHEN: POC验证发现技术瓶颈 | THEN: **权衡可行性**：评估瓶颈是否可突破，不可突破则更换方案 | 技术方案切实可行 | 返回选型工单重新评估 |
| WHEN: 验证时间与计划冲突 | THEN: **权衡范围**：优先验证核心功能，非核心功能简化验证 | 核心功能验证完成 | 调整POC计划，分阶段验证 |

## 观测模块

| 检查点 | 观测方法 | 预期状态 | 异常处理 |
|--------|----------|----------|----------|
| OBS_POINT: POC服务启动 | OBS_METHOD: curl -f http://localhost:8080/health | HTTP 200 | 检查服务日志，重启服务 |
| OBS_POINT: 功能可观测页面 | OBS_METHOD: 访问web-show页面检查交互入口 | 页面正常加载 | 检查前端资源，修复加载问题 |
| OBS_POINT: API响应时间 | OBS_METHOD: 测量API接口响应时间 | 响应时间 < 500ms | 分析性能瓶颈，优化实现 |
| OBS_POINT: 日志输出 | OBS_METHOD: 检查应用日志文件 | 日志正常输出，无ERROR | 分析错误日志，修复问题 |

## 交付物

| 交付物 | 格式 | 说明 |
|--------|------|------|
| POC验证代码 | 代码文件 | 验证功能的实现代码 |
| 可行性报告 | Markdown | POC验证结果和可行性分析 |
| 改进建议 | Markdown | 针对验证发现的问题提出改进建议 |
| 软件组件图 | Mermaid | 推荐的POC组合的目标软件组件图 |

## 目录结构
```markdown
.aces/tickets/poc/{{execute_name}}/
├── input/                    # 输入文件目录
│   ├── meta.md                # 上游工单的元信息,包括工单目录和项目信息等等
│   ├──selection/             # 选型工单的结果文件
│   │    ├── phase1-candidates_analysis.md # 候选方案分析
│   │    ├── phase2-recommended_solution.md # 推荐方案
│   │    ├── phase3-software_component_diagram.md # 各POC组合的目标软件组件图(ipd-uml图)
│   │    ├── phase4-end_to_end_diagram.md # 端到端时序图效果(ipd-uml绘图)
│   │    └── phase5-poc-validate.md      # POC验证方案
├── output/                  # 输出文件目录
│   ├── meta.md                # 工单的元信息,包括工单目录和项目信息等等
│   ├── poc_1 <验证项标题>/
│   │    ├── src/                 # 最新实现代码
│   │    └── web-show/            # 页面化展示或调测
│   │       ├── interactive_input.md   # 演示页面可供交互的入口
│   │       ├── common/           # 公共组件
│   │       │    ├── css/          # 公共组件
│   │       │    └── js/            # 页面化展示或调测
│   │       └── web/                # 功能可观测页面展示
│   │           ├── test-xx.html/          # 功能1可观测页面进行人机交互演示效果
│   │           ├── test-xx.html/         # 功能2可观测页面进行人机交互演示效果
│   │           └── .../         # 功能xx可观测页面进行人机交互演示效果
│   ├── poc_2 <验证项标题>/
│   │    ├── ...
│   │    └── ...
│   ├── feasibility_report.md # 可行性报告
│   └── software_component_diagram.md # 推荐的POC组合的目标软件组件图(ipd-uml图)
├── temp/                    # 临时文件目录
│   ├── cache/               # 缓存文件
│   ├── drafts/              # 中间草稿
│   └── logs/                # 处理日志
└── trace.md                 # 执行跟踪文件
```

## 占位符号变量清单

| 变量 | 来源 |
|------|------|
| {{WORKFLOW_NAME}} | 工作流创建时指定,根据上下文自动补全 |
| {{WORKFLOW_TYPE}} | 工作流创建时指定，固定为poc |
| {{CREATE_TIME}} | 工作流创建时自动生成,根据上下文自动补全 |
| {{OWNER}} | 工作流创建时指定负责人,根据上下文自动补全 |
| {{PROJECT_CWD}} | 项目根目录路径,根据上下文自动补全 |
| {{WORKFLOW_PATH}} | 工作流文件完整路径,根据上下文自动补全 |
| {{execute_name}} | 本次执行的工单标题,根据上下文自动补全 |
| {{input_ticket_id}} | 上游工单ID（选型工单）,根据上下文自动补全 |
| {{output_ticket_id}} | 下游工单ID（验收工单）,根据上下文自动补全 |

## 子工作流清单

| 子工作流名称 | 验证是否通过(workflow-creator validate <子工作流路径>) |
|--------|----------|
| 无 | N/A |

## AI能力增强

| 类型 | 名称 | 预期使用 |
|------|------|----------|
| skill | 代码开发 | WHEN 需要实现POC功能 THEN 使用代码开发技能完成功能实现 |
| skill | 功能可观测 | WHEN 需要展示POC效果 THEN 使用功能可观测技能实现web-show |
| skill | ticket-management | WHEN 需要创建下游工单 THEN 使用ticket-management技能创建开发工单 |
| mcp | filesystem | WHEN 需要读写POC文件 THEN 使用filesystem MCP操作文件系统 |
| mcp | git | WHEN 需要提交POC代码 THEN 使用git MCP提交代码变更 |

### 核心原则

#### 1. 精简高效原则
- **信息压缩**：优先使用Markdown Table和IPD图表
- **聚焦做什么** When-How 的结构化表达
- **即刻标记**: 完成即刻对任务进行标注[x]

### 工作流命名标准

| 领域 | 类型 | 说明 | 示例 |
|------|------|------|------|
| user | softinstall/setup | 个人用户场景 | user-softinstall-vscode |
| ipd | coding/review/ops/data/sec | 集成产品开发 | ipd-coding-webui |
| aigc | ppt/xlsx/doc | AIGC内容生成 | aigc-ppt-report |
| aitools | skills/agent | AI能力增强 | aitools-skills-creator |

---

*模板版本: v1.0 (IPO结构)*
*更新时间: 2026-04-01*
*设计模式: IPO (Input->Process->Output)*
*依赖工单: 选型工单 (selection)*
