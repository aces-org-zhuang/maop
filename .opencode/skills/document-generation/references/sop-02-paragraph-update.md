# SOP-02 Paragraph Update

## Goal

按 paragraph_id 局部更新并自动 validate。

## Steps

1. 读取 `doc_cli.py next-step <directory>` 返回的当前步骤 schema。
2. 构建更新 JSON（`step_id`、`blocks`、`next_step`）。
3. 调用 `python scripts/doc_cli.py update <directory> <json-or-file>` 执行更新。
4. CLI 校验块类型、必填字段、枚举值和下一步骤，并自动 validate。

## Output

更新后的段落 + 验证结果。
