---
name: submodule-manager
description: Git submodule 管理技能。用户提供外部代码仓地址，或要求引入、更新、审计、修复、移除 submodule 时使用。本技能聚焦 Git submodule 运行机制：从仓库 URL 和 Git 状态自动解析可得信息，生成最小操作计划，执行或指导 `git submodule add/update/sync/status/diff`，并在写操作前确认授权。不要把可由仓库地址、`.gitmodules` 或 Git 命令解析的信息转成问题。
---

# Submodule Manager

本技能用于按 Git submodule 的真实机制管理外部代码仓。它应先利用用户提供的代码仓地址和 Git 命令解析事实，再决定是否需要向用户确认。不要把当前会话偏好、项目版图枚举或价值评审模板固化为 submodule 的必要流程。

## 基本原则

- 仓库地址优先：如果用户提供了 repo URL，先解析 URL 和远端信息。
- Git 事实优先：优先读取 `.gitmodules`、`git submodule status --recursive`、`git diff --submodule`、`git status --short`。
- 自动解析优先：项目名、host、推荐目录名、现有冲突、当前 pinned commit、远端 refs 等能从 Git 或 URL 得到的信息，不向用户询问。
- 多平台兼容：GitHub、AtomGit、Gitee、GitLab、自建 Git 服务和本地 Git 路径都按 Git URL 处理，平台差异只作为 `platform_hint` 和诊断信息。
- 写操作授权：会修改 `.gitmodules`、Git index、submodule checkout 或 pinned commit 前，向用户确认执行授权。
- 写操作前置确认：执行 `submodule add/update/sync/deinit/rm` 或 pinned commit 写入前，按 `development-workflow/references/configuration-readiness-gate.md` 一次性确认 repo URL、path、target ref、认证边界、planned_commands、validation_commands 和写入授权；不要在执行过程中临时索要配置。
- 路径规范：新增 submodule 前必须按主仓路径规范生成完整 `proposed_path`。不能把路径设计交给用户临场决定。
- 主仓索引：submodule 不能只是孤岛目录。主仓必须记录子仓路径、边界、用途、构建/验证入口和消费关系。
- 文档最小化：只有 submodule 机制、命令、路径、边界或验证规则发生长期变化时才更新 docs；不要把每次引入的主观价值评审写成长期规则。

## 触发后先做什么

1. 读取仓库根目录 `AGENTS.md` 和 `docs/README.md`。
2. 如果存在，读取 `docs/02-development/git-submodules.md`。
3. 检查 `.gitmodules` 是否存在。
4. 执行或建议执行只读 Git 检查：

```bash
git status --short
git submodule status --recursive
git diff --submodule
```

5. 如果用户提供了 repo URL，解析协议、host、owner、repo、`platform_hint` 和推荐目录名，并按需使用只读远端查询：

```bash
git ls-remote --symref <repo-url> HEAD
git ls-remote --tags <repo-url>
```

只读检查和远端元数据查询不需要用户授权。写操作前必须完成 Configuration Readiness Gate 并确认授权。

## 内部记录结构

使用下面的内部记录组织事实。字段应优先自动填充；只有无法从 URL、Git 状态、远端元数据或已有 docs 解析，且该缺口会影响操作正确性时，才向用户确认。

```text
SubmoduleOperationRecord
- operation: add | update | audit | repair | remove
- repository_url: 用户提供或 .gitmodules 中记录的 URL
- url_scheme: https | ssh | file | local-path | unknown
- repo_host: 从 URL 解析的 host
- platform_hint: github | atomgit | gitee | gitlab | self-hosted | local | unknown
- repo_owner: 从 URL 尽力解析的 owner/group
- repo_name: 从 URL 解析的仓库名
- current_path: 已存在 submodule 的路径
- proposed_path: 根据主仓路径规范、已有 .gitmodules、主仓索引和消费场景推导的完整主仓路径
- current_ref: 当前 pinned commit 或状态
- target_ref: 用户指定、远端解析或计划采用的 commit/tag/branch
- default_branch: 远端 HEAD 指向的默认分支
- existing_status: .gitmodules/status/diff 中观察到的状态
- conflict: none | path-exists | url-mismatch | dirty-submodule | uninitialized | unknown
- planned_commands: 将执行的 Git 命令
- validation_commands: 执行后验证命令
- docs_update_needed: yes | no | uncertain
- execution_permission: plan-only | allowed | cancelled
```

