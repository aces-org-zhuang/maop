# 工单类型规格说明

## 标准工单类型

### 📝 research (调研工单)
- **用途**: 技术文章分析、趋势提取、立项方向
- **目录**: `.aces/tickets/research/`
- **输入**: `input/requirements.md`
- **输出**: `output/trend-analysis.md`, `output/recommendations.md`
- **占位符**: `{{input_ticket_id}}`, `{{last_updated}}`
- **验证**: `ticket-cli validate .aces/tickets/research/工单ID`

### 🔍 selection (选型工单)
- **用途**: 技术选型、方案推荐、可行性分析
- **目录**: `.aces/tickets/selections/`
- **输入**: `input/tech-requirements.md`
- **输出**: `output/tech-comparison.md`, `output/selection-report.md`
- **占位符**: `{{input_ticket_id}}`, `{{last_updated}}`
- **验证**: `ticket-cli validate .aces/tickets/selections/工单ID`

### 🧪 poc (POC工单)
- **用途**: 方案验证、可行性分析、原型开发
- **目录**: `.aces/tickets/pocs/`
- **输入**: `input/poc-plan.md`
- **输出**: `output/poc-results.md`, `output/validation-report.md`
- **占位符**: `{{input_ticket_id}}`, `{{last_updated}}`
- **验证**: `ticket-cli validate .aces/tickets/pocs/工单ID`

### 💻 dev (开发工单)
- **用途**: 开发实现、代码编写、测试验证
- **目录**: `.aces/tickets/dev/`
- **输入**: `input/dev-specs.md`
- **输出**: `output/code-delivery.md`, `output/test-results.md`
- **占位符**: `{{input_ticket_id}}`, `{{acceptance_ticket_id}}`, `{{last_updated}}`
- **验证**: `ticket-cli validate .aces/tickets/dev/工单ID`

### ✅ acceptance (验收工单)
- **用途**: 质量验证、标准检查、最终确认
- **目录**: `.aces/tickets/acceptance/`
- **输入**: `input/acceptance-criteria.md`
- **输出**: `output/acceptance-report.md`, `output/final-approval.md`
- **占位符**: `{{input_ticket_id}}`, `{{last_updated}}`
- **验证**: `ticket-cli validate .aces/tickets/acceptance/工单ID`

 
## 自定义工单类型

### 🚀 deployment (部署工单)
- **用途**: 系统部署、应用发布、配置管理
- **目录**: `.aces/tickets/deployment/`
- **输入**: `input/deployment-requirements.md`, `input/environment-config.json`
- **输出**: `output/deployment-report.md`, `output/config-docs/`, `output/metrics.json`
- **占位符**: `{{input_ticket_id}}`, `{{output_ticket_id}}`, `{{creation_time}}`, `{{last_updated}}`
- **验证**: `ticket-cli validate .aces/tickets/deployment/工单ID`

### 🛠️ ops (运维工单)
- **用途**: 系统监控、故障处理、性能优化
- **目录**: `.aces/tickets/ops/`
- **输入**: `input/ops-requirements.md`
- **输出**: `output/monitoring-report.md`, `output/incident-log.md`
- **占位符**: `{{input_ticket_id}}`, `{{output_ticket_id}}`, `{{creation_time}}`, `{{last_updated}}`
- **验证**: `ticket-cli validate .aces/tickets/ops/工单ID`

### 🧪 testing (测试工单)
- **用途**: 质量保证、测试执行、缺陷跟踪
- **目录**: `.aces/tickets/testing/`
- **输入**: `input/test-plan.md`
- **输出**: `output/test-execution.md`, `output/defect-report.md`
- **占位符**: `{{input_ticket_id}}`, `{{output_ticket_id}}`, `{{creation_time}}`, `{{last_updated}}`
- **验证**: `ticket-cli validate .aces/tickets/testing/工单ID`

## 工单类型对比

| 特性 | 标准类型 | 自定义类型 |
|------|---------|-----------|
| 数量 | 6个 | 3个 |
| 占位符 | 基础占位符 | 扩展占位符 |
| 目录结构 | 固定 | 可定制 |
| 流转关系 | 预定义 | 可配置 |
| 验证方式 | 统一 | 统一 |

## 工单文件结构

```
.aces/tickets/<工单类型>/<工单名称>/
├── input/          # 输入文件目录
│   ├── requirements.md
│   └── config.json
├── output/         # 输出文件目录
│   ├── result.md
│   └── report.md
└── trace.md        # 执行跟踪文件
```

## 占位符说明

- `{{input_ticket_id}}` - 上游工单ID
- `{{output_ticket_id}}` - 下游工单ID
- `{{acceptance_ticket_id}}` - 验收工单ID
- `{{creation_time}}` - 创建时间
- `{{last_updated}}` - 最后更新时间