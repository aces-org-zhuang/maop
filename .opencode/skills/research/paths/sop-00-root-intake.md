# SOP 00: Root Intake

所有 discovery / research / innovation 请求都必须先创建或续接 `research_root`。

## Steps

1. 确认 `research_workspace = vendor/research/aces-research` 存在且可读写。
2. 读取 `{research_workspace}/index.md`，匹配用户指定课题或最近 active topic。
3. 如果是新请求，生成 `{research_slug}` 并创建 `{research_root} = {research_workspace}/topics/<research_slug>`。
4. 创建或更新 `{research_root}/README.md`，记录状态、当前 path、冻结点和下一步。
5. 写入 `{research_root}/intake/request.md`，保留用户原始请求、目标、范围和约束。
6. 进入 `sop-01-pipeline-routing.md` 选择本次最小必要 path。

## Rules

- 不把新材料写入主仓 `docs/` 或主仓 `research/`。
- 只执行用户本次请求需要的 path。
- 若无法初始化 research workspace，标记 blocked，不回退写入主仓。
