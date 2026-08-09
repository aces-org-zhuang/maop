# SOP 05 - PRD Generation

## Goal

将已确认的问题、场景和需求整理为项目可用的产品定义或 PRD。

## Steps

1. 优先读取并遵循项目已有 PRD 模板；没有模板时使用 `templates/prd.md`。
2. 先执行 Preview Gate，使用 `templates/product-sketch.md` 或项目更合适的低成本预览形式，覆盖问题、角色、Use Case、需求、验收和开放假设。
3. 除非用户明确要求确认、关键产品目标/用户/成功标准无法推断，或继续会改变已确认范围，否则不要等待用户确认草图；记录假设并继续生成 PRD。
4. PRD 正文必须有角色与 Use Case 主轴；功能需求应引用对应角色和 Use Case，避免离散功能堆叠。
5. 若 PRD 使用委派结果，先按 `references/delegation-quality-gate.md` 通过 Synthesis Gate，并用 User/Use Case、Acceptance/Risk、Market/Alternative、Scope/Revision lens 标注每条吸收结论。
6. 保持章节与需求来源可追踪，不把前序分析结论丢失在摘要里。
7. 将功能需求、非功能需求、验收标准、开放问题和依赖分开写。
8. 如果需要原型，只产出 prototype brief；真实界面、图表、slides 或其他表达产物交给 `expression-delivery`。
9. 需要进入 `technical-design` 时，同步生成 Product Handoff Packet：原始输入摘要、角色、Use Case、范围、需求、验收、风险、市场替代、假设、开放问题、已读/复用/拒绝材料、归档/修订状态和 handoff readiness；每个字段按 `references/delegation-quality-gate.md` 字段级吸收规则处理。
10. 输出前运行 `checklists/prd-completeness.md`；如果 PRD completeness、Review Gate 或下游可消费性不达标，按 `development-workflow/references/auto-remediation-gate-loop.md` 自动补齐并复审，最多 7 轮，硬阻断才询问用户。

## Validation

- PRD 能被 technical-design 直接消费。
- PRD 的功能范围能追溯到明确角色和 Use Case。
- Product Handoff Packet 能被 technical-design 直接消费，不要求下游重做产品研究。
- Product Handoff Packet 字段级吸收了已验证委派结果；未通过 Synthesis Gate 的内容未作为确认事实进入下游。
- PRD 前已完成 Preview Gate，或用户明确要求跳过且风险已说明。
- 需求没有混入未经确认的实现方案。
- 开放问题被显式列出，不作为隐含假设进入后续阶段。
