# SOP 06 - Fresh Verification

## Goal

用本轮新鲜证据支撑完成声明。

## Steps

1. 明确每个完成声明需要什么命令或检查证明。
2. 使用 Test Surface lens 确认验证覆盖：自动测试、类型检查、lint、构建、smoke、手工步骤、截图检查或无法运行原因。
3. 运行与风险匹配的完整验证。
4. 阅读完整输出和退出码，记录失败、跳过或无法运行原因。
5. 必要时使用 Evidence Extraction lens 把输出整理为 claim-to-evidence 映射，但主 agent 负责结论。
6. 若验证失败，报告真实状态并修复或说明阻塞。
7. 只有验证通过或风险被明确接受后，才宣称对应范围完成。

## Validation

- 交付摘要包含实际运行的验证和结果。
- 不使用“应该”“看起来”“大概”替代证据。
- Delivery Evidence Packet 中每条完成声明都有 fresh evidence 或明确的未验证状态。
- delegated evidence 已经 synthesis，不把未复核的 subagent 输出当成事实。
