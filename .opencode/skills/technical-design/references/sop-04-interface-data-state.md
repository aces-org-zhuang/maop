# SOP 04 - Interface Data State

## Goal

明确接口、数据、状态、错误处理和权限边界。

## Steps

1. 列出现有接口、需要新增或修改的接口，以及调用方/消费者。
2. 描述数据结构、字段语义、持久化、迁移和兼容性影响。
3. 描述核心状态机、事件顺序、异步边界和就绪条件。
4. 描述错误处理、重试、回滚、权限和安全边界。
5. 对照 Delegation Quality Gate 判断是否必须前置委派 Interface/State lens；多消费者契约、并行状态源、异步链路、权限/错误边界不清时必须委派局部复核。
6. 将 Interface/State lens 字段吸收到 handoff：`contract_or_state`、`producer`、`consumer`、`source_of_truth`、`lifecycle_or_sequence`、`compatibility`、`failure_mode`、`confidence`。
7. 需要图表时转入 `expression-delivery` 生成最少必要图，不为琐碎细节画图。

## Validation

- 消费者能根据接口和数据说明实现或评审。
- 异步和状态变化有时序保证或明确风险。
- 每个契约和状态都有唯一 owner/source of truth；未知项标 RED，不能交给实现阶段猜测。
