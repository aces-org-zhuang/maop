# SOP 02: Directory Governance

## 目标

先定义目录职责域，再根据技术栈映射到具体目录名。初始化 skill 不固定某一种技术栈目录，而是建立可演进的目录设计规则。

## 目录职责域

新项目至少要明确这些职责域，即使某些域暂时没有具体目录：

- 源码域：应用源码、库源码、入口代码。
- 构建域：构建脚本、打包配置、构建产物规则。
- 安装域：依赖安装、环境准备、本地 bootstrap。
- 测试域：单测、集成测试、端到端测试、fixtures。
- 配置域：工具配置、环境变量样例、CI 配置。
- 文档域：长期稳定项目知识。
- 过程记录域：非研究工程记录、调试、失效模式、实现证据。
- 研究域：研究过程、论文、开源项目对比、证据包。
- AI 引擎域：独立演进的 AI engine、agent runtime、engine-side `.opencode`、skills/agents/commands 和相关能力代码。
- 外部依赖域：vendor 源码、参考仓、submodule。
- 资源域：静态资源、运行资源、样例数据。
- 自动化域：安装、验证、生成、迁移、发布、诊断脚本，以及 OpenCode 本地组件。

## 技术栈映射规则

1. 先写明职责域，再选择目录名。
2. 技术栈有强约定时沿用强约定，例如 Go 的 `cmd/`、Rust 的 `crates/`、Node monorepo 的 `apps/` 和 `packages/`。
3. 技术栈未知时，使用中性目录名，例如 `src/`、`tests/`、`scripts/`、`docs/`、`guides/`、`vendor/`、`resources/`、`data/`。
4. 允许 co-located tests，但必须在开发规则中写清楚测试文件命名和运行方式。
5. 构建产物不得混入源码域；如果技术栈默认输出在源码附近，必须由 `.gitignore` 保护。

## 顶层目录推荐职责

- `docs/`: 长期稳定知识和规则。
- `guides/`: 非研究类阶段性工程记录、PR 记录、历史输出。
- `vendor/`: 外部仓库、研究工作区、供应商资源和 submodule。
- `vendor/research/aces-research/`: 锁定研究工作区 submodule。
- `.opencode/`: OpenCode 配置说明；maop 源仓模式下还是 AI 能力源码目录。
- `vendor/ai/maop/`: 普通宿主项目的锁定 AI 引擎 submodule；maop 源仓模式除外。
- `scripts/`: 可重复执行的安装、验证、生成、迁移、发布、诊断脚本。
- `.opencode/skills/`、`.opencode/agents/`、`.opencode/commands/`: 普通宿主项目仅在确有本地覆盖时创建；maop 源仓模式下属于能力开发面。
- `resources/` 或 `assets/`: 运行资源或静态资源，按项目语义选择。
- `data/`: 样例数据、内置数据或测试数据，必须说明是否可公开、可打包。
- `tests/`: 跨模块测试；若测试 co-located，则可不创建但要记录规则。

## 执行步骤

1. 根据 intake 结果列出项目实际需要的职责域。
2. 为每个职责域选择目录名或说明暂不落盘。
3. 创建必要顶层目录，避免过度细分业务源码。
4. 在根 `AGENTS.md` 和 `README.md` 中记录所有已创建顶层目录职责；不能只列 `src/` 或源码目录。
5. 如果创建 docs 子目录，同步 `docs/README.md` 或子目录 README。

## 目录新增规则

新增顶层目录时必须回答：它保存什么，谁消费它，新增/删除/移动时同步哪个 README、index 或规则文件。

## 常见 RED 点

- 只按流行模板生成目录，但没有说明职责域。
- 把研究资料放入 `docs/`。
- 把外部参考仓普通 clone 到主仓。
- 把 maop 的 `.opencode` 内容复制到项目仓 `.opencode`，导致职责混淆。
- 把构建产物、缓存或下载包纳入源码目录。
- 初始化时创建了多个顶层目录，但 `AGENTS.md` 的项目结构只记录部分目录，导致后续 LLM 无法索引治理边界。
