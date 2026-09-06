# 调研工单模板 - IPO结构 v1.0

## 基本信息

**工作流名称**: {{WORKFLOW_NAME}}
**工作流类型**: {{WORKFLOW_TYPE}}
**项目目录**: {{PROJECT_CWD}}
**创建时间**: {{CREATE_TIME}}
**负责人**: {{OWNER}}
**工作流文件路径**: {{WORKFLOW_PATH}}
**本工作流是否有效**: true

## 工单目标
**目标**: 通过分析外部知识文章，提炼技术趋势和选型方向

## Input（输入）
- **输入来源**: 用户输入或系统需求
- **输入内容**: 搜索关键词、技术方向
- **触发条件**: 需要技术趋势分析

## 执行步骤

### Stage 1: 文章收集
[ ] Task: 文章收集
    操作(必选)：
        Step1: 使用tech-link-finder技能完成技术文章搜索
        Step2: 使用文章整理技能完成文章资源整理

### Stage 2: 内容分析
[ ] Task: 内容分析
    操作(必选)：
        Step1: 使用weixin-article技能完成文章内容分析
        Step2: 使用关键信息技能完成关键信息提炼

### Stage 3: 创建下游工单
[ ] Task: 验证当前工单是否符合[交付物](##交付物)要求和[目录结构](##目录结构)
    操作(必选)：
        Step1: 验证交付物
        Step2: 验证目录结构
[ ] Task: 创建下游工单
    操作(必选)：
        Step1: 使用ticket-management技能创建下游工单(选型工单selection)

## Output（输出）
- **输出内容**: 技术趋势分析、选型方向建议、文章摘要
- **下游工单**: 选型工单
- **触发条件**: 分析完成，趋势确定

## 异常场景和处理方式

| 错误代码 | 异常描述 | 处理动作 | 负责人 |
|----------|----------|----------|--------|
| ERROR:001 | 搜索关键词为空 | 使用自动模式生成搜索关键词 | 分析人员 |
| ERROR:002 | 文章链接无法访问 | 检查网络状态，尝试其他链接源 | 分析人员 |
| ERROR:003 | 文章内容提取失败 | 检查反爬机制，切换提取策略 | 分析人员 |
| ERROR:004 | 分析结果质量低 | 调整分析参数，重新执行分析 | 分析人员 |
| ERROR:005 | 技术趋势不明确 | 扩大搜索范围，增加分析样本 | 分析人员 |

## 决策场景

| 触发条件 | 决策动作 | 预期结果 | 回退方案 |
|----------|----------|----------|----------|
| WHEN: 多个技术方向可选 | THEN: **权衡成熟度**：选择技术成熟度高、社区活跃的方向 | 选型方向明确可行 | 保留备选方向，持续跟踪 |
| WHEN: 文章信息量不足 | THEN: **权衡深度**：扩大搜索范围，增加分析样本量 | 分析结果充分可靠 | 使用自动模式补充搜索 |
| WHEN: 技术趋势存在分歧 | THEN: **权衡共识**：以主流观点和头部企业实践为准 | 选型方向具有行业共识 | 组织专家评审，达成共识 |

## 观测模块

| 检查点 | 观测方法 | 预期状态 | 异常处理 |
|--------|----------|----------|----------|
| OBS_POINT: 文章收集数量 | OBS_METHOD: 检查tech-link.md中的文章数量 | 文章数量 >= 10篇 | 扩大搜索范围，增加关键词 |
| OBS_POINT: 内容提取成功率 | OBS_METHOD: 统计成功提取的文章比例 | 成功率 >= 80% | 检查反爬策略，切换提取方法 |
| OBS_POINT: 分析结果完整性 | OBS_METHOD: 检查输出文件是否完整生成 | 所有输出文件存在 | 重新执行分析流程 |

## 交付物

| 交付物 | 格式 | 说明 |
|--------|------|------|
| 技术文章清单 | Markdown | tech-link-finder搜索到的文章和链接 |
| 文章分析报告 | Markdown | weixin-article分析的文章内容摘要 |
| 技术趋势分析 | Markdown | 技术趋势和选型方向建议 |
| 选型方向建议 | Markdown | 基于分析结果的选型方向建议 |

## 目录结构
```markdown
.aces/tickets/research/{{execute_name}}/
├── input/                    # 输入文件目录
│   ├── meta.md                # 上游工单的元信息,包括工单目录和项目信息等等
│   └── search_keywords.md    # 搜索关键词(允许零输入，因为技能支持自动模式)
├── output/                   # 输出文件目录
│   ├── meta.md                # 工单的元信息,包括工单目录和项目信息等等
│   ├── tech-link.md       # 技能tech-link-finder 的文章和链接
│   └── github-selection/           # 技能github-selection 的所有outputs文件
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
| {{WORKFLOW_TYPE}} | 工作流创建时指定，固定为research |
| {{CREATE_TIME}} | 工作流创建时自动生成,根据上下文自动补全 |
| {{OWNER}} | 工作流创建时指定负责人,根据上下文自动补全 |
| {{PROJECT_CWD}} | 项目根目录路径,根据上下文自动补全 |
| {{WORKFLOW_PATH}} | 工作流文件完整路径,根据上下文自动补全 |
| {{execute_name}} | 本次执行的工单标题,根据上下文自动补全 |
| {{input_ticket_id}} | 上游工单ID,根据上下文自动补全 |
| {{output_ticket_id}} | 下游工单ID（选型工单selection）,根据上下文自动补全 |

## 子工作流清单

| 子工作流名称 | 验证是否通过(workflow-creator validate <子工作流路径>) |
|--------|----------|
| 无 | N/A |

## AI能力增强

| 类型 | 名称 | 预期使用 |
|------|------|----------|
| skill | tech-link-finder | WHEN 需要搜索技术文章 THEN 使用tech-link-finder技能完成文章搜索 |
| skill | weixin-article | WHEN 需要分析微信文章 THEN 使用weixin-article技能提取和分析内容 |
| skill | ticket-management | WHEN 需要创建下游工单 THEN 使用ticket-management技能创建选型工单 |
| mcp | filesystem | WHEN 需要读写分析文件 THEN 使用filesystem MCP操作文件系统 |
| mcp | memory | WHEN 需要检索历史分析 THEN 使用memory MCP检索相关记忆 |

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
*依赖工单: 无*
单: 无*
