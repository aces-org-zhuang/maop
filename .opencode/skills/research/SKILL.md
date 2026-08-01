---
name: research
description: |
  LLM 研究与论文生成统一入口技能。用户要求技术研究、继续已有研究课题、开源仓库对比、证据包整理、核心观点建模、论文选题、论文草稿生成或从 aces-research 续点时，必须使用本技能。触发后先解析 research_workspace 与 research_root，再按 stage-step 工作流由独立 subagent 逐段执行，默认连续推进到真实阻塞点或用户显式要求停下为止；阶段方法论必须加载对应子技能，不要把研究过程材料写入主仓 docs/ 或主仓 research/。
---

# Research Stage Workflow

本技能是 `.opencode/skills/research/` 的渐进式路由器。它只负责：确定研究工作区和课题、选择当前阶段、把当前 Stage 分派给独立子代理、检查阶段产物、更新课题 README。具体研究方法留给阶段子技能。

## 不可绕过规则

- 每个 Stage 必须由独立 subagent 执行，根技能只做路由、补齐上下文和结果校验，不在主上下文里完成阶段研究。
- 默认按照“一个 Stage 一个 subagent”运行；若当前课题已具备后续 Stage 所需输入，且不会触发用户确认，则可以在同一次用户请求内继续把下一个 Stage 交给新的 subagent，直到遇到真实阻塞。
- 每个 Stage 的 Step 1 永远是读取或加载对应子技能；不得用手工搜索、手工总结替代阶段子技能。
- `research_workspace` 固定为主仓 submodule `vendor/research/aces-research`；所有研究材料、课题索引、论文草稿、证据包和研究用开源参考仓都必须写入该 submodule。
- `research_root` 固定为 `{research_workspace}/topics/<research_slug>`；主仓根目录 `research/` 只允许作为历史只读迁移来源，不再作为新研究输出根。
- 研究参考开源项目必须以 Git submodule 形式加入 `{research_root}/repos/<repo_name>`，不得独立克隆到主仓目录，也不得放在 `aces-research` 仓库根目录。
- 不要提前读取下游阶段子技能。只有当前 Stage 的 Exit Criteria 满足后，才能把 README 的下一步指向下游阶段。
- 如果用户请求很宽泛，选择最早缺失的 Stage，而不是综合执行全流程。
- 如果阶段输入缺失，回退到能补齐输入的最早 Stage，并更新 README 的状态/下一步。
- 研究材料只能写入 `{research_workspace}/topics/<research_slug>/`；不要写入主仓 `docs/`、主仓 `research/` 或主仓其他目录。
- `product-definition` 或 `technical-design` 需要深度外部证据、开源样本、论文级证据包或可复现研究材料时，可以转入本技能；普通 PRD 竞品扫描、轻量产品分析、一次性技术判断不自动进入 research 工作区。

## Stage 0: Resolve Topic

### Goal

确定本轮唯一 `research_workspace`、`research_root` 和当前阶段。

### Inputs

- 用户请求。
- `{research_workspace}/index.md`。
- `.opencode/skills/research/references/subskills-index.md`。

### Steps

1. 确认 `vendor/research/aces-research` submodule 已存在且可读取；若远端仍为空或未初始化，标记 blocked，不把新研究材料写回主仓 `research/`。
2. 读取 `{research_workspace}/index.md`。
3. 读取 `.opencode/skills/research/references/subskills-index.md`。
4. 如果用户指定课题标题或 slug，从 index 匹配并读取 `{research_workspace}/topics/<research_slug>/README.md`。
5. 如果用户只说继续研究，优先选择最近更新且仍处于 `in_progress` 的 active topic；若没有可续接课题，再回报可用课题并标记需要用户指定。
6. 如果是新课题，创建 `{research_workspace}/topics/<research_slug>/README.md`，并登记到 `{research_workspace}/index.md`。
7. 根据“Stage Router”选择本轮唯一当前阶段。

### Outputs

- 已确定的 `research_workspace = vendor/research/aces-research`。
- 已确定的 `research_root = vendor/research/aces-research/topics/<research_slug>`。
- 已确定的 `current_stage`。

### Exit Criteria

