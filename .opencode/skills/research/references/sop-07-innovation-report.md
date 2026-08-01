# SOP 07: Innovation Report

用于生成技术创新产品分析报告、技术创新报告或创新汇报文档。它是 `research` 的输出 path，不是独立入口。

## When To Use

- 用户要求撰写创新产品分析报告、技术创新报告或创新汇报文档。
- 用户需要以技术问题与技术方案论证为主线的报告，而不是市场/创业叙事。
- 用户需要把 research_root 下的 discovery、innovation、evidence、repo insights 和技术设计整合成可交付长文档。

## Report Rules

- 技术创新主导：报告必须围绕技术问题与技术方案展开。
- 市场最小支撑：市场/竞品信息只做最小必要支撑，默认放在背景章节。
- 证据化表达：关键结论必须可追溯到 research_root 内的证据、来源或前序产物。
- 禁止泛商业化：不要写成融资、增长、营销或商业计划书。
- 图文并茂：对比表、架构图、场景图必须服务论证，不做装饰性输出。
- 质量门禁：完整报告前先 Preview Gate；复杂技术论证先 Reasoning Gate；定版前 Review Gate >=80；完成声明前提供 evidence。

## Input Mapping

- `{research_root}/intake/request.md` -> 报告首页、问题定义和边界。
- `{research_root}/discovery/*`、`{research_root}/sources/*` -> 背景和业界方案。
- `{research_root}/innovation/*` -> 创新方案整体描述和技术展开。
- `{research_root}/insights/*`、`{research_root}/matrix/*`、技术设计产物 -> 技术方案展开和预期效果。
- `{research_root}/evidence/*` -> 技术壁垒、可绕过性和取证方法。
- `expression-delivery` -> 架构图、场景图、对比图、slides 或 HTML preview。

## Fixed Structure

必须按顺序输出 7 章正文，并在全文贯穿第 8 条呈现约束。

```text
1. 整体创新方案名称（首页）
2. 背景描述：现实应用背景、需求、痛点、约束和最小必要市场支撑
3. 业界现有技术方案：相关方案描述、问题场景、局限性与不足
4. 本项目创新方案整体描述：痛点、差异化创新点、应用场景、产品形态
5. 技术方案展开：每步的动机、本步痛点、技术挑战、与业界差异、关键技术点与产出
6. 技术方案预期效果：可验证的预期效果与量化表达
7. 技术壁垒、可绕过性与技术点取证方法

第 8 条（呈现约束，贯穿 1–7，不单成章）：
适当使用对比表格、架构图、场景图等，使全文图文并茂、逻辑严谨；禁止无说明的装饰性图表。
```

## Chapter Requirements

- 第 2 章：量化数据必须标注来源或说明为内部估算。
- 第 3 章：必须包含业界方案对比表。
- 第 5 章：每一步必须包含 step / motivation / painAddressed / keyProblem / differentiationVsIncumbent / keyTechPoint / expectedOutput。
- 第 6 章：必须包含 baseline / target / measurementMethod / estimatedImpact。
- 第 7 章：必须包含壁垒类型、绕过路径、绕过成本、验证/防御建议和技术取证方法。

## Output Files

- `{research_root}/outputs/innovation-report-preview.md`
- `{research_root}/outputs/innovation-report.md`
- 可选：`{research_root}/reports/innovation-report-assets.md`
