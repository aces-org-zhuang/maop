# SOP-01 CLI-Driven Generation

## Goal

按初始化时定义的步骤计划，逐步提交经过 schema 约束的 JSON 内容到目标文档。

## Steps

1. 初始化时通过 `--steps-plan <json-or-file>` 提交步骤数组。
2. 读取 `python scripts/doc_cli.py next-step <directory>` 返回的当前步骤、允许块、schema 和下一步。
3. 构建符合当前 schema 的更新 JSON：`{"step_id":"...","blocks":[...],"next_step":"..."}`。
4. 调用 `python scripts/doc_cli.py update <directory> <json-or-file>` 执行提交；CLI 校验后自动推进到 `next_step`。
5. 记录当前状态和产物。

步骤计划示例：

```json
[
  {
    "step_id": "problem-definition",
    "instruction": "记录现象、预期、实际和复现条件",
    "next_step": "evidence",
    "allowed_blocks": ["heading", "paragraph", "table"],
    "schema": {
      "type": "object",
      "required": ["id", "type", "content"],
      "properties": {"type": {"enum": ["heading", "paragraph", "table"]}}
    }
  }
]
```

## Output

当前轮次 JSON + 最终文档草稿。
