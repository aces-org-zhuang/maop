---
name: trend-research
description: |
  前沿热点调研 skill：在 research 统一入口下，对业界前沿与核心网站进行热点调研，输出10个研究方向供后续选型，并写入根入口传入的 vendor/research/aces-research/topics/<research_slug>/trend/。
---

# Trend Research (Hot Topics)

## 覆盖信息源
- 论文/预印本（例如 arXiv / 会议趋势聚合）
- 代码趋势（例如 GitHub Trending / 热门 repo 类别）
- 技术社区（例如 Hacker News / Reddit / 国内技术社区）
- 厂商与基金会（例如 CNCF / 大厂 Engineering Blog / RFC）

## 输入
- `{topic}`（研究主题/大方向；如果用户未给出则先澄清）
- `{research_root}`：由统一入口指定，格式必须是 `vendor/research/aces-research/topics/<research_slug>`；缺失时先回到根入口确定，不要自行猜测

## 输出（必须写入，按topic隔离）
- `{research_root}/trend/hot-topics.md`
- `{research_root}/trend/directions.md`（10个方向）
- `{research_root}/trend/direction-selected.json`（默认冻结方向）

## 规则
- directions.md 必须包含10个方向：每个方向包含「标题/问题定义/为何是热点/可用代码仓线索/风险」
- 默认自动选择排名最高且最贴合用户主题的方向写入 `direction-selected.json`，不要停下来询问下一步。
- 只有用户明确要求人工筛选、多个方向同分且无法根据用户主题区分，或缺少研究主题时，才使用 `question`。
- 写入后同步更新 `{research_root}/README.md` 的当前阶段、下一步和研究方向冻结点
