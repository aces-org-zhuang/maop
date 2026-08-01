---
name: paper-modeling-topics
description: |
  论文建模 skill：在 research 统一入口下，基于洞察与对比矩阵生成论文模型、论文大纲，并给出10个候选选题与推荐，写入根入口传入的 vendor/research/aces-research/topics/<research_slug>/paper/。
---

# Paper Modeling & Topics

## 输入
- `{research_root}/insights/*`
- `{research_root}/matrix/comparison-matrix.md`
- `{research_root}`：由统一入口指定，格式必须是 `vendor/research/aces-research/topics/<research_slug>`；缺失时先回到根入口确定，不要自行猜测

## 输出（必须写入）
- `{research_root}/paper/model.md`
- `{research_root}/paper/outline.md`
- `{research_root}/paper/topics.md`
- `{research_root}/paper/topic-selected.json`（默认冻结题目）

## 规则
- topics.md 必须包含10个选题，每个含：标题、研究问题、材料来源（哪些仓）、预期贡献、风险。
- 需给出推荐顺序与推荐理由。
- 默认自动选择推荐顺位最高且最贴合研究主线的题目写入 `topic-selected.json`，不要停下来询问下一步。
- 只有用户明确要求人工选择、多个题目同分且无法根据研究主线区分，或缺少论文建模目标时，才使用 `question`。
- 写入后同步更新 `{research_root}/README.md` 的当前阶段、下一步和论文题目冻结点。
