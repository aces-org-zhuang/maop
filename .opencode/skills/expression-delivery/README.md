# Expression Delivery

统一表达产物流水线，用于收敛旧的 frontend、prototype、diagram、slides、image 和 UI/UX 智能类入口。

## 范围

- 前端 UI、React/HTML/CSS 页面和组件。
- 交互原型、低保真 mock、HTML preview。
- Mermaid、UML、流程图、时序图、状态图、架构图和 DFD。
- HTML slides、视觉报告和演示 deck。
- 图片生成提示词、参考图分析和多模态视觉表达。

## 质量门禁

- Reasoning Gate: 复杂表达结构、交互、渲染或多模态链路前使用 `reasoning-map`。
- Preview Gate: 高成本生成前先确认低成本预览。
- Review Gate: 复杂预览、关键视觉产物和交付前 review >=80。
- POC Gate: 高风险交互、响应式、动画、渲染或生成路径先薄切片验证。
- Verification Gate: 完成声明前提供 fresh evidence。

## 收敛范围

本技能统一承接前端界面、原型、图表、slides、图片和多模态表达产物，避免为每一种表达形式保留分散入口。

## 迁移资产

- `references/diagram-examples/`: 图表类型示例库，覆盖 E-R、组件、时序、流程、DFD、状态、用例、FMEA、威胁模型、决策树和甘特图。
- `references/html-slides/`: HTML slides 设计、排版、颜色、字体、Mermaid 渲染和高度控制参考。
- `references/image-generation/`: 图片生成 prompt、Gemini Banana API 和历史构建参考。
- `data/ui-ux-library/`: UI/UX 风格、颜色、字体、产品类型、技术栈和设计系统检索数据。
- `tools/`: HTML 校验、slide height 检查、图片生成和 UI/UX 检索辅助脚本。
