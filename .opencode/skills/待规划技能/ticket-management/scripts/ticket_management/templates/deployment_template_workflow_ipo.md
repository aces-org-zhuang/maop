# 部署工单模板 - IPO结构 v1.0

## 基本信息

**工作流名称**: {{WORKFLOW_NAME}}
**工作流类型**: {{WORKFLOW_TYPE}}
**项目目录**: {{PROJECT_CWD}}
**创建时间**: {{CREATE_TIME}}
**负责人**: {{OWNER}}
**工作流文件路径**: {{WORKFLOW_PATH}}
**本工作流是否有效**: true

## 工单目标
**目标**: 使用software-integration技能完成系统部署、应用发布和配置管理

## Input（输入）
- **输入来源**: 上游工单(software-build)或用户输入
- **输入内容**: 
  - 软件包（二进制文件、压缩包）
  - 部署配置文件
  - 目标环境信息
  - 依赖项清单
  - 构建配置
- **触发条件**: 上游工单(software-build)完成或接收到部署需求
- **注意**: 如果用户输入是源码目录，应该先创建软件构建工单（software-build）执行结束后才能执行部署工单

## 执行步骤

### Stage 1: 部署环境准备
[ ] Task: 部署环境准备
    操作(必选)：
        Step1: 使用software-integration初始化部署目录结构 (.aces/deploy/)
        Step2: 使用software-integration添加目标软件到部署管理系统
        Step3: 使用software-integration配置软件依赖和参数

### Stage 2: 软件安装与配置
[ ] Task: 软件安装与配置
    操作(必选)：
        Step1: 使用software-integration执行软件安装 (install.sh)
        Step2: 验证安装结果和依赖完整性
        Step3: 配置环境变量和启动参数

### Stage 3: 部署验证
[ ] Task: 部署验证
    操作(必选)：
        Step1: 使用software-integration运行健康检查
        Step2: 验证服务可用性
        Step3: 生成部署报告

