# Init Readiness Checklist

执行初始化写操作前检查：

- 已确认目标项目路径。
- 已判断是新项目、既有项目补齐，还是审计。
- 已检查是否存在 Git 仓库。
- 已检查是否存在 `README.md`、`AGENTS.md`、`docs/`、`.opencode/`、`vendor/`。
- 已识别可能被覆盖的用户文件。
- 已完成 reasoning-map 推演。
- 已确定需要执行的 SOP 列表。
- 技术栈未知时，已决定只写职责域规则，不伪造命令。
- `.opencode/opencode.json` 是否生成已有明确依据。
- 研究区锁定为 `vendor/research/aces-research` -> `https://github.com/aces-org-zhuang/aces-research.git`。
- 已判断是否为 maop 源仓模式。
- 普通宿主项目：AI 引擎锁定为 `vendor/ai/maop` -> `https://github.com/aces-org-zhuang/maop.git`。
- maop 源仓模式：不得添加 `vendor/ai/maop`，本仓 `.opencode/skills` 是能力源码目录。
- 已判定 `design_workspace_mode`（`required` / `skipped` / `existing` / `audit_only`）。
- 判定为 `required` 时，`design_repo_url` 已由用户确认；未确认时不得自行推断或创建远端仓。
- 判定为 `skipped` 时，跳过原因已记录，且架构决策改记入 `docs/`。
- 判定为 `existing` 时，确认已有设计仓路径，不重复创建。
- 已确认设计仓不会被 sparse-checkout 裁剪，主仓 CI 不构建它。
