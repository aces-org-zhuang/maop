# SOFTWARE-BUILD工单模板 - IPO结构 v1.0

## 基本信息

**工作流名称**: {{WORKFLOW_NAME}}
**工作流类型**: {{WORKFLOW_TYPE}}
**项目目录**: {{PROJECT_CWD}}
**创建时间**: {{CREATE_TIME}}
**负责人**: {{OWNER}}
**工作流文件路径**: {{WORKFLOW_PATH}}
**本工作流是否有效**: true

## 工单目标
**目标**: 使用software-integration技能进行源码构建，支持Python、Node.js、Go、Java、C++、Qt等语言的统一构建管理

## Input（输入）
- **输入来源**: 上游开发工单或技术选型工单
- **输入内容**: 
  - 源码仓库地址或本地源码路径
  - 构建目标平台 (Linux/Windows/macOS)
  - 编程语言类型 (Python/Node.js/Go/Java/C++/Qt)
  - 依赖配置要求 (requirements.txt/package.json等)
  - 构建参数和环境变量
- **触发条件**: 源码准备完成，需要构建可执行文件或安装包

## 执行步骤

### Stage 1: 构建环境初始化
[ ] Task: 构建环境初始化
    操作(必选)：
        Step1: 使用software-integration技能初始化构建目录结构
        Step2: 使用software-integration技能创建软件构建配置
        Step3: 使用源码获取技能获取源码到指定目录

### Stage 2: 依赖管理
[ ] Task: 依赖管理
    操作(必选)：
        Step1: 使用software-integration技能配置依赖文件 (requirements.txt/package.json)
        Step2: 使用software-integration技能安装构建依赖
        Step3: 使用环境检查技能验证构建环境完整性

### Stage 3: 源码构建
[ ] Task: 源码构建
    操作(必选)：
        Step1: 使用software-integration技能执行构建脚本 (build.sh)
        Step2: 使用构建验证技能验证构建产物完整性
        Step3: 使用交叉编译技能支持多平台编译 (ARM64/ARM32/Windows)

### Stage 4: 安装部署
[ ] Task: 安装部署
    操作(必选)：
        Step1: 使用software-integration技能执行安装脚本 (install.sh)
        Step2: 使用部署验证技能验证安装结果
        Step3: 使用环境配置技能配置运行时环境

### Stage 5: 质量保障
[ ] Task: 质量保障
    操作(必选)：
        Step1: 使用构建测试技能执行构建后测试
        Step2: 使用性能验证技能验证构建产物性能
        Step3: 使用文档生成技能生成构建文档

