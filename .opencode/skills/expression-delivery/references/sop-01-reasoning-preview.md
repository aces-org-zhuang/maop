# SOP 01: Reasoning and Preview

1. 复杂视觉结构、交互状态、渲染链路、多模态生成或跨产物依赖前，先用 `reasoning-map` 做 Reasoning Gate。
2. 最终生成前必须做 Preview Gate。
3. Preview 形式按产物选择：ASCII、Mermaid、wireframe、HTML preview、style tile、storyboard、prompt draft 或表格草案。
4. 只有用户明确要求确认、高成本外部调用、required 配置/授权缺失或关键偏好无法推断时，才等待用户确认；其他情况记录假设并继续完整生成。
5. Reasoning Gate 不替代 Preview Gate，Preview Gate 不替代 Verification Gate。
