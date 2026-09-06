---
name: create-ticket-template
description: 按工作流模板创建工单模板并注册到工单管理系统。支持扩展工单管理系统模板类型，在SKILL.md中登记新类型，并将模板文件放入templates目录。使用场景：需要扩展工单模板库、创建新的工单类型、定制工单流程。
---

# create-ticket-template - 工单模板创建技能

按IPO结构设计模式创建工单模板并注册到工单管理系统。工单遵循标准IPO结构：Input（输入）→ Process（处理）→ Output（输出），实现工单流转的自动化和标准化。

## 使用场景

- 扩展工单模板库：添加新的工单类型到系统
- 创建定制工单：基于IPO结构设计特定领域的工单
- 工单流程设计：定义工单之间的流转关系和技能执行顺序
- 模板库管理：维护和更新符合IPO标准的工单模板集合

## 核心功能

### IPO结构模板创建
- **标准IPO结构**：自动生成Input、Process、Output三个核心部分
- **技能清单管理**：按执行顺序罗列技能清单
- **自动流转机制**：定义输入来源和下游工单触发条件
- **占位符处理**：自动配置工单ID占位符变量

### 工单管理系统集成
- **类型注册**：在工单管理系统SKILL.md中登记新类型
- **模板文件管理**：将模板文件放入工单管理系统templates目录
- **完全集成**：与现有工单管理系统无缝集成

## 使用方法

### 1. 安装技能
```bash
# 安装技能（支持热加载）
pip install -e E:\clawspace\skills\create-ticket-template\scripts
```

### 2. 创建新工单类型（IPO结构）
```bash
# 创建新的工单类型
ticket-template-ipo create-type <类型名> <描述>

# 示例：创建部署工单类型
ticket-template-ipo create-type deployment "部署工单：系统部署、应用发布、配置管理"
```

### 3. 创建IPO模板文件
```bash
# 创建标准IPO结构模板文件
ticket-template-ipo create-template <类型名>

# 示例：创建部署工单IPO模板
ticket-template-ipo create-template deployment
```

### 4. 查看工单类型
```bash
# 列出所有工单类型
ticket-template-ipo list-types
```

### 5. 获取帮助
```bash
# 显示帮助信息
ticket-template-ipo --help

# 显示特定命令的帮助
ticket-template-ipo create-type --help
```

## 模板文件结构

### 生成的模板文件
- **文件名格式**：`<类型名>_template_workflow.md`
- **存储位置**：`E:\clawspace\skills\ticket-management\templates\`
- **文件内容**：严格遵循IPO结构（Input→Process→Output）

### IPO标准模板结构
```markdown
# [工单类型]工单模板

## 📋 工单目标
**目标**: [简要描述工单目标和业务价值]

## 📥 Input（输入）
- **输入来源**: [用户输入/上游工单ID]
- **输入内容**: [具体输入内容描述]
- **触发条件**: [什么条件下启动此工单]

## 🔄 Process（处理）
### 任务1: [任务名称] 🎯
- [ ] **技能名称1** - [完成什么工作]
- [ ] **技能名称2** - [完成什么工作]
- [ ] **技能名称3** - [完成什么工作]

### 任务2: [任务名称] 🎯
- [ ] **技能名称4** - [完成什么工作]
- [ ] **技能名称5** - [完成什么工作]

## 📤 Output（输出）
- **输出内容**: [技能执行结果汇总]
- **下游工单**: [自动创建的下游工单类型]
- **触发条件**: [什么条件下触发下游工单]

## 📝 占位符变量
- `{{input_ticket_id}}` - 上游工单ID
- `{{output_ticket_id}}` - 下游工单ID
- `{{creation_time}}` - 创建时间
- `{{last_updated}}` - 最后更新时间
```

## 工单类型注册

### 在SKILL.md中注册
新类型会自动在工单管理系统SKILL.md中注册：

```markdown
## 工单类型

- **deployment** - 部署工单类型
- **ops** - 运维工单类型
- **custom-type** - 自定义工单类型
```

### 支持的类型
- 标准类型：research, selection, poc, dev, acceptance, self-check
- 自定义类型：任意符合命名规范的类型名称

## 占位符变量

### 支持的占位符
- `{{input_ticket_id}}` - 上游工单ID
- `{{output_ticket_id}}` - 下游工单ID
- `{{creation_time}}` - 创建时间
- `{{last_updated}}` - 最后更新时间

### 变量使用
```markdown
## 流转关系

### 上游依赖
- 输入来自工单: {{input_ticket_id}}

