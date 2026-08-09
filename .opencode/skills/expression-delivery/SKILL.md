---
name: expression-delivery
description: 必须用于表达产物交付，包括前端 UI、HTML/CSS/React 页面、交互原型、Mermaid/UML/架构图/时序图/状态图、HTML slides、视觉报告、图片生成提示词和多模态表达。用户要求生成、预览、优化、检查或验证 UI、prototype、diagram、slides、image、visual artifact 时优先使用本技能；不要用于产品定义、架构主设计或通用代码实现。
---

# Expression Delivery

本技能是 maop 的表达产物流水线入口。它把已确认的需求、设计、研究内容或报告结构转成可视化、交互式、图形化或多模态产物。

## Output Budget Rule

- 默认 compact 输出：只说明 artifact 类型、预览形式、关键假设、验证边界和下一步。
- 不默认生成完整 HTML/slides/image/API 调用；full artifact 仅在用户明确要求、交付阶段或下游必须消费时生成。
- 简单 diagram、单条图片 prompt 或局部 UI 建议不展开完整 review/verification packet。

## Verification Budget Rule

- 按产物风险选择最小验证：diagram 优先 syntax/static review，frontend/prototype 才做响应式和交互，slides 才做高度/viewport，image/multimodal 先做 prompt review。
- 浏览器、截图、构建、打包、外部 API 或多模态生成只在用户授权、配置和成本边界明确后执行。

## Auto-Remediation Budget Rule

- 普通表达产物默认最多 1-2 轮自动修复。
- 高风险交付、用户明确要求高质量或验证失败影响交付时才扩大轮次。
- 视觉偏好冲突、品牌风格不确定或外部调用成本不清时先请求确认，不用自动修复消耗轮次。

## 触发后先做什么

1. 判断表达产物类型：frontend UI、prototype、diagram、slides、image/multimodal，或组合产物。
2. 复杂表达结构、多模态链路、前端状态/交互复杂时，先使用 `reasoning-map` 做 Reasoning Gate。
3. 多产物组合、前端 UI、slides、截图/验证、多轮修复、外部图片/多模态调用前，先更新 todo；每个产物、viewport、验证动作、修复轮次和外部调用都应有对应 todo。单个小图表、单条 prompt 或简单视觉建议可跳过。
4. 最终生成前必须执行 Preview Gate；除非用户明确要求确认、高成本外部 API/多模态调用、required 配置/授权缺失，或品牌/风格关键偏好无法推断，否则记录假设并继续生成。
5. 复杂预览、关键视觉产物和交付前执行 Review Gate，review 分数必须 >=80；低于 80 按 `development-workflow/references/auto-remediation-gate-loop.md` 自动修订并复审，但普通表达产物默认只做 1-2 轮自动修复。
6. 复杂交互、动画、canvas、Three.js、响应式、渲染或多模态不确定时执行 POC Gate。
7. 浏览器渲染、截图、图片生成、外部 API、多模态服务、构建预览、打包或验证前，按 `development-workflow/references/configuration-readiness-gate.md` 统一确认运行时、API/env 凭据边界、输出路径、验证信号和授权；缺失 required 配置时先停止并给出降级方案。
8. 声称完成前执行与产物风险匹配的 Verification Gate；简单文本/diagram 可用静态证据，frontend/slides/多模态再升级到浏览器、截图、构建或外部验证。

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

Auto-Remediation Gate Loop
  -> ordinary expression artifacts default to 1-2 repair rounds
  -> expand only for high-risk delivery, explicit high-quality requests, or blocking verification failures
  -> stop on missing required config/authorization, high-cost external calls needing approval, user style tradeoff, or 2 no-progress rounds

Configuration Readiness Gate
  -> confirm runtime, browser/API/env boundaries, output paths, validation signals, and authorization before rendering, generation, build preview, packaging, or external calls

Verification Gate
  -> risk-matched fresh evidence: static syntax review for simple diagram/text; render/build/screenshot/viewport/height/interaction only when artifact risk requires it
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
