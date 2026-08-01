# Research 子模块索引

本文件是 `.opencode/skills/research/` 的阶段索引。根级 `SKILL.md` 触发后，先读本索引，再按 stage-step workflow 选择一个当前 Stage，并读取或加载对应子模块。

## Progressive Stage 规则

- 每个 Stage 由独立 subagent 执行；根技能只做路由、补齐上下文和结果校验。
- 默认允许在同一用户请求内顺序交给多个 subagent 续跑，只要不触发真实阻塞或用户显式确认点。
- Stage 0 只负责确定 `research_root`、课题 README 和当前 Stage。
- 每个 Stage 的第一步必须读取或加载对应子模块，并由该 Stage 的 subagent 完成执行；不得用主线程手工研究替代子模块。
- 下游 Stage 不提前展开。只有当前 Stage 的最小产物满足 Exit Criteria 后，才在 README 的“下一步”中指向下游 Stage。
- 如果用户请求命中多个 Stage，选择最早缺失 Stage。例如“研究工程化建设能力并对比仓库”在没有 `repos-index.md` 时先进入仓库选型。

## 阶段模块

| Stage | 子模块 | 何时读取/加载 | 最小产物 |
| --- | --- | --- | --- |
| Stage 1 趋势与方向发现 | `trend-research/SKILL.md` | 新课题开始、需要热点调研、需要 10 个候选方向时由独立 subagent 执行 | `trend/hot-topics.md`、`trend/directions.md`、`trend/direction-selected.json` |
| Stage 2 资料发现 | `tech-link-finder` | 需要技术文章、趋势资料、开源项目线索、学习资源或外部资料扩展时由独立 subagent 执行 | `sources/source-index.md`、`sources/links.md`、`sources/tech-trends.md` |
| Stage 2a 微信文章来源抽取 | `weixin-article` | 输入材料包含 `mp.weixin.qq.com` 链接，且需要抽取、总结或作为证据来源时由独立 subagent 执行 | `sources/weixin/<article-slug>.md`、`sources/source-index.md` |
| Stage 3 仓库选型 | `repo-selection/SKILL.md` | 需要候选仓库、评分维度、工程样本边界或用户给出仓库 URL 时由独立 subagent 执行 | `selection/candidates.md`、`selection/selection.md`、`repos-index.md` |
| Stage 4 仓库洞察 | `repo-insights-algorithms/SKILL.md` | 已有 `repos-index.md`，需要按仓库阅读代码、文档或工程机制时由独立 subagent 执行 | `insights/<repo-slug>.md`、`insights/evidence-notes.md`、`insights/gaps.md` |
| Stage 5 对比矩阵 | `repo-comparison-matrix/SKILL.md` | 已有仓库洞察，需要正交比较和补漏标注时由独立 subagent 执行 | `matrix/coverage-annotation.md`、`matrix/comparison-matrix.md` |
| Stage 6 论文建模与选题 | `paper-modeling-topics/SKILL.md` | 已有洞察和矩阵，需要论文模型、大纲和候选选题时由独立 subagent 执行 | `paper/model.md`、`paper/outline.md`、`paper/topics.md`、`paper/topic-selected.json` |
| Stage 7 核心观点 | `core-claims/SKILL.md` | 已冻结论文题目，需要可追溯核心观点时由独立 subagent 执行 | `paper/core-claims.md`、`paper/claim-map.md` |
| Stage 8 证据验证 | `evidence-validation/SKILL.md` | 已有核心观点和 claim-map，需要 claim->evidence 闭环时由独立 subagent 执行 | `evidence/snippets.md`、`evidence/validation.md`、`evidence/threats-to-validity.md` |

## 辅助模块

| 模块 | 何时读取 | 用途 |
| --- | --- | --- |
| `patent-fetch/SKILL.md` | 研究需要专利证据、专利来源追踪或竞品专利材料时 | 通过 patent-mcp-server 获取专利详情 |

`tech-link-finder` 和 `weixin-article` 保持独立技能身份；research 只在 Stage 2/Stage 2a 中按需用 Skill 工具加载，并约束其输出路径。

## 路由规则

- 根级 `research/SKILL.md` 负责续点、Stage 判断、产物路径和 Completion Review。
- 子模块只负责各自 Stage 的执行细节；主入口不得手工替代子模块方法论。
- 子模块输出根统一使用根入口传入的 `{research_root}`，格式必须是 `vendor/research/aces-research/topics/<research_slug>`。
- 子模块不得自行猜测 `{research_root}`；缺少该值时先回到 Stage 0 Resolve Topic。
- 一次任务只允许写入一个 `{research_root}`；并行课题必须逐个确认、分批处理，避免混写。
- 外部资料模块输出必须落到 `{research_root}/sources/`，不得写入 `docs/` 或其他课题目录。
- 每个 Stage 完成后都要更新课题 README 的状态、当前阶段、下一步和相关冻结点。
- 若发现缺少上游冻结点，先回退补齐，不要直接生成下游产物。
- 如果未加载当前 Stage 子技能或 Stage 最小产物缺失，不得把该 Stage 标记为完成。
- 来自 `product-definition` 或 `technical-design` 的转入请求必须明确需要长期研究材料、开源样本、证据包或论文级可追溯输出；轻量产品/技术判断应留在原技能内完成。