## 多平台 URL 解析

submodule 主流程依赖 Git 协议，不依赖平台 Web API。解析 URL 的目的是生成路径、诊断认证问题和减少不必要提问。

优先识别这些 URL 形态：

```text
HTTPS: https://<host>/<owner>/<repo>.git
HTTPS: https://<host>/<owner>/<repo>
SSH:   git@<host>:<owner>/<repo>.git
SSH:   ssh://git@<host>/<owner>/<repo>.git
File:  file:///path/to/repo
Local: ../relative/path/to/repo 或 E:\path\to\repo
```

`platform_hint` 只用于提示和诊断，不改变 Git 主流程：

```text
github.com -> github
atomgit.com -> atomgit
gitee.com -> gitee
gitlab.com -> gitlab
其他 host -> self-hosted
file:// 或本地路径 -> local
```

解析失败时，不要直接放弃。先保留原始 URL，使用 `git ls-remote <repo-url>` 验证 Git 是否可访问；只有 Git 也无法识别时，再询问用户修正 URL。

## 认证与凭据边界

不同平台的认证方式不同，但 skill 不管理 token。遵循这些规则：

- 不要求用户粘贴 token、personal access token、密码或 SSH 私钥。
- 不把任何凭据写入 `.gitmodules`、docs、evidence 或 skill 输出。
- HTTPS 私有仓库依赖本地 Git credential helper、系统凭据管理器或已配置的认证环境。
- SSH 仓库依赖本地 SSH key、agent 和 `known_hosts`。
- AtomGit、Gitee 或自建 Git 服务如需企业内网、代理或证书配置，只报告 Git 命令错误并提示用户检查本地 Git 访问能力。

远端查询失败时，按错误类型诊断：

- authentication failed / permission denied：本地 Git 凭据或 SSH key 不可用。
- repository not found：URL、权限或仓库可见性异常。
- could not resolve host：网络、DNS、代理或平台 host 不可达。
- SSL certificate problem：本地证书链或企业证书配置异常。
- protocol not supported：URL scheme 不适合 Git submodule。

诊断结论应基于 Git 命令输出，不要猜测平台状态。

## 子仓克隆路径策略

新增 submodule 时必须给出明确路径。路径由主仓规范决定，用户不需要为常规引入设计目录。

路径决策优先级：

1. 已存在 submodule：使用 `.gitmodules` 中已有 path，不重新推导。
2. 主仓已有 `docs/02-development/submodules-index.md` 记录：沿用索引登记的 path。
3. 新增长期 submodule：按“规范路径矩阵”生成 path。
4. 临时或一次性 submodule：按 `guides/vendor/<purpose>/<repo_name>` 生成 path，并在索引中标记临时用途或说明不登记原因。
5. 用户提出自定义路径：作为例外处理，必须说明为什么规范路径不适用，并把例外原因写入主仓索引。

如果已有 submodule 路径不符合当前规范，不要只改 docs 或索引 path。先保持索引 path 与 `.gitmodules` 一致，并输出迁移计划；真正迁移路径需要修改 `.gitmodules`、Git index 和工作区目录，必须单独确认授权。

规范路径矩阵：

