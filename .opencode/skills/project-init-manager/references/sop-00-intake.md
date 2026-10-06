# SOP 00: Intake

## 目标

确认本次是新项目初始化、既有仓补齐，还是初始化完整性审计。该阶段只做只读检查和范围推演，不直接写文件。

## 前置读取

- 本技能 `SKILL.md`。
- 如果目标目录已有 `AGENTS.md`，先读取它。
- 如果目标目录已有 `docs/README.md`，先读取它。
- 如果目标目录是 Git 仓库，检查 `.gitmodules` 是否存在。

## 输入信息

尽量从用户请求、路径和现有文件自动推断；只有影响写入安全时才提问。

- `project_path`: 目标项目目录。
- `project_name`: 项目名，默认来自目录名。
- `project_kind`: 新项目、既有项目补齐、审计。
- `tech_stack`: 已知技术栈；未知时保留为待补充。
- `package_manager`: 已知包管理器；未知时保留为待补充。
- `research_workspace_name`: 研究工作区名，固定默认 `aces-research`。
- `ai_engine_name`: AI 引擎 submodule 名，固定默认 `maop`。
- `opencode_mode`: 仅目录骨架、带本地 skill、带完整 config。
- `submodule_policy`: 是否已有外部仓或需要初始研究工作区 submodule。
- `design_workspace_mode`: 是否建设计仓机制，取值 `required` | `skipped` | `existing` | `audit_only`。由项目特征判定：存在外部系统交互、部署形态或多模块协作为 `required`；单模块脚本、一次性工具、无部署边界实验为 `skipped`；已有独立设计仓为 `existing`；审计既有仓为 `audit_only`。
- `design_repo_url`: 项目层设计仓远端地址；`required` 或 `existing` 时必须明确，未知时不得自行推断。
- `maop_source_mode`: 目标仓库本身是否为 maop 源仓。可由 Git remote 指向 `https://github.com/aces-org-zhuang/maop.git`、项目名为 `maop`、已有 `.opencode/skills/` 且 `.opencode/README.md` 表明 maop-owned OpenCode surface 等信号自动判断。

## 执行步骤

1. 使用 `reasoning-map` 输出初始化影响面，至少覆盖仓库基础、目录职责域、docs、AGENTS、`.opencode`、研究区、submodule、设计仓、验证。
2. 检查目标目录是否存在；不存在时只在用户明确要求创建新文件夹时创建。
3. 检查是否已有 Git 仓库、README、AGENTS、docs、`.opencode`、vendor、guides、scripts、tests，以及是否已有 `vendor/design/`。
4. 识别可能被覆盖的用户文件。已有文件必须读取后合并，不能盲目覆盖。
5. 形成本次 Stage 列表。新项目完整初始化默认进入 Stage 1 到 Stage 9，并在设计仓判定为 `required` 或 `existing` 时加入 Stage 10。
6. 判断是否为 `maop_source_mode`。如果是，`vendor/ai/maop` 从“必建 submodule”降级为“宿主项目消费 maop 时的规划规则”，不得把当前仓库自嵌套为 submodule。
7. 将锁定 submodule 纳入初始化检查：`vendor/research/aces-research` -> `https://github.com/aces-org-zhuang/aces-research.git`。非 `maop_source_mode` 时还必须检查 `vendor/ai/maop` -> `https://github.com/aces-org-zhuang/maop.git`。
8. 判定 `design_workspace_mode` 并写入输出。判定为 `required` 时确认 `design_repo_url`；未确认时不得创建远端仓，也不得猜测 URL。若为 `skipped`，记录原因，说明架构决策改记入 `docs/`。

## 输出

- 初始化模式。
- 已存在结构和缺失结构。
- `design_workspace_mode` 判定结果及依据。
- 本次要读取的 SOP 列表。
- 写操作风险和需要用户确认的点。
- 是否为 maop 源仓模式；若是，明确排除 `vendor/ai/maop` 自嵌套。

## 常见 RED 点

- 目标目录已有大量文件但没有 Git，先不要批量创建目录，先审计现状。
- 已有 `AGENTS.md` 或 `docs/README.md` 时，必须合并规则，不能覆盖。
- 技术栈未知时，目录只能按职责域设计，不生成具体构建/测试命令。
- 如果目标仓已有其他研究区或 AI 引擎路径，先输出迁移/兼容计划，不直接替换。
- 目标仓库本身就是 `maop` 时仍强制添加 `vendor/ai/maop`，会形成自嵌套和 `.opencode` 双源维护。
- 未判定 `design_workspace_mode` 就进入初始化，导致设计仓被静默遗漏或被过度创建。
- 判定为 `required` 但 `design_repo_url` 未确认就自行推断远端地址，或默认创建 GitHub 仓库。
- 已有设计仓时重复创建，产生双源维护。
