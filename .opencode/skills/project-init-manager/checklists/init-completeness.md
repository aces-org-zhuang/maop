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
- `.opencode/opencode.json` 存在，并按当前模式引用 OpenCode 能力面。
- 普通宿主项目：`.opencode/opencode.json` 引用 `../vendor/ai/maop/.opencode/skills`，并将 `references.maop-opencode` 指向 `../vendor/ai/maop/.opencode`。
- maop 源仓模式：`.opencode/opencode.json` 引用本仓 `./skills`，并将 `references.maop-opencode` 指向当前 `.opencode` 目录。
- `vendor/research/aces-research/index.md` 存在，或已规划锁定 submodule 写操作。
- 普通宿主项目：`vendor/ai/maop` 存在或已规划锁定 submodule 写操作，并已规划 sparse-checkout 只检出 `.opencode` 和 `README.md`。
- maop 源仓模式：已明确排除 `vendor/ai/maop` 自嵌套，并说明本仓 `.opencode/skills` 是能力源码。
- 项目 `.opencode` 与 maop 能力面的边界已记录。
- 如果使用 submodule，`.gitmodules` 与实际路径一致。
- 常用命令来自真实配置；未知命令标记为 `待补充`。
- 未闭环 RED 点已写入最终输出或对应 roadmap/debug 记录。