```text
vendor/runtime/<repo_name>    运行时、打包、二进制或外部可执行资源
vendor/assets/<repo_name>     图像、字体、模板等资源型子仓
vendor/harness/<repo_name>    MCP、Workbench、commands、verifier、agent harness 或协议/任务编排相关子仓
vendor/design/aces-design     项目层设计仓（架构即代码，LikeC4 模型）；一仓一项目，不得多项目共用
vendor/research/aces-research   研究工作区 submodule 根；课题内参考仓必须放在 `topics/<slug>/repos/<repo_name>` 下，不得放在该根目录
vendor/guides/<repo_name>     阶段性验证、一次性调研或临时方案材料
vendor/external/<repo_name>   无法归类但确认需长期保留的外部仓；必须写明原因
```

`repo_name` 使用 URL 中的仓库名，去掉结尾 `.git`。平台和 owner 信息不进入路径层级，统一记录到 `docs/02-development/submodules-index.md` 的 `url` 或 `notes` 字段，避免目录过深。

如果计划使用 `vendor/external/<repo_name>`，输出必须说明为什么无法归入其他规范目录，并把例外原因写入主仓索引。

## 主仓-子仓边界契约

每个长期 submodule 都需要在主仓侧留下索引，避免外部仓库变成没人知道如何构建、验证或消费的孤岛目录。

主仓索引至少记录：

- `path`：submodule 在主仓中的路径。
- `url`：`.gitmodules` 中的外部仓库地址。
- `pinned_ref`：主仓当前记录的 submodule commit。
- `boundary`：主仓和子仓的职责边界，说明哪些文件由子仓维护，哪些集成/包装由主仓维护。
- `consumer`：主仓中谁消费该 submodule，例如脚本、资源打包、Workbench 数据、MCP 配置、研究材料或文档引用。
- `build_entry`：子仓自身构建、安装或生成命令；如果主仓不构建它，写明 `none` 和原因。
- `validation_entry`：主仓验证该 submodule 可用的命令或人工检查。
- `update_policy`：更新方式，例如固定 commit、跟踪 tag、手动升级。

统一 submodule registry 是 `docs/02-development/submodules-index.md`。新增长期 submodule 时必须更新该索引，而不是把信息散落在对话里。

## 何时向用户确认

只在这些情况下提问：

- 用户未提供 repo URL，且当前任务需要一个具体外部仓库。
- 按规范推导出的目标路径有冲突，或只能落到 `vendor/external/` 例外路径。
- 用户要求更新但没有指定哪个 submodule 或目标 ref。
- 远端查询失败，无法确定目标 ref，且继续执行会改变 pinned commit。
- submodule 内部存在未提交改动，更新或修复可能覆盖状态。
- 即将执行写操作，例如 `git submodule add`、checkout 新 ref、删除 submodule、修改 `.gitmodules`。

不要询问这些可自动解析的信息：repo 名称、host 类型、默认目录名、是否存在 `.gitmodules`、当前 submodule status、当前 pinned commit、远端 HEAD、远端 tag 列表。

## 设计仓 submodule 的特殊规则

设计仓（架构即代码）除遵循通用规则外，还必须满足：

- **一仓一项目**。禁止把多个项目的设计放进同一个被多个项目引用的设计仓。gitlink 记录的是子仓 HEAD commit，与实际使用哪个子目录无关；一个设计仓被 N 个项目引用后，任意提交都会迫使 N 个项目仓各开一个 PR。
- **不得对设计仓启用 sparse-checkout**。LikeC4 CLI 需要完整工作区才能 `validate` 与 `build`；只检出会导致跨文件 `include` 目标缺失而构建失败。这一点与 maop submodule 相反——maop 需要 sparse-checkout，设计仓不能。
- **`build_entry` 写 `none`**。主仓不构建设计仓，构建在设计仓自身 CI。主仓 CI 若需感知设计模型，只做只读检出（`submodules: recursive`），不执行 `likec4 validate` 或 `build`。
- **资产边界**。需与代码同一个 PR 的设计内容（模块划分、接口草案、实现级契约）留在主仓 `docs/`，不进入设计仓。设计仓承载跨 PR 生命周期的架构资产。
- **更新策略需显式声明**。设计仓发版后由主仓开 PR 更新指针，因为 gitlink 不会自动跟随。
- 全局层聚合仓（如 `aces-architecture`）**不由主仓引用**，独立建设与发布；它反向聚合各项目设计仓，方向与 submodule 依赖相反，无循环依赖。

