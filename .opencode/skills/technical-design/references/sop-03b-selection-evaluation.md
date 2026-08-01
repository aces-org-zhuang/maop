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
- 本阶段的开源选型面向解决方案依赖引入：默认通过包管理器、SDK、框架、服务、CLI 或 submodule 等受控依赖形式接入项目，优先保障构建、测试、license/security 和版本锁定完整性。
- 非必要不侵入修改第三方源码，不把候选仓库复制进项目后自研化，也不把解决方案依赖选型当作 research 的论文样本或源码研究对象。

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
├── software-build-map.md
└── integration-plan.md
```

## Evaluation Flow

1. Intake：明确目标能力、必须条件、约束、禁用项、许可证边界和技术栈。
2. Candidate Discovery：已有候选直接评估；缺候选时用 `research` 的 Discovery Path 发现候选。
3. Reasoning Gate：使用 `reasoning-map` 推演候选与目标方案的能力闭环、依赖边界、集成路径、构建影响、运行时风险和替代方案；推荐项的关键结论置信度必须 >=90%。
4. Screening：按解决方案适配、维护状态、license、安全、生态、集成成本、构建完整性和退出成本筛掉明显不合适项。
5. Deep Evaluation：评估活跃度、成熟度、社区健康度、功能覆盖、风险、迁移成本、版本锁定方式和项目构建/测试影响。
6. Decision：输出推荐项、备选项、拒绝理由、引入方式和未闭环风险；置信度低于 90% 时不得定版，只能进入验证计划。
7. Software Build Map：输出项目软件构建图，清晰展示自研组件、开源组件、依赖引入方式、版本锁定、构建/运行边界和验证路径；图后必须用 Markdown table 补充组件交互逻辑和关键 IPO（输入、处理、输出），避免把图塞入过多文字。
8. Validation Plan：设计最小验证动作，例如 spike、sample integration、API probe、license/security check、build/test probe 或 POC Gate。

## Scoring Guidance

评分可以辅助排序，但不是硬规则。默认维度：

- Fit：需求匹配度、核心能力覆盖、扩展性。
- Health：最近更新、release 节奏、issue/PR 响应、贡献者数量。
- Maturity：项目年龄、文档、测试、生产案例、版本稳定性。
- Risk：license、CVE、依赖风险、默认配置暴露面、维护风险。
- Integration：API 复杂度、运行时依赖、平台兼容、迁移成本、版本锁定和构建完整性。
- Adoption：是否能以声明依赖方式接入、是否需要 fork/patch、是否侵入现有架构、是否存在可控替代和退出路径。

## Output Requirements

- 候选表必须包含推荐理由和拒绝理由。
- 最终建议必须能追溯到用户约束和评估证据。
- 不确定项必须列为风险或验证动作，不用高分掩盖。
- 选定方案进入实现前，必须说明 `reasoning-map` 门禁结论、关键置信度、依赖引入方式、版本/构建保障、license/security 边界和 POC Gate。
- 依赖选型完成后，必须产出 `software-build-map.md` 或等价项目软件构建图，清晰区分 first-party 自研组件与 third-party 开源组件，并标注它们如何进入构建、运行和验证链路；同时补充组件交互逻辑和关键 IPO 表。
