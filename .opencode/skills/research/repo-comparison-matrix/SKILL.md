---
name: repo-comparison-matrix
description: |
  对比矩阵 skill：在 research 统一入口下，在仓库洞察后执行补漏标注，并生成正交对比矩阵（特性×代码仓实现程度）到根入口传入的 vendor/research/aces-research/topics/<research_slug>/matrix/。
---

# Repo Comparison Matrix

## 输入
- `{research_root}/insights/*.md` 洞察产物
- 当前候选仓列表
- `{research_root}/repos-index.md`
- `{research_root}`：由统一入口指定，格式必须是 `vendor/research/aces-research/topics/<research_slug>`；缺失时先回到根入口确定，不要自行猜测

## 输出（必须写入）
- `{research_root}/matrix/coverage-annotation.md`
- `{research_root}/matrix/comparison-matrix.md`

## 规则
- 必须先做 coverage 标注：检查是否遗漏关键仓/关键特性
- 对比矩阵必须正交：行=特性/维度，列=仓库；单元格=实现程度（✅/⚠️/❌/?）+ 简短证据指针
- 如果 coverage 暴露缺项，先更新 `{research_root}/insights/gaps.md` 并回退补洞察，不要直接进入论文建模。
- 写入后同步更新 `{research_root}/README.md` 的当前阶段和下一步。