设计仓的适用判定、仓结构与 MCP 配置见 `project-init-manager/references/sop-10-design-workspace.md`；架构建模细节见 `architecture-design` 技能。

## 新增 submodule

当用户给出 repo URL 后，先自动形成计划：

1. 从 URL 得到 `repo_name`、`platform_hint` 和 `repo_owner`，按主仓路径规范生成完整 `proposed_path`。
2. 检查 `proposed_path` 是否已存在。
3. 查询远端 HEAD 和 tags，确定默认分支和可选 ref。
4. 检查 `.gitmodules` 中是否已有相同 URL 或相同路径。
5. 输出计划：目标路径、目标 ref、将执行的命令、验证命令。
6. 检查 `docs/02-development/submodules-index.md` 是否已有记录；没有则把新增索引纳入计划。
7. 写操作前确认授权。

推荐命令形态：

```bash
git submodule add <repo-url> <path>
git submodule status --recursive
git diff --submodule
git status --short
```

如果用户指定 tag 或 commit，添加后进入 submodule checkout 指定 ref，再回到主仓库确认 pinned commit diff。

## 更新 submodule

更新已有 submodule 时，先解析当前状态：

```bash
git submodule status --recursive
git diff --submodule
git status --short
```

如果用户指定目标 ref，按目标 ref 计划更新。如果用户只说“更新到最新”，先用远端查询解析默认分支最新 commit，并展示当前 ref -> 目标 ref。不要在未确认写操作授权时改变 pinned commit。

## 审计 submodule

审计是只读任务，默认直接执行检查，不需要先提问。输出应聚焦 Git 状态：

- `.gitmodules` 是否存在。
- 每个 submodule 的路径、URL 和当前 pinned commit。
- 主仓 docs 或 registry 是否记录了该 submodule 的边界、消费者、构建入口和验证入口。
- 是否未初始化、路径缺失、URL 不一致、内部 dirty、主仓库记录了 submodule commit 变化。
- 推荐的修复命令。

## 修复 submodule

常见修复命令：

```bash
git submodule sync --recursive
git submodule update --init --recursive
```

如果修复会 checkout 文件或改变 submodule 工作区状态，先确认授权。修复后再次运行 status/diff 检查。

## 移除 submodule

移除是破坏性操作。执行前确认目标路径和授权，并先检查引用：

```bash
git grep -n "<submodule-path>"
git submodule status --recursive
git status --short
```

删除后检查 `.gitmodules`、Git index、工作区目录和引用是否清理完成。

## 文档与证据

- 如果只是临时引入或一次性调研 submodule，通常记录在本次变更说明即可，不必修改长期 docs。
- 如果 submodule 将长期存在，必须更新 `docs/02-development/submodules-index.md`，记录路径、URL、pinned ref、边界、消费者、构建入口、验证入口和更新策略。
- 如果新增了可复用的 submodule 管理规则、路径约定或验证流程，更新 `docs/02-development/git-submodules.md`。
- 如果本次任务是明确的项目治理能力实现，更新 `docs/evidences/` 并同步索引。
- 不要把外部仓库源码或主观价值评审大段写入 docs。

## 输出格式

默认用中文输出短计划或结果：

```text
操作: add/update/audit/repair/remove
仓库: <repo-url>
路径: <path>
当前状态: <status/ref/conflict>
计划命令: <commands>
验证命令: <commands>
需要确认: <仅列写操作授权或真正阻塞的问题>
```

如果用户明确要求先推演，不要编辑文件；先用 `reasoning-map` 展示 submodule 操作链路和 RED/GREEN 节点。
