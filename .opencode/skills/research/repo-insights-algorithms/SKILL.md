---
name: repo-insights-algorithms
description: |
  算法实现洞察 skill：在 research 统一入口下，对选定代码仓以课题内 submodule 形式阅读与实现分析，输出到根入口传入的 vendor/research/aces-research/topics/<research_slug>/insights/，按 repo 隔离。
---

# Repo Insights (Algorithms)

## 输入
- 代码仓列表（name/url/branch 可选）
- 研究关注点（默认：算法实现）
- `{research_root}`：由统一入口指定，格式必须是 `vendor/research/aces-research/topics/<research_slug>`；缺失时先回到根入口确定，不要自行猜测
- `{research_root}/repos-index.md`

## 输出（必须写入）
- 每个仓：`{research_root}/insights/{repo-slug}.md`
- `{research_root}/insights/evidence-notes.md`
- `{research_root}/insights/gaps.md`（如存在缺仓、缺模块或证据弱点）

## 洞察内容模板
- 仓库概览（语言/模块/入口）
- 核心算法列表与定位（文件路径）
- 算法实现要点（数据结构/复杂度/边界条件/优化点）
- 可复用模式/反模式
- 每条关键洞察尽量带文件路径、模块入口或可复查锚点。
- 源码读取必须来自 `{research_root}/repos/<repo_name>` 下的 Git submodule；如果仓库尚未作为 submodule 加入，先补齐 submodule 或将本阶段标记为 blocked，不得临时 clone 到主仓目录。
- 写入后同步更新 `{research_root}/README.md` 的当前阶段和下一步。
