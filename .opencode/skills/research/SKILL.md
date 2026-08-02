---
name: research
description: 必须用于基于 research_root 沉淀的发现、资料搜索、微信关键词搜索、微信文章提取、技术趋势发现、tool/skill 发现、创新方法论、创新机会识别、技术创新报告、创新产品分析报告、创新汇报文档、证据包、仓库研究、论文建模和既有课题续点。触发后先创建或续接 research_root，再只执行本次请求需要的流水线路径；不要把研究材料写入主仓 docs/ 或主仓 research/。
---

# Research Discovery Pipeline

本技能是统一的发现、研究、创新和证据流水线。所有 discovery / research / innovation 请求都先创建或续接 `research_root`，但流水线支持部分执行：只搜微信、只找资料、只做创新机会、只做仓库研究或只补证据都可以，不强制跑完整论文链路。

## Root Rule

1. 每次触发先执行 Root Gate：创建或续接唯一 `research_root`。
2. `research_workspace` 固定为主仓 submodule `vendor/research/aces-research`。
3. `research_root` 固定为 `{research_workspace}/topics/<research_slug>`。
4. 研究材料只能写入 `{research_root}`；不要写入主仓 `docs/`、主仓 `research/` 或主仓其他目录。
5. 研究参考开源项目必须以 Git submodule 形式加入 `{research_root}/repos/<repo_name>`；不得普通 clone 到主仓目录。
6. 每次执行后更新 `{research_root}/README.md`：本次 path、产物、冻结点、下一步建议和未闭环风险。

## Trigger Paths

```text
资料、链接、趋势、学习资源、知识库、tool/skill 查找
  -> Discovery Path

微信关键词搜索、搜狗微信搜索、公众号文章搜索
  -> Weixin Search Path

mp.weixin.qq.com URL 阅读、总结、提取、证据化
  -> WeChat Extraction Path

创新方法论、TRIZ、蓝海、设计思维、精益创业、创新机会
  -> Innovation Discovery Path

技术创新报告、创新产品分析报告、创新汇报文档、技术壁垒或技术取证报告
  -> Innovation Report Path

仓库 URL、开源样本、仓库研究、源码洞察、横向对比
  -> Repo Research Path

证据包、claim-evidence、来源验证、论文支撑
  -> Evidence Path

论文选题、论文模型、大纲、核心观点、论文材料
  -> Paper Path
```

## Pipeline Control

- 支持部分执行：用户只要求一个 path 时，只执行该 path 并停止。
- 如果请求命中多个 path，按依赖顺序执行最小必要路径；不要默认展开全链路。
- 如果缺少上游输入，只补齐当前 path 所需的最小输入。
- 复杂课题、影响面、证据链或创新路径选择前，先使用 `reasoning-map` 推演。
- 大范围检索、候选扩展、来源抽取、仓库初筛、证据完整性检查可使用 subagent Task 隔离低价值探索上下文；使用前按 `development-workflow/references/subagent-context-budgeting.md` 定义边界和 return contract，主 agent 保留 research_root、reasoning-map、收敛和最终结论责任。
- 外部联网检索、微信/公众号搜索、GitHub/API 访问、下载、工具/skill 安装建议或浏览器提取前，按 `development-workflow/references/configuration-readiness-gate.md` 统一确认检索范围、平台、速率/安全边界、输出路径、凭据边界和用户授权；不要在抓取过程中临时索要配置。
- 检索、搜索、文章提取、创新机会发现和创新报告素材整合必须遵循 `paths/sop-retrieval-reasoning.md`：先扩展检索，再收敛证据，再围绕 RED 点继续扩展，再收敛，直到满足退出条件；不要一次性关键词搜索后直接写结论。
- 仓库研究、开源样本选择、源码洞察和横向对比前，必须先经过 `modules/repo-selection/SKILL.md` 的研究对象门禁；核心样本必须先证明 Level1 直接研究对象充足且 `topic_directness >= 0.90`，不得把 Level0 基础技术栈仓库直接当作主研究对象。
- 需要产品定义/PRD 时转入 `product-definition`。
- 需要技术选型或设计决策时转入 `technical-design`。
- 需要图表、slides、原型或视觉表达时转入 `expression-delivery`。
- 需要 submodule 操作和 PR 治理时转入 `submodule-manager`。

## Path Index

- `paths/sop-00-root-intake.md`: 创建或续接 `research_root`。
- `paths/sop-01-pipeline-routing.md`: path-based 路由和部分执行规则。
- `paths/sop-02-discovery.md`: 外部资料、技术链接、趋势、tool/skill 发现。
- `paths/sop-03-weixin-search.md`: 关键词 + Playwright MCP + 搜狗微信搜索。
- `paths/sop-04-innovation-discovery.md`: 创新方法论和机会发现。
- `paths/sop-05-research-workspace.md`: research workspace、README 和产物规范。
- `paths/sop-06-evidence.md`: 来源验证、claim-evidence 和证据边界。
- `paths/sop-07-innovation-report.md`: 技术创新报告和创新汇报输出。
- `paths/sop-retrieval-reasoning.md`: Discovery、Weixin、WeChat Extraction、Innovation Discovery 和 Innovation Report 的扩展/收敛检索推演循环。
- `router/subskills-index.md`: 原深度研究子技能索引。

## Migrated Assets

- `assets/discovery/technical-sources/`: 技术资料和趋势发现流程。
- `assets/discovery/wechat-extraction/`: 微信文章提取、安全和输出格式。
- `assets/discovery/skills-ecosystem/`: tool/skill 发现与安装规则。
- `assets/innovation/methodology/`: 创新方法论参考。
- `tools/discovery/`: 资料发现 CLI 原型与辅助脚本。
- `templates/innovation-report.md`: 技术创新报告模板。
- `checklists/innovation-report.md`: 技术创新报告质量检查清单。

## Default Research Root Layout

```text
{research_root}/
├── README.md
├── intake/
│   └── request.md
├── discovery/
│   ├── search-plan.md
│   ├── technical-sources.md
│   ├── weixin-search.md
│   └── skills-tools.md
├── sources/
│   ├── source-index.md
│   ├── links.md
│   └── weixin/
├── innovation/
│   ├── methodology.md
│   ├── opportunities.md
│   ├── assumptions.md
│   └── validation-plan.md
├── selection/
├── repos/
├── insights/
├── evidence/
├── paper/
├── reports/
└── outputs/
    ├── innovation-report-preview.md
    └── innovation-report.md
```

## Completion Rule

完成声明必须说明：本次 `research_root`、执行 path、新增或更新的产物、来源证据、未闭环风险、下一步建议，以及是否需要转入其他流水线。
