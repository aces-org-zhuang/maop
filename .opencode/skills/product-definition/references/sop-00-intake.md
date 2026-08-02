# SOP 00 - Intake

## Goal

确定本次产品定义工作的范围、输入可信度、已有材料和下一阶段。

## Steps

1. 读取用户输入，保留原始表述中的目标、痛点、约束、示例和假设。
2. 按 `development-workflow/references/knowledge-handoff-gate.md` 执行 Read Gate：先查已有 PRD、需求模板、路线图、任务记录、用户反馈、`docs/README.md`、相关 docs 索引和研究材料引用，不默认读取整个 `docs/`。
3. 建立 Reuse Ledger，记录已读材料、可复用结论、已拒绝重复研究路径、仍需补证的 RED 点。
4. 判定请求类型：完整产品定义、PRD 生成、需求修订、验收标准补齐、轻量竞品分析或 prototype brief。
5. 若用户只要求一个窄产物，直接路由到对应 SOP，不强行执行完整流程。
6. 若缺少完成当前阶段的必要信息，用结构化问题一次性询问；若可从现有材料推断，不把可验证事实转成问题。

## Outputs

- 当前请求类型。
- 已有材料路径或输入摘要。
- Reuse Ledger：已读、已复用、已拒绝、Open RED。
- 下一阶段 SOP。
- 需要用户确认的真实缺口。

## RED Points

- 把用户提出的实现方案当成产品需求本身。
- 在未确认用户和成功标准前生成完整 PRD。
- 将普通产品分析升级为长期 research 课题，造成不必要的工作区污染。
