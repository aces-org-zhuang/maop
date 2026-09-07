# Target Skill Execution Model

本文件是 `frontend-management-ops` 的执行模型补充，不是通用 skill-creator 模板。

## Selected models

- `任务依赖树`: intake -> contract map -> CRUD/CLI -> import/export/doctor -> validation/handoff。
- `round`: 在实体发现、契约收敛和验证反馈之间迭代。
- `loop`: 验证失败时只修复失败实体或命令，最多 7 轮；配置、授权或安装环境缺失则 blocked。
- `dialectical`: 默认关闭；只有互斥实现方案风险相近时，才进行多视角对抗评审，主 LLM 最终裁决。

## Dispatch

主 LLM 在满足明确节点条件时派发代理执行：并行只读源码发现、独立测试面盘点、CLI 证据抽取或对抗评审。代理不得写业务代码、决定 schema、接受最终 diff 或声明完成。代理必须返回 `Finding`、`Evidence`、`Confidence`、`Fidelity`、`RED`、`Excluded scope`、`Next step`。

## State

每个节点执行前后更新 `todo/status`，并保留实体、动作、产物、验证证据和下一步。成功需要 fresh verification；阻塞需要恢复条件；失败需要保留日志；退出时不得遗留 running 状态。
