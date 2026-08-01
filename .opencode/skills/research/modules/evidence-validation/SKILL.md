---
name: evidence-validation
description: |
  证据与验证 skill：在 research 统一入口下，为核心观点生成代码片段证据包，并输出 claim->evidence 验证映射表。
---

# Evidence & Validation

## 输入
- `{research_root}/paper/core-claims.md`
- `{research_root}/paper/claim-map.md`
- 相关仓库洞察文档
- `{research_root}`：由统一入口指定，格式必须是 `vendor/research/aces-research/topics/<research_slug>`；缺失时先回到根入口确定，不要自行猜测

## 输出（必须写入）
- `{research_root}/evidence/snippets.md`
- `{research_root}/evidence/validation.md`
- `{research_root}/evidence/threats-to-validity.md`

## 规则
- 证据以代码片段为主，必须包含文件路径、上下文说明
- validation.md 必须是 claim→evidence 的映射，可审计
- 验证失败的 claim 必须回退到核心观点阶段修订或删除，不能进入 `paper/paper.md`。
- 写入后同步更新 `{research_root}/README.md` 的当前阶段和下一步。
