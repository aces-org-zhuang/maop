# 选型工单模板 - IPO结构 v1.0

## 基本信息

**工作流名称**: {{WORKFLOW_NAME}}
**工作流类型**: {{WORKFLOW_TYPE}}
**项目目录**: {{PROJECT_CWD}}
**创建时间**: {{CREATE_TIME}}
**负责人**: {{OWNER}}
**工作流文件路径**: {{WORKFLOW_PATH}}
**本工作流是否有效**: true

## 工单目标
**目标**: 基于立项分析结果，评估和选择最适合的技术方案

## Input（输入）
- **输入来源**: 上游工单（调研工单）
- **输入内容**: 主流观点和文章摘要
- **触发条件**: 调研工单完成，需要技术选型

## 执行步骤

### Stage 1: 选型分析
[ ] Task: 选型分析
    操作(必选)：
        Step1: 使用github-selection技能完成Github选型和POC方案

### Stage 2: 创建下游工单
[ ] Task: 验证当前工单是否符合[交付物](##交付物)要求和[目录结构](##目录结构)
    操作(必选)：
        Step1: 验证交付物
        Step2: 验证目录结构
[ ] Task: 创建下游工单
    操作(必选)：
        Step1: 使用ticket-management技能创建下游工单(POC工单)

## Output（输出）
- **输出内容**: 候选方案分析、推荐方案、实施建议
- **下游工单**: POC工单
- **触发条件**: 选型完成，方案确定

## 异常场景和处理方式

| 错误代码 | 异常描述 | 处理动作 | 负责人 |
|----------|----------|----------|--------|
| ERROR:001 | Github搜索失败 | 检查网络连接，重试搜索或切换搜索策略 | 分析人员 |
| ERROR:002 | 候选方案不足 | 扩大搜索范围，增加候选方案数量 | 分析人员 |
| ERROR:003 | 评估标准不明确 | 重新定义评估维度，完善评估标准 | 分析人员 |
| ERROR:004 | 推荐方案存在风险 | 记录风险点，提供备选方案 | 分析人员 |
| ERROR:005 | 开源协议不兼容 | 检查开源协议，选择兼容的方案 | 法务人员 |

## 决策场景

| 触发条件 | 决策动作 | 预期结果 | 回退方案 |
|----------|----------|----------|----------|
| WHEN: 多个候选方案评分接近 | THEN: **权衡生态**：选择社区活跃度高、文档完善的方案 | 选型结果具有生态优势 | 保留备选方案，POC阶段验证 |
| WHEN: 推荐方案存在已知缺陷 | THEN: **权衡风险**：评估缺陷影响范围，选择影响最小的方案 | 选型风险可控 | 选择次优方案，规避已知缺陷 |
| WHEN: 商业方案与开源方案冲突 | THEN: **权衡成本**：综合评估TCO，选择性价比最优方案 | 选型结果经济合理 | 采用混合方案，核心功能开源 |

## 观测模块

| 检查点 | 观测方法 | 预期状态 | 异常处理 |
|--------|----------|----------|----------|
| OBS_POINT: 候选方案数量 | OBS_METHOD: 检查phase1-candidates_analysis.md | 候选方案 >= 3个 | 扩大搜索范围 |
| OBS_POINT: 评估维度完整性 | OBS_METHOD: 检查评估报告中的维度覆盖 | 评估维度覆盖全面 | 补充缺失评估维度 |
| OBS_POINT: 推荐方案明确性 | OBS_METHOD: 检查phase2-recommended_solution.md | 推荐方案明确唯一 | 重新评估候选方案 |

## 交付物

| 交付物 | 格式 | 说明 |
|--------|------|------|
| 候选方案分析 | Markdown | phase1-candidates_analysis.md |
| 推荐方案 | Markdown | phase2-recommended_solution.md |
| 软件组件图 | Mermaid | phase3-software_component_diagram.md |
| 端到端时序图 | Mermaid | phase4-end_to_end_diagram.md |
| POC验证方案 | Markdown | phase5-poc-validate.md |

## 目录结构
```markdown
.aces/tickets/selection/{{execute_name}}/
├── input/                    # 输入文件目录
│   ├── meta.md                # 上游工单的元信息,包括工单目录和项目信息等等
│   └── requirements.md        # 选型要求
├── output/                  # 输出文件目录(和技能github-selection技能同步)
│   ├── meta.md                # 工单的元信息,包括工单目录和项目信息等等
│   ├── phase1-candidates_analysis.md # 候选方案分析
│   ├── phase2-recommended_solution.md # 推荐方案
│   ├── phase3-software_component_diagram.md # 各POC组合的目标软件组件图(ipd-uml图)
│   ├── phase4-end_to_end_diagram.md # 端到端时序图效果(ipd-uml绘图)
│   └── phase5-poc-validate.md      # POC验证方案
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
| {{WORKFLOW_TYPE}} | 工作流创建时指定，固定为selection |
| {{CREATE_TIME}} | 工作流创建时自动生成,根据上下文自动补全 |
| {{OWNER}} | 工作流创建时指定负责人,根据上下文自动补全 |
| {{PROJECT_CWD}} | 项目根目录路径,根据上下文自动补全 |
| {{WORKFLOW_PATH}} | 工作流文件完整路径,根据上下文自动补全 |
| {{execute_name}} | 本次执行的工单标题,根据上下文自动补全 |
| {{input_ticket_id}} | 上游工单ID（调研工单）,根据上下文自动补全 |
| {{output_ticket_id}} | 下游工单ID（POC工单）,根据上下文自动补全 |

## 子工作流清单

| 子工作流名称 | 验证是否通过(workflow-creator validate <子工作流路径>) |
|--------|----------|
| 无 | N/A |

## AI能力增强

| 类型 | 名称 | 预期使用 |
|------|------|----------|
| skill | github-selection | WHEN 需要技术选型 THEN 使用github-selection技能完成Github项目评估和推荐 |
| skill | ticket-management | WHEN 需要创建下游工单 THEN 使用ticket-management技能创建POC工单 |
| skill | ipd-uml | WHEN 需要绘制架构图 THEN 使用ipd-uml技能生成组件图和时序图 |
| mcp | filesystem | WHEN 需要读写选型文件 THEN 使用filesystem MCP操作文件系统 |
| mcp | memory | WHEN 需要检索历史选型 THEN 使用memory MCP检索相关记忆 |

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
*依赖工单: 调研工单 (research)*
