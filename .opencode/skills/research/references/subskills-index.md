# Research Path And Subskill Index

本文件是 `research` 的 path 与深度研究子技能索引。根级 `SKILL.md` 先创建或续接 `research_root`，再按用户请求选择最小必要 path。Discovery、Weixin 和 Innovation 已内置在 `research/references/sop-*.md`；深度仓库/论文/证据阶段继续使用子技能。

## Built-in Paths

| Path | 何时使用 | 最小产物 |
| --- | --- | --- |
| Root Intake | 所有请求 | `README.md`、`intake/request.md` |
| Discovery | 资料、链接、趋势、学习资源、tool/skill 查找 | `discovery/technical-sources.md`、`sources/source-index.md`、`sources/links.md` |
| Weixin Search | 微信关键词搜索、公众号搜索、搜狗微信搜索 | `discovery/weixin-search.md`、`sources/source-index.md` |
| WeChat Extraction | `mp.weixin.qq.com` URL 阅读、总结、提取 | `sources/weixin/<article-slug>.md`、`sources/source-index.md` |
| Innovation Discovery | 创新方法论、TRIZ、蓝海、设计思维、精益创业、创新机会 | `innovation/methodology.md`、`innovation/opportunities.md`、`innovation/assumptions.md`、`innovation/validation-plan.md` |

## Deep Research Subskills

| Stage | 子模块 | 何时读取/加载 | 最小产物 |
| --- | --- | --- | --- |
| Trend Discovery | `trend-research/SKILL.md` | 新课题需要热点调研或 10 个候选方向 | `trend/hot-topics.md`、`trend/directions.md`、`trend/direction-selected.json` |
| Repo Selection | `repo-selection/SKILL.md` | 需要候选仓库、评分维度、工程样本边界或用户给出仓库 URL | `selection/candidates.md`、`selection/selection.md`、`repos-index.md` |
| Repo Insights | `repo-insights-algorithms/SKILL.md` | 已有 `repos-index.md`，需要仓库源码/文档/工程机制洞察 | `insights/<repo-slug>.md`、`insights/evidence-notes.md`、`insights/gaps.md` |
| Comparison Matrix | `repo-comparison-matrix/SKILL.md` | 已有仓库洞察，需要正交比较和补漏标注 | `matrix/coverage-annotation.md`、`matrix/comparison-matrix.md` |
| Paper Modeling | `paper-modeling-topics/SKILL.md` | 需要论文模型、大纲和候选选题 | `paper/model.md`、`paper/outline.md`、`paper/topics.md`、`paper/topic-selected.json` |
| Core Claims | `core-claims/SKILL.md` | 已冻结论文题目，需要可追溯核心观点 | `paper/core-claims.md`、`paper/claim-map.md` |
| Evidence Validation | `evidence-validation/SKILL.md` | 需要 claim->evidence 闭环和证据边界 | `evidence/snippets.md`、`evidence/validation.md`、`evidence/threats-to-validity.md` |

## Auxiliary Subskills

| 模块 | 何时读取 | 用途 |
| --- | --- | --- |
| `patent-fetch/SKILL.md` | 研究需要专利证据、专利来源追踪或竞品专利材料时 | 通过 patent-mcp-server 获取专利详情 |

## Routing Rules

- 一次任务只允许写入一个 `{research_root}`；并行课题必须逐个确认、分批处理，避免混写。
- 支持部分执行；不要因为缺少下游论文产物就阻塞轻量 Discovery、Weixin 或 Innovation path。
- 子技能输出根统一使用根入口传入的 `{research_root}`，格式必须是 `vendor/research/aces-research/topics/<research_slug>`。
- 子技能不得自行猜测 `{research_root}`；缺少该值时先回到 Root Intake。
- 每个 path 完成后都要更新课题 README 的状态、当前 path、下一步和相关冻结点。
- 若发现缺少当前 path 必需的上游冻结点，先补齐最小输入，不要自动展开无关 path。
