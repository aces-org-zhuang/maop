# SOP 01 - Context Discovery

## Goal

基于真实项目材料理解当前系统，而不是凭经验设计。

## Steps

1. 优先读取项目已有架构文档、模块说明、接口契约和开发规则。
2. 检查相关源代码、测试和配置，以当前实现为最终事实来源。
3. 对照 Delegation Quality Gate 判断是否必须前置委派 Source Map lens；当代码/文档范围较大、入口分散、owner 不清或证据需要独立复核时，先委派只读探索，再由主 agent 合成。
4. 建立源码目录结构图谱：列出相关顶层目录、主入口、模块 owner、测试目录、配置目录和生成物目录；无法确认的目录标为 RED 待补证。
5. 识别相关模块、入口、数据流、状态、权限和外部依赖，并映射到具体目录或文件类别。
6. 如涉及复杂链路，使用 `reasoning-map` 绘制影响面和时序分支。
7. 记录文档与代码不一致之处，并以代码事实为准。
8. 将 Source Map lens 字段写入 Technical Handoff Packet：`source_path`、`owner/module`、`entrypoint`、`test_or_config_path`、`evidence_type`、`confidence`、`gap`。

## Validation

- 设计依据包含具体项目材料或代码位置。
- 设计依据包含源码目录结构图谱，并明确本次设计会触达、复用或避开的目录边界。
- Source Map lens 已吸收到 handoff；低置信或缺 owner 的路径已标 RED，不作为定版依据。
- 没有跳过现有系统直接提出重写方案。
