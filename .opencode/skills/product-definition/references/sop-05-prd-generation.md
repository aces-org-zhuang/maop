# SOP 05 - PRD Generation

## Goal

将已确认的问题、场景和需求整理为项目可用的产品定义或 PRD。

## Steps

1. 优先读取并遵循项目已有 PRD 模板；没有模板时使用 `templates/prd.md`。
2. 先执行 Preview Gate，使用 `templates/product-sketch.md` 或项目更合适的低成本预览形式，覆盖问题、用户、场景、需求、验收和开放假设。
3. 等待用户确认草图；如果用户要求继续且草图中仍有假设，必须在 PRD 中显式保留这些假设。
4. 保持章节与需求来源可追踪，不把前序分析结论丢失在摘要里。
5. 将功能需求、非功能需求、验收标准、开放问题和依赖分开写。
6. 如果需要原型，只产出 prototype brief；真实界面实现交给 `frontend-design`。
7. 输出前运行 `checklists/prd-completeness.md`。

## Validation

- PRD 能被 technical-design 直接消费。
- PRD 前已完成 Preview Gate，或用户明确要求跳过且风险已说明。
- 需求没有混入未经确认的实现方案。
- 开放问题被显式列出，不作为隐含假设进入后续阶段。