### Stage 4: 创建下游工单
[ ] Task: 验证当前工单是否符合[交付物](##交付物)要求和[目录结构](##目录结构)
    操作(必选)：
        Step1: 验证交付物
        Step2: 验证目录结构
[ ] Task: 创建下游工单
    操作(必选)：
        Step1: 使用ticket-management技能创建下游工单(验收工单)

## Output（输出）
- **输出内容**: 
  - 部署状态报告
  - 安装目录和输出目录信息
  - 服务访问地址和端口
  - 健康检查结果
- **下游工单**: 自动创建验收工单
- **触发条件**: 部署成功，服务正常运行

## 异常场景和处理方式

| 错误代码 | 异常描述 | 处理动作 | 负责人 |
|----------|----------|----------|--------|
| ERROR:001 | 依赖包安装失败 | 检查网络连接，重试安装，如失败则切换镜像源 | 运维人员 |
| ERROR:002 | 配置文件缺失 | 检查模板文件，重新生成默认配置 | 运维人员 |
| ERROR:003 | 权限不足 | 申请相应权限，或切换执行用户 | 管理员 |
| ERROR:004 | 端口被占用 | 检查端口占用情况，更换端口或停止冲突服务 | 运维人员 |
| ERROR:005 | 服务启动失败 | 检查服务日志，修复配置问题后重试 | 运维人员 |
| ERROR:006 | 健康检查不通过 | 检查服务状态，回滚到上一版本 | 运维人员 |

## 决策场景

| 触发条件 | 决策动作 | 预期结果 | 回退方案 |
|----------|----------|----------|----------|
| WHEN: 多个依赖库版本冲突 | THEN: **权衡兼容性**：选择版本占比最大的库，如无兼容库使用隔离容器(Docker) | 构建成功，功能完整性最高 | 锁定至旧版本依赖，暂停新特性上线 |
| WHEN: 资源使用量（CPU/内存）超标 | THEN: **权衡负载**：降级部分非核心功能，启动自动扩容 | 关键业务不宕机，资源恢复正常 | 切换至灾备系统，限制用户访问 |
| WHEN: 多个部署环境配置不一致 | THEN: **权衡一致性**：以Production环境配置为准进行回滚 | 环境统一，避免线上问题 | 暂停新功能上线，等待环境同步 |
| WHEN: 部署过程中发现安全漏洞 | THEN: **权衡风险**：立即停止部署，修复漏洞后重新部署 | 系统安全性得到保障 | 回滚到安全版本 |

## 观测模块

| 检查点 | 观测方法 | 预期状态 | 异常处理 |
|--------|----------|----------|----------|
| OBS_POINT: 服务启动状态 | OBS_METHOD: curl -f http://localhost:8080/health | HTTP 200 | 检查日志，重启服务 |
| OBS_POINT: 磁盘空间 | OBS_METHOD: df -h /data | 使用率 < 80% | 清理日志，扩容磁盘 |
| OBS_POINT: 端口监听 | OBS_METHOD: netstat -tlnp \| grep 8080 | 端口处于LISTEN状态 | 检查服务配置，重启服务 |
| OBS_POINT: 进程状态 | OBS_METHOD: ps aux \| grep service-name | 进程正常运行 | 检查进程日志，重启进程 |

## 交付物

| 交付物 | 格式 | 说明 |
|--------|------|------|
| 部署状态报告 | Markdown | 包含部署结果、服务状态、访问地址 |
| 安装配置文档 | Markdown | 安装步骤、配置参数、环境变量说明 |
| 健康检查报告 | Markdown | 服务健康检查结果 |
| 部署特性清单 | Markdown | 部署对象的功能特性清单 |

## 目录结构
```markdown
.aces/tickets/deployment/{{execute_name}}/
├── input/                    # 输入文件目录
│   ├── meta.md                # 上游工单的元信息,包括工单目录和项目信息等等
│   ├── software_package.zip   # 软件包（二进制/压缩包）
│   ├── deploy_config.json     # 部署配置
│   └── install.md            # 安装指导
├── output/                  # 输出文件目录
│   ├── meta.md                # 工单的元信息,包括工单目录和项目信息等等
│   ├── phase1-deployment_report.md   # 部署状态报告
│   └── phase2-features.md            # 部署对象特性清单 比如部署的微服务功能等等
└── trace.md                 # 执行跟踪文件
```

## 部署命令参考

### 初始化部署环境
```bash
bash scripts/manage.sh init
```

### 添加软件
```bash
bash scripts/manage.sh add <software-name>
```

### 构建软件（源码预处理）
```bash
# 检测输入类型并执行构建
bash .aces/deploy/build.sh <software-name>
```

### 安装软件（二进制部署）
```bash
# 确保部署的是二进制文件或压缩包
bash .aces/deploy/install.sh <software-name>
```

### 构建流程说明
1. **输入检测**: 自动识别源码、二进制文件或压缩包
2. **源码处理**: 如为源码，先执行编译构建
3. **打包处理**: 将构建结果打包成压缩包
4. **二进制部署**: 最终部署二进制文件或压缩包

## 占位符号变量清单

| 变量 | 来源                     |
|------|------------------------|
| {{WORKFLOW_NAME}} | 工作流创建时指定,根据上下文自动补全              |
| {{WORKFLOW_TYPE}} | 工作流创建时指定，固定为deployment |
| {{CREATE_TIME}} | 工作流创建时自动生成,根据上下文自动补全            |
| {{OWNER}} | 工作流创建时指定负责人,根据上下文自动补全           |
| {{PROJECT_CWD}} | 项目根目录路径,根据上下文自动补全               |
| {{WORKFLOW_PATH}} | 工作流文件完整路径,根据上下文自动补全             |
| {{execute_name}} | 本次执行的工单标题,根据上下文自动补全             |
| {{input_ticket_id}} | 上游工单ID,根据上下文自动补全                |
| {{output_ticket_id}} | 下游工单ID,根据上下文自动补全                |

## 子工作流清单

| 子工作流名称 | 验证是否通过(workflow-creator validate <子工作流路径>) |
|--------|----------|
| 无 | N/A |

## AI能力增强

| 类型 | 名称 | 预期使用 |
|------|------|----------|
| skill | software-integration | WHEN 需要部署软件 THEN 使用software-integration技能完成安装和配置 |
| skill | ticket-management | WHEN 需要创建下游工单 THEN 使用ticket-management技能创建验收工单 |
| mcp | filesystem | WHEN 需要读写部署文件 THEN 使用filesystem MCP操作文件系统 |
| mcp | git | WHEN 需要提交部署结果 THEN 使用git MCP提交变更 |

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
*工单类型: deployment*
*核心技能: software-integration*
