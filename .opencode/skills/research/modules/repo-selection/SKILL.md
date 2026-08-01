---
name: repo-selection
description: |
  代码仓选型 skill：在 research 统一入口下，基于研究主题与约束，生成候选代码仓清单、评分维度与选型结论，并写入根入口传入的 vendor/research/aces-research/topics/<research_slug>/selection/ 与 repos-index.md。
---

# Repo Selection

## 输入
- 研究主题（topic）与目标
- 技术栈偏好（可选）
- 约束（stars/license/活跃度等，可选）
- `{research_root}`：由统一入口指定，格式必须是 `vendor/research/aces-research/topics/<research_slug>`；缺失时先回到根入口确定，不要自行猜测

## 输出（必须写入）
- `{research_root}/selection/candidates.md`
- `{research_root}/selection/selection.md`
- `{research_root}/repos-index.md`

## 约束
- 输出必须可追溯：包含仓库URL、选择理由、评分维度。
- 多因子选型：代码质量 / 文档 / 社区活跃度 / 技术相关性。
- `repos-index.md` 是论文可复现样本边界；深度阅读前必须冻结或明确标记为暂定。
- 进入核心样本或后续需要源码洞察的仓库，必须记录目标 submodule 路径 `{research_root}/repos/<repo_name>`；不得规划为普通 clone、主仓 `vendor/research/<repo_name>` 或 `aces-research` 根目录子仓。
- 写入后同步更新 `{research_root}/README.md` 的当前阶段、下一步和样本仓库冻结点。
