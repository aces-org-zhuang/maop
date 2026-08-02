# SOP 06: Image Generation

1. 先确认用途、受众、画幅、风格、主体、约束和禁止内容。
2. 有参考图时先分析构图、色彩、材质、光照、镜头和风格，不复制受版权保护的独特表达。
3. 先输出 prompt draft 或 storyboard preview；高成本外部生成、required 配置/授权缺失、用户明确要求确认或关键风格偏好无法推断时才等待确认，否则记录假设并继续生成或迭代。
4. 对多模态链路标注输入、输出、失败模式和回退方案。
5. 验证生成结果是否满足主体、文本、构图、品牌安全和用户约束；不达标时按 `development-workflow/references/auto-remediation-gate-loop.md` 自动修正 prompt/storyboard/参数并复验，最多 7 轮。高成本外部生成仍受 Configuration Readiness Gate 和授权边界约束。
