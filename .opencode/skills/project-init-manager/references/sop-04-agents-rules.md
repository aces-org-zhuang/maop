# SOP 04: Agent Rules

## 目标

生成根 `AGENTS.md` 和 `docs/AGENTS.md`，让后续 LLM 进入项目时先理解项目定位、边界、目录、验证、文档反哺和研究区隔离规则。

## 根 AGENTS.md 内容结构

根 `AGENTS.md` 建议包含：

1. 语言规则。
2. 项目定位。
3. 产品或工程范围。
4. 关键开发规则。
5. reasoning-map 推演优先规则。
6. 文档规则和反哺机制。
7. 失效模式、调试记录、实现证据规则。
8. 目录职责域和顶层目录说明。
9. 常用命令；未知命令写 `待补充`。
10. 技术栈注意事项。
11. OpenCode 本地配置说明。
12. 研发流水线引导：需求用 `product-definition`，设计用 `technical-design`，实现/验证/交付用 `implementation-delivery`；复杂影响面用 `reasoning-map`，深度研究用 `research`。
13. 全链路质量保障：Reasoning Gate、Preview Gate、Review Gate、POC Gate、Verification Gate、Confidence Gate 和 Stop Rule。
14. Todo、委派和输出预算：复杂任务、并行委派多个子代理执行、验证、提交/PR 或 submodule 操作前先更新 todo；对外统一使用“委派子代理执行”；默认 compact 输出，full packet 只在高风险、跨阶段、提交/PR 或用户要求时展开。
15. 写入、验证和 submodule budget：先审计再写入，优先最小文件集；验证按风险匹配；submodule 写操作需授权，审计/轻量补齐不默认 add/update。
16. Submodule 提交与 PR 规则：修改 submodule 内容时，submodule 仓库必须独立分支、提交、推送并创建 PR；主仓 PR 只更新远端可见的 submodule 指针并关联 submodule PR。

## 通用治理规则边界

`AGENTS.md` 初始化时只生成通用治理元规则，不复制某个既有项目的业务特化细则。应保留的是规则生产和反哺机制，而不是具体技术栈实现约束。

应默认保留：

- 复杂问题、架构影响面、docs 体系、研究区、submodule 和 `.opencode` 规划前使用 `reasoning-map`。
- 目录职责域优先于具体目录名。
- 技术栈命令来自真实配置、源码或用户确认，不猜测。
- 复杂任务和多步骤交付前维护 todo；每个子代理委派、验证动作、提交/PR 和 submodule 操作应有对应 todo。
- 默认 compact 输出，不把模板、packet、验证脚本或临时验证手段写成长期规则。
- 写入、验证、外部调用和 submodule 操作按预算执行，优先低成本、最小变更、可回滚路径。
- 新增规则后同步评估根 `AGENTS.md`、`docs/AGENTS.md`、`docs/README.md` 和相关索引。
- 代码实现后评估是否写入 `docs/evidences/`。
- 修复可复用问题后评估是否写入 `docs/failure-modes/`。
- 复杂调试过程评估是否写入 `docs/debugs/`。

不应默认复制：

- 某个既有项目的具体前端、后端、运行时、打包、i18n、Workbench、MCP、IPC 或平台抽象细则。
- 某个既有项目的具体命令、目录深层结构和历史 failure/debug/evidence 记录。
- 本项目的一次性验证命令、`opencode run` 回放 prompt、PR 调试过程或临时 CLI wrapper。
- 把所有任务都强制委派子代理执行、强制 full packet 或强制多轮自动修复的规则。
- `profiles` 或 `overlays` 机制；本技能保持单一通用 SOP，技术栈细节在目标项目确认后写入对应 docs 和 AGENTS。

## docs/AGENTS.md 内容结构

`docs/AGENTS.md` 只约束 docs 写作和演进，不重复全部项目开发细节：

1. 文档语言规则。
2. `docs/`、`guides/`、研究区边界。
3. 编辑 docs 前的读取顺序。
4. 写作规则。
5. reasoning-map 前置规则。
6. 索引同步规则。
7. failure/debug/evidence 记录规则。
8. token 与输出预算规则。
9. todo 前置和委派子代理执行规则。

## 执行步骤

1. 如果已有 `AGENTS.md`，读取并保留用户规则，增量合并初始化治理规则。
2. 根据 `sop-02-directory-governance.md` 的目录职责域生成项目结构说明。
3. 根据 `sop-03-docs-system.md` 写入文档边界和反哺机制。
4. 根据 `sop-06-research-workspace.md` 写入研究区必建和隔离规则。
5. 写入研发流水线引导，帮助后续 agent 在需求、设计、实现、验证和交付之间选择正确 maop 技能。
6. 写入 todo 前置、委派子代理执行、Output Budget、写入/验证/submodule budget 等轻量治理元规则；保持简短，不把完整 skill SOP 复制进 `AGENTS.md`。
7. 写入全链路质量保障，要求真实脚本/构建/高成本实现前先 reasoning-map 推演预检，高成本产物前做 Preview Gate，必要节点 Review Gate >=80，高风险实现先 POC，完成声明前 fresh verification，90%+ 置信度必须有 eval 和残余风险说明。
8. 写入 Submodule 提交与 PR 规则，要求 submodule 内容变更必须先走 submodule 仓库分支和 PR，主仓只提交远端可见的 submodule 指针并在 PR 中关联 submodule PR。
9. 技术栈命令未知时保留 `待补充`，不要猜测。
10. 检查是否误复制既有项目特化规则；如果发现，只保留可泛化的治理元规则。
11. 生成或合并 `docs/AGENTS.md`。

## 模板

- `templates/AGENTS.md.template`
- `templates/docs-AGENTS.md.template`

## 常见 RED 点

- 根 `AGENTS.md` 过细，复制大量架构细节，导致默认上下文过重。
- `docs/AGENTS.md` 与根规则冲突。
- 新增文档规则后没有同步到 docs 局部规则。
- 没有写明研究资料不得进入主仓 `docs/`。
- 把既有项目的技术栈细则或历史记录当成通用初始化默认规则。
- 把 Preview Gate 误写成必须 ASCII，或把 POC Gate 误写成所有任务必经。
- 主仓 PR 指向 submodule 本地 commit，或 submodule 内容变更没有对应 submodule PR。
- 把一次性验证命令、临时回放 prompt 或 PR 调试过程写进长期 `AGENTS.md`。
- 把所有任务都强制维护 todo、委派子代理执行、展开 full packet 或多轮自动修复。
- 写入、验证或 submodule 操作超出本次任务必要预算。