### 下游工单
- 输出将触发工单: {{output_ticket_id}}
```

## 工作流转换

### 转换过程
1. **读取工作流**：读取源工作流文件内容
2. **分析结构**：分析输入输出文件
3. **生成模板**：转换为工单模板格式
4. **保存文件**：保存到工单管理系统模板目录

### 自动分析
- **输入文件检测**：自动识别input/目录下的文件
- **输出文件检测**：自动识别output/目录下的文件
- **任务提取**：提取工作流中的任务列表

## 集成规范

### 目录结构
```
E:\clawspace\skills\ticket-management\
├── SKILL.md                    # 工单管理系统技能文件
└── templates\
    ├── research_template_workflow.md
    ├── selection_template_workflow.md
    ├── deployment_template_workflow.md    # 新增
    └── ops_template_workflow.md           # 新增
```

### 文件规范
- **编码**：UTF-8
- **换行符**：Windows CRLF
- **命名规范**：小写字母+下划线，最多20字符
- **版本控制**：使用Git管理

## 错误处理

### 常见错误
- **类型已存在**：创建重复的类型名称
- **文件不存在**：指定的工作流文件不存在
- **权限不足**：无法写入模板目录
- **编码错误**：文件编码不兼容

### 解决方案
- **重复类型**：使用list-types查看现有类型
- **文件路径**：使用绝对路径或正确相对路径
- **权限问题**：检查目录权限
- **编码问题**：确保文件使用UTF-8编码

## 示例工作流

### 示例1: 创建部署工单（IPO结构）
```bash
# 1. 安装技能
pip install -e E:\clawspace\skills\create-ticket-template\scripts

# 2. 创建部署工单类型
ticket-template-ipo create-type deployment "部署工单：系统部署、应用发布、配置管理"

# 3. 创建IPO模板
ticket-template-ipo create-template deployment

# 4. 查看工单类型
ticket-template-ipo list-types
```

### 示例2: 创建技术选型工单（IPO结构）
```bash
# 1. 安装技能
pip install -e E:\clawspace\skills\create-ticket-template\scripts

# 2. 创建选型工单类型
ticket-template-ipo create-type selection "选型工单：技术选型、安全分析、部署方案"

# 3. 创建IPO模板
ticket-template-ipo create-template selection

# 4. 查看工单类型
ticket-template-ipo list-types
```

### 示例3: 创建演示工单（IPO结构）
```bash
# 1. 安装技能
pip install -e E:\clawspace\skills\create-ticket-template\scripts

# 2. 创建演示工单类型
ticket-template-ipo create-type demo "演示工单：IPO结构演示"

# 3. 创建IPO模板
ticket-template-ipo create-template demo

# 4. 查看工单类型
ticket-template-ipo list-types
```

## 最佳实践

### 类型命名
- **简洁明了**：使用简短、明确的名称
- **避免冲突**：不与现有类型重复
- **语义化**：名称能反映工单用途

### 模板设计
- **单一职责**：每个模板专注于一个特定任务
- **输入明确**：明确定义需要的输入文件
- **输出清晰**：明确定义产生的输出文件
- **流转关系**：定义与上下游工单的关系

### 集成建议
- **逐步扩展**：先创建类型，再创建模板
- **验证测试**：创建后立即验证
- **文档更新**：更新相关文档
- **版本管理**：使用Git管理变更

## 故障排除

### 问题1: 命令未找到
**症状**: 无法找到ticket-template-ipo命令
**原因**: 技能未正确安装
**解决**: 重新运行`pip install -e E:\clawspace\skills\create-ticket-template\scripts`

### 问题2: 类型注册失败
**症状**: 无法在SKILL.md中注册新类型
**原因**: SKILL.md文件格式不正确或权限不足
**解决**: 检查SKILL.md文件语法，确保格式正确且有写入权限

### 问题3: 模板文件创建失败
**症状**: 无法创建模板文件
**原因**: 模板目录不存在或权限不足
**解决**: 检查模板目录权限，确保可写入

### 问题4: 类型已存在
**症状**: 创建重复的类型名称
**原因**: 类型名称已存在
**解决**: 使用list-types查看现有类型，选择不同的名称

## 参考文档

- **工作流规范**: 见 [references\workflow.md](references\workflow.md) - 技能创建和验证的标准工作流

## 相关技能

- **ticket-management** - 工单管理系统
- **workflow-manager** - 工作流管理器
- **skill-creator** - 技能创建器

## 版本信息

- **版本**: v1.0.0 (IPO版本)
- **更新时间**: 2026-04-01
- **兼容性**: 与工单管理系统v3.9.0兼容
- **设计模式**: IPO (Input→Process→Output)
- **安装方式**: pip install -e (支持热加载)