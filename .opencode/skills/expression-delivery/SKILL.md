---
name: expression-delivery
description: 必须用于表达产物交付，包括前端 UI、HTML/CSS/React 页面、交互原型、Mermaid/UML/架构图/时序图/状态图、HTML slides、视觉报告、图片生成提示词和多模态表达。用户要求生成、预览、优化、检查或验证 UI、prototype、diagram、slides、image、visual artifact 时优先使用本技能；不要用于产品定义、架构主设计或通用代码实现。
---

# Expression Delivery

本技能是 maop 的表达产物流水线入口。它把已确认的需求、设计、研究内容或报告结构转成可视化、交互式、图形化或多模态产物。

## 触发后先做什么

1. 判断表达产物类型：frontend UI、prototype、diagram、slides、image/multimodal，或组合产物。
2. 复杂表达结构、多模态链路、前端状态/交互复杂时，先使用 `reasoning-map` 做 Reasoning Gate。
3. 最终生成前必须执行 Preview Gate，先给低成本预览并等待确认或显式标注假设。
4. 复杂预览、关键视觉产物和交付前执行 Review Gate，review 分数必须 >=80；低于 80 先修订并复审。
5. 复杂交互、动画、canvas、Three.js、响应式、渲染或多模态不确定时执行 POC Gate。
6. 浏览器渲染、截图、图片生成、外部 API、多模态服务、构建预览、打包或验证前，按 `development-workflow/references/configuration-readiness-gate.md` 统一确认运行时、API/env 凭据边界、输出路径、验证信号和授权；缺失 required 配置时先停止并给出降级方案。
7. 声称完成前执行 Verification Gate，提供本轮 fresh evidence。

## Artifact Router

```text
Frontend UI / React / HTML / CSS / page / component
  -> references/sop-02-frontend-ui.md

Interactive prototype / low-fi mock / clickable demo
  -> references/sop-03-prototype.md

Mermaid / UML / flowchart / sequence / state / architecture / DFD
  -> references/sop-04-diagram.md

HTML slides / report deck / visual narrative
  -> references/sop-05-html-slides.md

Image prompt / visual generation / reference image analysis / multimodal
  -> references/sop-06-image-generation.md

Verification / screenshot / viewport / slide height / diagram syntax / interaction check
  -> references/sop-07-verification.md
```

## Quality Gates

```text
Reasoning Gate
  -> reasoning-map before complex visual structure, interaction, rendering, or multimodal chains

Preview Gate
  -> low-cost preview before expensive output
  -> forms: ASCII | Mermaid | wireframe | HTML preview | style tile | storyboard | prompt draft

Review Gate
  -> score >=80 before downstream work or final delivery

POC Gate
  -> thin proof for risky interaction, responsive layout, rendering, animation, or generation path

Configuration Readiness Gate
  -> confirm runtime, browser/API/env boundaries, output paths, validation signals, and authorization before rendering, generation, build preview, packaging, or external calls

Verification Gate
  -> fresh evidence: render/build/screenshot/viewport/height/diagram syntax/interaction check
```

## 边界

- 产品方向、PRD、用户场景和验收标准不清时，转入 `product-definition`。
- 架构、接口、数据、状态和验证策略不清时，转入 `technical-design`。
- 通用代码实现、bugfix、测试和交付摘要转入 `implementation-delivery`。
- 深度研究、开源仓库对比和证据包转入 `research`。
- 项目已有设计系统、组件库或表达规范优先；没有时再使用本技能 references 和 templates。

## 资源

- `references/sop-00-intake.md`: 表达产物需求澄清。
- `references/sop-01-reasoning-preview.md`: Reasoning + Preview 门禁。
- `references/sop-02-frontend-ui.md`: 前端 UI 表达。
- `references/sop-03-prototype.md`: 原型表达。
- `references/sop-04-diagram.md`: 图表表达。
- `references/sop-05-html-slides.md`: HTML slides 表达。
- `references/sop-06-image-generation.md`: 图片和多模态表达。
- `references/sop-07-verification.md`: 表达产物验证。
- `references/sop-08-review.md`: Review Gate。
- `references/diagram-examples/`: 图表类型示例库。
- `references/html-slides/`: HTML slides 设计、排版、Mermaid 和高度控制参考。
- `references/image-generation/`: 图片生成提示词、API 和历史构建参考。
- `data/ui-ux-library/`: UI/UX 风格、颜色、字体、产品类型、技术栈和设计系统检索数据。
- `tools/`: HTML 校验、slide height 检查、图片生成和 UI/UX 检索辅助脚本。