- `research_root` 已存在并登记在 `{research_workspace}/index.md`。
- 课题 README 存在，且包含状态、当前阶段、下一步、冻结点和产物导航。

### Handoff

进入 Stage Router 选择的阶段链路，并继续交给后续 subagent，直到遇到真实阻塞或完成当前请求范围。

## Stage Router

按用户请求和已存在产物选择最早缺失阶段。

```text
用户要求热点/趋势/方向发现
  -> Stage 1 Trend Discovery

用户要求补充外部资料/技术文章/趋势资料/资料来源
  -> Stage 2 Source Discovery

用户给出仓库 URL、要求工程样本、仓库选型、开源项目对比
  -> Stage 3 Repo Selection

`repos-index.md` 已存在，用户要求深入仓库/源码/实现机制/工程化能力
  -> Stage 4 Repo Insights

`insights/*.md` 已存在，用户要求对比/矩阵/横向分析
  -> Stage 5 Comparison Matrix

矩阵和洞察已存在，用户要求论文模型/选题/大纲
  -> Stage 6 Paper Modeling

论文题目已冻结，用户要求核心观点/claim-map
  -> Stage 7 Core Claims

核心观点已存在，用户要求证据包/验证/claim 对齐
  -> Stage 8 Evidence Validation
```

如果请求同时命中多个阶段，选择最早缺失阶段。比如“研究工程化建设能力并对比仓库”应先进入 Stage 3 Repo Selection；如果样本仓已冻结，再进入 Stage 4 Repo Insights。

## Stage 1: Trend Discovery

### Goal

发现 10 个研究方向并冻结 1 个方向。

### Inputs

- `research_root`。
- 研究主题或用户大方向。

### Steps

1. 读取 `.opencode/skills/research/trend-research/SKILL.md`。
2. 按子技能要求调研热点、生成 10 个方向。
3. 自动选择排名最高且最贴合用户主题的方向作为默认冻结项；如果用户显式要求交互筛选，再改用 `question`。
4. 写入阶段产物。
5. 更新课题 README 的当前阶段、下一步和研究方向冻结点。

### Outputs

- `{research_root}/trend/hot-topics.md`
- `{research_root}/trend/directions.md`
- `{research_root}/trend/direction-selected.json`

### Exit Criteria

- 10 个方向已写入 `directions.md`，并已写入默认冻结项。

### Handoff

下一步通常是 Stage 2 Source Discovery 或 Stage 3 Repo Selection。

## Stage 2: Source Discovery

### Goal

补充外部资料、趋势材料、技术文章、学习资源或候选项目线索。

### Inputs

- `research_root`。
- 研究方向或用户给出的资料范围。

### Steps

1. 使用 Skill 工具加载 `tech-link-finder`；不要只手工 webfetch。
2. 按 `tech-link-finder` 的发现/分析/收集流程搜索并筛选资料。
3. 如果材料包含 `mp.weixin.qq.com` 且需要抽取正文，使用 Skill 工具加载 `weixin-article`。
4. 写入 sources 产物。
5. 更新课题 README 的当前阶段和下一步。

### Outputs

- `{research_root}/sources/source-index.md`
- `{research_root}/sources/links.md`
- `{research_root}/sources/tech-trends.md`
- 可选：`{research_root}/sources/weixin/<article-slug>.md`

### Exit Criteria

- `source-index.md` 登记了本轮来源。
- `links.md` 或 `tech-trends.md` 至少一个包含可追溯链接和价值说明。

### Handoff

如果资料中产生候选仓库或用户要求工程样本，进入 Stage 3 Repo Selection。

## Stage 3: Repo Selection

### Goal

冻结用于后续深入研究的样本仓库边界。

### Inputs

- 研究主题、方向或外部资料线索。
- 可选：用户指定的仓库 URL。
- `research_root`。

### Steps

1. 读取 `.opencode/skills/research/repo-selection/SKILL.md`。
2. 基于研究目标生成候选仓库、评分维度和选择理由。
3. 对用户明确给出的仓库，必须纳入候选清单并说明是否作为核心样本。
4. 对进入核心样本或后续需要源码洞察的开源项目，规划为 `{research_root}/repos/<repo_name>` 下的 Git submodule，不得规划为主仓 `vendor/research/<repo_name>`、主仓 `research/vendor/<repo_name>` 或普通 clone 目录。
5. 写入阶段产物。
6. 更新课题 README 的样本仓库冻结点。

### Outputs

- `{research_root}/selection/candidates.md`
- `{research_root}/selection/selection.md`
- `{research_root}/repos-index.md`

### Exit Criteria

- `repos-index.md` 存在，且每个样本包含 name/url/branch 或默认分支/选择理由/状态。

### Handoff

下一步是 Stage 4 Repo Insights。

## Stage 4: Repo Insights

### Goal

对已冻结样本仓进行源码、文档或工程机制洞察。

### Inputs

- `{research_root}/repos-index.md`
- 研究关注点。
- `research_root`。

### Steps

1. 读取 `.opencode/skills/research/repo-insights-algorithms/SKILL.md`。
2. 根据研究关注点修正“算法实现”默认模板；如果主题是工程化能力，洞察轴应覆盖 workflow/state/permission/verification/artifact/dashboard/evolution 等工程机制。
3. 通过 `{research_root}/repos/<repo_name>` 下的 Git submodule 读取样本仓；如样本仓尚未加入，应先按该路径生成 submodule 添加计划并执行或标记 blocked，不得普通 clone 到主仓目录。
4. 写入每仓洞察、证据笔记和缺口。
5. 更新课题 README 的当前阶段和下一步。

### Outputs

- `{research_root}/insights/<repo-slug>.md`
- `{research_root}/insights/evidence-notes.md`
- `{research_root}/insights/gaps.md`（如存在）

### Exit Criteria

- 每个核心样本至少有一份 `insights/<repo-slug>.md`。
- 关键洞察带路径、模块入口或可复查锚点。

### Handoff

下一步是 Stage 5 Comparison Matrix。

## Stage 5: Comparison Matrix

### Goal

把仓库洞察转成正交对比矩阵，并标注缺口。

### Inputs

- `{research_root}/repos-index.md`
- `{research_root}/insights/*.md`
- `research_root`。

### Steps

1. 读取 `.opencode/skills/research/repo-comparison-matrix/SKILL.md`。
2. 先做 coverage 标注，检查是否遗漏关键仓或关键特性。
3. 若缺口阻塞矩阵，更新 `insights/gaps.md` 并回退 Stage 4。
4. 写入对比矩阵。
5. 更新课题 README 的当前阶段和下一步。

### Outputs

- `{research_root}/matrix/coverage-annotation.md`
- `{research_root}/matrix/comparison-matrix.md`

### Exit Criteria

- `comparison-matrix.md` 行列正交，单元格包含实现程度和证据指针。

### Handoff

下一步是 Stage 6 Paper Modeling，或按用户要求回到 Stage 4 补洞察。

## Stage 6: Paper Modeling

### Goal

基于洞察和矩阵生成论文模型、大纲和候选选题。

### Inputs

- `{research_root}/insights/*`
- `{research_root}/matrix/comparison-matrix.md`
- `research_root`。

### Steps

1. 读取 `.opencode/skills/research/paper-modeling-topics/SKILL.md`。
2. 生成模型、大纲和 10 个候选选题。
3. 自动选择推荐顺位最高且最贴合研究主线的题目作为默认冻结项；如果用户显式要求交互确认，再改用 `question`。
4. 写入阶段产物。
5. 更新课题 README 的论文题目冻结点。

### Outputs

- `{research_root}/paper/model.md`
- `{research_root}/paper/outline.md`
- `{research_root}/paper/topics.md`
- `{research_root}/paper/topic-selected.json`

### Exit Criteria

- `topic-selected.json` 已写入默认冻结题目。

### Handoff

下一步是 Stage 7 Core Claims。

## Stage 7: Core Claims

### Goal

生成可追溯核心观点和 claim-map。

### Inputs

- `{research_root}/paper/topic-selected.json`
- `{research_root}/paper/outline.md`
- 洞察与矩阵产物。
- `research_root`。

### Steps

1. 读取 `.opencode/skills/research/core-claims/SKILL.md`。
2. 生成核心观点列表和模型拆解。
3. 为每条 claim 记录 insight/matrix/evidence-note 指针。
4. 写入阶段产物。
5. 更新课题 README 的核心观点冻结点。

### Outputs

- `{research_root}/paper/core-claims.md`
- `{research_root}/paper/claim-map.md`

### Exit Criteria

- 每条核心观点至少可追溯到一个仓库洞察或矩阵证据。

### Handoff

下一步是 Stage 8 Evidence Validation。

## Stage 8: Evidence Validation

### Goal

生成 claim->evidence 验证映射，删除或回退无法验证的 claim。

### Inputs

- `{research_root}/paper/core-claims.md`
- `{research_root}/paper/claim-map.md`
- 相关仓库洞察文档。
- `research_root`。

### Steps

1. 读取 `.opencode/skills/research/evidence-validation/SKILL.md`。
2. 收集代码片段、路径和上下文说明。
3. 写入 claim->evidence 映射。
4. 对验证失败的 claim，回退 Stage 7 修订或删除。
5. 更新课题 README 的当前阶段和下一步。

### Outputs

- `{research_root}/evidence/snippets.md`
- `{research_root}/evidence/validation.md`
- `{research_root}/evidence/threats-to-validity.md`

### Exit Criteria

- `validation.md` 中每个保留 claim 都有证据映射。

### Handoff

只有通过 `evidence/validation.md` 验证的 claim 可以进入论文草稿生成。

## 状态值

`{research_workspace}/index.md` 和课题 README 只能使用以下状态：`planned`、`in_progress`、`blocked`、`on_hold`、`drafted`、`completed`、`archived`。

## research_workspace 与 research_root 隔离规则

- `research_workspace` 必须是 `vendor/research/aces-research`。
- `research_root` 必须是 `vendor/research/aces-research/topics/<research_slug>`。
- 续接已有课题时，slug 必须来自 `{research_workspace}/index.md`。
- 新建课题时，先登记 `{research_workspace}/index.md`，再写入课题目录。
- 一次任务只允许写入一个 `research_root`。
- 用户给出主仓 `research/<old_slug>` 或外部历史目录时，只能作为只读参考输入；除非明确要求迁移，不得作为本轮 `research_root`。
- `{research_workspace}/repos/` 禁止直接放置参考仓；参考仓必须位于具体课题下的 `{research_root}/repos/<repo_name>`，避免影响其他课题。

## 课题 README 最小结构

```markdown
# [研究标题]

## 状态
- 状态: in_progress
- 当前阶段: [Stage 名称]
- 上次更新时间: YYYY-MM-DD
- 下一步: [明确的下一步动作]

## 冻结点
- 研究方向: [状态和链接]
- 样本仓库: [状态和链接]
- 论文题目: [状态和链接]
- 核心观点: [状态和链接]

## 产物导航
- 趋势与方向: `trend/`
- 外部资料: `sources/source-index.md`
- 仓库选型: `selection/`
- 样本索引: `repos-index.md`
- 仓库洞察: `insights/`
- 对比矩阵: `matrix/comparison-matrix.md`
- 论文模型: `paper/model.md`
- 核心观点: `paper/core-claims.md`
- 证据验证: `evidence/validation.md`
- 论文草稿: `paper/paper.md`
- 参考仓库: `repos/<repo_name>`（Git submodule）

## 续点规则
优先从“当前阶段”和“下一步”恢复。如果当前阶段依赖的冻结点缺失，先回退补齐冻结点，不直接生成后续产物。
```

## Completion Review

结束本轮前检查：

- 每个已执行 Stage 是否都由独立 subagent 完成；若不是，最终说明为何无法拆分。
- 是否读取或加载了当前 Stage 对应子技能；若没有，README 必须标记 blocked 或说明降级原因。
- Stage Outputs 是否存在；若不存在，不得把阶段写成完成。
- README 的状态、当前阶段、下一步和相关冻结点是否已更新。
- 研究材料是否只写入当前 `research_root`。
- 研究参考开源项目是否只以 Git submodule 形式写入 `{research_root}/repos/<repo_name>`。
