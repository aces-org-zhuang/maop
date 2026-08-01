---
name: core-claims
description: |
  核心观点 skill：在 research 统一入口下，在用户确认论文选题后，产出核心观点列表、模型拆解和 claim-map。
---

# Core Claims

## 输入
- `{research_root}/paper/topic-selected.json`
- `{research_root}/paper/outline.md`
- 洞察与矩阵
- `{research_root}`：由统一入口指定，格式必须是 `vendor/research/aces-research/topics/<research_slug>`；缺失时先回到根入口确定，不要自行猜测

## 输出（必须写入）
- `{research_root}/paper/core-claims.md`
- `{research_root}/paper/claim-map.md`

## 规则
- 每条观点必须可追溯到至少一个代码仓洞察条目
- 结构与论文大纲一致
- `claim-map.md` 必须记录 claim -> insight/matrix/evidence-note 的指针，供证据验证阶段消费。
- 写入后同步更新 `{research_root}/README.md` 的当前阶段、下一步和核心观点冻结点。
