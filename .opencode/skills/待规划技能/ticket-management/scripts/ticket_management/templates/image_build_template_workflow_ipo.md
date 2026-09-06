# IMAGE-BUILD工单模板 - IPO结构 v1.0

## 基本信息

**工作流名称**: {{WORKFLOW_NAME}}
**工作流类型**: {{WORKFLOW_TYPE}}
**项目目录**: {{PROJECT_CWD}}
**创建时间**: {{CREATE_TIME}}
**负责人**: {{OWNER}}
**工作流文件路径**: {{WORKFLOW_PATH}}
**本工作流是否有效**: true

## 工单目标
**目标**: 使用image-builder技能制作多语言Docker镜像，支持Python、Node.js、Go、Java、C++等语言的交叉编译环境

## Input（输入）
- **输入来源**: 上游技术选型工单或用户需求
- **输入内容**: 
  - 镜像版本要求 (如: v1.0, latest)
  - 目标平台架构 (x86_64, ARM64, ARM32, Windows)
  - 编程语言需求清单
  - 特殊工具要求
- **触发条件**: 技术选型确认，需要建立开发环境镜像

## 执行步骤

### Stage 1: 镜像规格确认
[ ] Task: 镜像规格确认
    操作(必选)：
        Step1: 使用image-builder技能确认镜像构建规格和参数
        Step2: 备份现有image-builder技能的Dockerfile文件
        Step3: 在现有image-builder技能的Dockerfile文件进行调整

### Stage 2: Docker镜像制作
[ ] Task: Docker镜像制作
    操作(必选)：
        Step1: 使用image-builder技能执行镜像构建，支持版本管理和标签
        Step2: 验证镜像完整性和工具可用性

### Stage 3: 输出验证
[ ] Task: 输出验证
    操作(必选)：
        Step1: 使用image-builder技能验证所有编程语言运行时
        Step2: 检查交叉编译工具链完整性

### Stage 4: github推送
[ ] Task: github推送
    操作(必选)：
        Step1: 使用gh创建github issue补充镜像使用文档
        Step2: 提交变更并创建远程tag image-<版本号>

### Stage 5: 创建下游工单
[ ] Task: 验证当前工单是否符合[交付物](##交付物)要求和[目录结构](##目录结构)
    操作(必选)：
        Step1: 验证交付物
        Step2: 验证目录结构
[ ] Task: 创建下游工单
    操作(必选)：
        Step1: 本工单为终端工单，无需创建下游工单

## Output（输出）
- **输出内容**: 
  - Docker镜像文件 (multi-lang-builder:vX.X 或 multi-lang-builder:latest)
  - 镜像使用文档
  - 工具验证报告
  - 构建日志和版本信息
- **下游工单**: (无)
- **触发条件**: 镜像构建成功，所有工具验证通过

## 异常场景和处理方式

| 错误代码 | 异常描述 | 处理动作 | 负责人 |
|----------|----------|----------|--------|
| ERROR:001 | Docker服务未启动 | 启动Docker服务，检查Docker守护进程状态 | 运维人员 |
| ERROR:002 | 镜像构建失败 | 检查Dockerfile语法，修复构建错误后重试 | 开发人员 |
| ERROR:003 | 网络下载超时 | 切换国内镜像源，重试拉取基础镜像 | 运维人员 |
| ERROR:004 | 磁盘空间不足 | 清理无用镜像，释放磁盘空间后重试 | 运维人员 |
| ERROR:005 | 交叉编译工具链缺失 | 安装缺失的工具链，重新构建 | 开发人员 |
| ERROR:006 | Github推送失败 | 检查SSH认证，修复认证问题后重试 | 开发人员 |

## 决策场景

| 触发条件 | 决策动作 | 预期结果 | 回退方案 |
|----------|----------|----------|----------|
| WHEN: 多个基础镜像版本可选 | THEN: **权衡稳定性**：选择LTS版本，确保长期支持 | 镜像稳定可靠 | 使用上一稳定版本 |
| WHEN: 镜像体积过大 | THEN: **权衡精简度**：使用多阶段构建，移除不必要工具 | 镜像体积优化 | 分层构建，按需加载 |
| WHEN: 多平台构建时间过长 | THEN: **权衡效率**：优先构建常用平台，其他平台按需构建 | 构建效率提升 | 使用CI/CD并行构建 |

## 观测模块

| 检查点 | 观测方法 | 预期状态 | 异常处理 |
|--------|----------|----------|----------|
| OBS_POINT: Docker服务状态 | OBS_METHOD: docker info | Docker服务正常运行 | 启动Docker服务 |
| OBS_POINT: 镜像构建进度 | OBS_METHOD: docker build 输出日志 | 构建成功完成 | 检查构建日志，修复错误 |
| OBS_POINT: 镜像大小 | OBS_METHOD: docker images \| grep multi-lang-builder | 镜像大小在合理范围 | 优化Dockerfile，减少层数 |
| OBS_POINT: 工具验证 | OBS_METHOD: docker run 镜像名 工具名 --version | 所有工具版本正确 | 重新安装缺失工具 |

## 交付物

| 交付物 | 格式 | 说明 |
|--------|------|------|
| Docker镜像 | Docker Image | 多语言开发环境镜像 |
| Dockerfile | 文本文件 | 镜像构建配置文件 |
| 镜像使用文档 | Markdown | 镜像使用说明和示例 |
| 工具验证报告 | Markdown | 工具验证结果和版本信息 |

## 目录结构
```markdown
.aces/tickets/image_build/{{execute_name}}/
├── input/          # 输入文件目录
│   ├── meta.md                # 上游工单的元信息,包括工单目录和项目信息等等
│   └── requirements.md       # 镜像制作要求
├── output/         # 输出文件目录
│   ├── meta.md                # 工单的元信息,包括工单目录和项目信息等等
│   ├── scripts/    # Dockerfile引用的脚本
│   └── Dockerfile      # 交付Dockerfile
└── trace.md        # 执行跟踪文件
```

## 占位符号变量清单

| 变量 | 来源                      |
|------|-------------------------|
| {{WORKFLOW_NAME}} | 工作流创建时根据上下文自动补全         |
| {{WORKFLOW_TYPE}} | 工作流创建时指定，固定为image_build |
| {{CREATE_TIME}} | 工作流创建时根据上下文自动补全自动生成     |
| {{OWNER}} | 工作流创建时指定负责人             |
| {{PROJECT_CWD}} | 项目根目录路径,根据上下文自动补全       |
| {{WORKFLOW_PATH}} | 工作流文件完整路径,根据上下文自动补全     |
| {{execute_name}} | 本次执行的工单标题,根据上下文自动补全     |
| {{input_ticket_id}} | 上游技术选型工单ID,根据上下文自动补全    |
| {{output_ticket_id}} | 无，不需要         |

## 子工作流清单

| 子工作流名称 | 验证是否通过(workflow-creator validate <子工作流路径>) |
|--------|----------|
| 无 | N/A |

## AI能力增强

| 类型 | 名称 | 预期使用 |
|------|------|----------|
| skill | image-builder | WHEN 需要构建Docker镜像 THEN 使用image-builder技能完成镜像制作 |
| skill | ticket-management | WHEN 需要管理工单 THEN 使用ticket-management技能创建和管理工单 |
| mcp | filesystem | WHEN 需要读写Dockerfile THEN 使用filesystem MCP操作文件系统 |
| mcp | git | WHEN 需要提交变更 THEN 使用git MCP提交代码变更 |

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
*工单类型: image-build*
