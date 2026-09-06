# SOP 02b - Architecture Confirmation Gate

## Goal

在进入接口、数据、状态、部署实施切片或 implementation handoff 前，先确认目标系统的架构边界、系统组件、部署形态和 IT 资源约束，避免技术设计过早下钻到局部接口或任务清单。

## When Required

必须执行本 Gate，当请求涉及以下任一情况：

- 新系统、新 POC、新服务或外部平台接入。
- 架构、系统组件、部署、资源、环境、账号、网络或安全边界尚未确认。
- 用户要求 technical design、实现准备、implementation handoff、API 接入方案、状态机、RAG、消息队列、外部服务、云资源或部署方案。
- 设计产物会被用于工程排期、资源申请、采购、账号开通或跨团队评审。

只有以下情况可跳过：

- 用户明确只要局部接口草案/状态机片段，且声明不进入实现或资源评估。
- 既有架构包已经存在、路径明确、且本轮没有改变架构边界。

## Required Architecture Confirmation Package

在进入 Stage 4/5/6 或 implementation handoff 前，必须先输出或读取并复用以下内容：

1. Context Diagram
   - 用户/外部系统/第三方平台/内部系统的边界。
   - 谁触发、谁消费、谁拥有凭据和权限。

2. System Component Diagram
   - 核心服务、适配层、编排层、数据层、异步任务、人工/运营后台、观测系统。
   - 每个组件的职责和 owner，禁止出现只写“backend/system/service”的泛节点。

3. Deployment Diagram
   - 运行时实例、网络入口、HTTPS/域名、数据库、缓存、队列、对象存储、模型服务、日志监控。
   - POC 与生产部署差异。

4. Data and State Boundary
   - 主状态来源、持久化对象、缓存对象、消息/事件生命周期。
   - 生产者 -> 持久化/提交 -> 就绪信号 -> 消费者。

5. Integration Boundary
   - 外部 API、SDK、Webhook、凭据、回调、限流、失败重试、权限配置。
   - 哪些接口是 POC 必需，哪些延后。

6. IT Resource List
   - 账号/权限、域名/证书、服务器/容器、DB、Redis/Queue、对象存储、LLM/Embedding、监控告警、人员角色。
   - 标记必需/可选/延后。

7. Open Decisions and RED Points
   - 未确认技术栈、目标仓库、部署环境、凭据边界、数据来源、合规负责人、资源预算。
   - 每个 RED 必须有验证或决策动作。

## Output Order

默认顺序：

```text
1. 设计范围与已确认输入
2. Context Diagram
3. System Component Diagram
4. Deployment Diagram
5. Data/State/Sequence Boundary
6. IT Resource List
7. Architecture Decisions
8. Open RED Points
9. 是否允许进入接口/状态/实施切片
```

## Blocking Rule

如果 Architecture Confirmation Package 未完成：

- 不得定版接口/API。
- 不得定版数据表。
- 不得定版状态机。
- 不得输出 implementation handoff。
- 只能输出架构预览、待确认问题、资源缺口和下一步验证动作。

如果用户催促实现，也必须先说明：当前缺失架构确认包，继续实现会扩大返工风险。

## Quality Bar

架构包合格标准：

- 组件图能回答“系统由哪些部分构成”。
- 部署图能回答“跑在哪里，需要哪些 IT 资源”。
- 数据/状态边界能回答“状态谁生产、谁持久化、谁消费”。
- 集成边界能回答“外部平台怎么接，凭据和回调在哪里”。
- RED 点能回答“进入实现前还缺什么”。

## Common Failure Patterns

- 先写 API、数据库表、状态机，但没有系统组件图。
- 先给实施切片，但没有部署图和资源清单。
- 把“服务端”写成一个大盒子，没有拆接入、编排、AI、数据、观测、人工兜底。
- 忽略账号、域名、证书、凭据、回调和外部平台权限。
- 没有区分 POC 部署和生产部署。
- 没有说明哪些资源是必需、可选或延后。