### Stage 6: 创建下游工单
[ ] Task: 验证当前工单是否符合[交付物](##交付物)要求和[目录结构](##目录结构)
    操作(必选)：
        Step1: 验证交付物
        Step2: 验证目录结构
[ ] Task: 创建下游工单
    操作(必选)：
        Step1: 使用ticket-management技能创建下游工单(部署工单)

## Output（输出）
- **输出内容**: 
  - 构建产物 (可执行文件/JAR包/二进制文件)
  - 安装包 (deb/rpm/exe/msi)
  - 构建日志和版本信息
  - 构建文档和使用说明
  - 测试报告和性能指标
- **下游工单**: 部署工单（系统部署和应用发布）
- **触发条件**: 构建成功，测试通过，文档完整

## 异常场景和处理方式

| 错误代码 | 异常描述 | 处理动作 | 负责人 |
|----------|----------|----------|--------|
| ERROR:001 | 依赖包安装失败 | 检查网络连接，重试安装，如失败则切换镜像源 | 开发人员 |
| ERROR:002 | 编译错误 | 检查代码语法，修复编译错误后重新编译 | 开发人员 |
| ERROR:003 | 交叉编译失败 | 检查交叉编译工具链，安装缺失工具后重试 | 开发人员 |
| ERROR:004 | 构建产物不完整 | 检查构建日志，修复构建配置后重新构建 | 开发人员 |
| ERROR:005 | 安装脚本执行失败 | 检查安装环境，修复权限问题后重试 | 运维人员 |
| ERROR:006 | 构建后测试失败 | 分析测试失败原因，修复问题后重新测试 | 开发人员 |

## 决策场景

| 触发条件 | 决策动作 | 预期结果 | 回退方案 |
|----------|----------|----------|----------|
| WHEN: 多个构建工具可选 | THEN: **权衡生态**：选择项目占比最大的构建工具 | 构建工具生态完善 | 使用备选构建工具 |
| WHEN: 构建时间过长 | THEN: **权衡效率**：启用并行构建，优化构建缓存 | 构建效率提升 | 拆分构建任务，分批执行 |
| WHEN: 多平台构建冲突 | THEN: **权衡优先级**：优先构建主平台，其他平台按需构建 | 主平台构建完成 | 使用CI/CD并行构建 |
| WHEN: 构建产物体积过大 | THEN: **权衡精简度**：启用裁剪选项，移除不必要依赖 | 产物体积优化 | 分层打包，按需加载 |

## 观测模块

| 检查点 | 观测方法 | 预期状态 | 异常处理 |
|--------|----------|----------|----------|
| OBS_POINT: 构建环境状态 | OBS_METHOD: 检查构建工具版本和环境变量 | 工具版本正确，环境变量完整 | 安装缺失工具，配置环境变量 |
| OBS_POINT: 依赖安装进度 | OBS_METHOD: 检查依赖安装日志 | 所有依赖安装成功 | 检查网络，切换镜像源重试 |
| OBS_POINT: 编译进度 | OBS_METHOD: 检查编译输出日志 | 编译成功完成 | 分析编译错误，修复代码 |
| OBS_POINT: 构建产物 | OBS_METHOD: 检查输出目录中的构建产物 | 产物完整，版本正确 | 重新执行构建流程 |
| OBS_POINT: 测试结果 | OBS_METHOD: 检查测试报告 | 所有测试用例通过 | 修复失败用例，重新测试 |

## 交付物

| 交付物 | 格式 | 说明 |
|--------|------|------|
| 构建产物 | 压缩包 | 可执行文件或库文件 |
| 安装包 | deb/rpm/exe | 平台安装包 |
| 构建日志 | 文本文件 | 构建过程和版本信息 |
| 安装文档 | Markdown | 安装步骤和使用说明 |
| 测试报告 | Markdown | 构建后测试结果 |

## 目录结构
```markdown
.aces/tickets/software-build/{{execute_name}}/
├── input/                    # 输入文件目录
│   ├── meta.md                # 上游工单的元信息,包括工单目录和项目信息等等
│   ├── source/              # 源码目录
│   └── source.md            # 其他来源 比如github等源码来源
├── output/                  # 输出文件目录
│   ├── meta.md                # 工单的元信息,包括工单目录和项目信息等等
│   ├── <soft-name>-<version>-<时间戳>.zip  # 构建产物
│   └── install.md           # 安装文档
└── trace.md                 # 执行跟踪文件
```

## 构建命令示例

```bash
# 初始化构建环境
bash .aces/deploy/build.sh init {{software_name}}

# 执行构建
bash .aces/deploy/build.sh {{software_name}}

# 执行安装
bash .aces/deploy/install.sh {{software_name}}
```

## 占位符号变量清单

| 变量 | 来源 |
|------|------|
| {{WORKFLOW_NAME}} | 工作流创建时指定,根据上下文自动补全 |
| {{WORKFLOW_TYPE}} | 工作流创建时指定，固定为software_build |
| {{CREATE_TIME}} | 工作流创建时自动生成,根据上下文自动补全 |
| {{OWNER}} | 工作流创建时指定负责人,根据上下文自动补全 |
| {{PROJECT_CWD}} | 项目根目录路径,根据上下文自动补全 |
| {{WORKFLOW_PATH}} | 工作流文件完整路径,根据上下文自动补全 |
| {{execute_name}} | 本次执行的工单标题,根据上下文自动补全 |
| {{input_ticket_id}} | 上游工单ID（开发工单或技术选型工单）,根据上下文自动补全 |
| {{output_ticket_id}} | 下游工单ID（部署工单）,根据上下文自动补全 |
| {{software_name}} | 软件名称,根据上下文自动补全 |
| {{build_target}} | 构建目标平台,根据上下文自动补全 |
| {{language_type}} | 编程语言类型,根据上下文自动补全 |

## 子工作流清单

| 子工作流名称 | 验证是否通过(workflow-creator validate <子工作流路径>) |
|--------|----------|
| 无 | N/A |

## AI能力增强

| 类型 | 名称 | 预期使用 |
|------|------|----------|
| skill | software-integration | WHEN 需要构建软件 THEN 使用software-integration技能完成构建和安装 |
| skill | ticket-management | WHEN 需要创建下游工单 THEN 使用ticket-management技能创建部署工单 |
| mcp | filesystem | WHEN 需要读写构建文件 THEN 使用filesystem MCP操作文件系统 |
| mcp | git | WHEN 需要提交构建结果 THEN 使用git MCP提交变更 |

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
*工单类型: software-build*
*核心技能: software-integration*
*支持语言: Python, Node.js, Go, Java, C++, Qt*
*支持平台: Linux, Windows, macOS, ARM64, ARM32*
