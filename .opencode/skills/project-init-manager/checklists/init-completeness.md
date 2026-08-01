# Init Completeness Checklist

初始化完成后检查：

- 根 `README.md` 存在，并指向 docs 和研究区入口。
- 根 `AGENTS.md` 存在，并包含项目定位、目录职责域、文档规则、研究区规则和反哺机制。
- 根 `AGENTS.md` 的项目结构覆盖所有已创建顶层目录，不只列源码目录。
- `docs/README.md` 存在，并保持短入口。
- `docs/AGENTS.md` 存在，并只约束 docs 写作和演进。
- `docs/07-llm/llm-reading-order.md` 存在或已记录暂缓原因。
- `docs/failure-modes/index.md` 存在。
- `docs/debugs/index.md` 存在。
- `docs/evidences/index.md` 存在。
- `guides/` 存在或已记录暂缓原因。
- `.opencode/README.md` 存在。
- `.opencode/skills/`、`.opencode/agents/`、`.opencode/commands/` 存在。
- `vendor/research/aces-research/index.md` 存在，或已规划锁定 submodule 写操作。
- `vendor/ai/maop` 存在，或已规划锁定 submodule 写操作。
- 项目仓 `.opencode` 与 `vendor/ai/maop/.opencode` 的边界已记录。
- 如果使用 submodule，`.gitmodules` 与实际路径一致。
- 常用命令来自真实配置；未知命令标记为 `待补充`。
- 未闭环 RED 点已写入最终输出或对应 roadmap/debug 记录。
