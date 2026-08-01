# SOP 03b: Selection Evaluation

用于技术选型、依赖选型、开源库/框架/仓库评估和候选方案对比。它是 `technical-design` 的子阶段，不是独立入口。

## When To Use

- 用户要求技术选型、开源项目评估、GitHub repo 对比、库/框架/依赖选择。
- 方案设计依赖第三方项目、SDK、框架、数据库、中间件或工具链。
- 需要在多个实现路径之间做可追踪取舍。

## Boundaries

- 候选资料、链接和初步 repo 搜索可转入 `research` 的 Discovery Path。
- 论文级证据包、长期研究课题或深度开源仓对比转入 `research`。
- 选定后需要 submodule 接入、提交和 PR 治理时转入 `submodule-manager`。
- 需要图表、slides 或选型可视化时转入 `expression-delivery`。

## Artifact Root

- 优先使用项目已有设计产物目录。
- 项目没有规范时，先声明并征得确认：`{selection_artifact_root}`。
- 不硬编码项目私有目录、历史 runtime 目录或固定 workflow 目录。
- 临时 clone、扫描、缓存和中间产物使用 `{temp_root}` 或项目允许的临时目录。

Recommended structure:

```text
{selection_artifact_root}/
├── candidates.md
├── selection-matrix.md
├── license-security-risk.md
├── feature-coverage.md
└── integration-plan.md
```

## Evaluation Flow

1. Intake：明确目标能力、必须条件、约束、禁用项、许可证边界和技术栈。
2. Candidate Discovery：已有候选直接评估；缺候选时用 `research` 的 Discovery Path 发现候选。
3. Screening：按相关性、维护状态、license、安全、生态、集成成本筛掉明显不合适项。
4. Deep Evaluation：评估活跃度、成熟度、社区健康度、功能覆盖、风险和迁移成本。
5. Decision：输出推荐项、备选项、拒绝理由和未闭环风险。
6. Validation Plan：设计最小验证动作，例如 spike、sample integration、API probe、license/security check 或 POC Gate。

## Scoring Guidance

评分可以辅助排序，但不是硬规则。默认维度：

- Fit：需求匹配度、核心能力覆盖、扩展性。
- Health：最近更新、release 节奏、issue/PR 响应、贡献者数量。
- Maturity：项目年龄、文档、测试、生产案例、版本稳定性。
- Risk：license、CVE、依赖风险、默认配置暴露面、维护风险。
- Integration：API 复杂度、运行时依赖、平台兼容、迁移成本。

## Output Requirements

- 候选表必须包含推荐理由和拒绝理由。
- 最终建议必须能追溯到用户约束和评估证据。
- 不确定项必须列为风险或验证动作，不用高分掩盖。
- 选定方案进入实现前，应提供验证策略或 POC Gate。
