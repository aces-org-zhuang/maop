# SOP 07: Submodule Governance

## 目标

为研究工作区、AI 引擎、外部参考仓、供应商代码和课题内参考仓建立可追踪来源、可审计状态和可更新流程。

## 锁定 submodule

新项目初始化必须规划这两个 submodule：

```text
vendor/research/aces-research -> https://github.com/aces-org-zhuang/aces-research.git
vendor/ai/maop                 -> https://github.com/aces-org-zhuang/maop.git
```

`aces-research` 承载研究资产；`maop` 承载 AI 引擎能力和 engine-side `.opencode`。两个 submodule 都应通过 `.gitmodules` 记录来源，并在主仓索引中记录 pinned commit、边界、消费者和验证方式。`maop` 与其他 submodule 不同：它必须启用 sparse-checkout，只检出 `.opencode` 和 `README.md`，再由项目 `.opencode/opencode.json` 桥接到 maop 的 OpenCode 能力面。

## 路径规则

```text
vendor/research/aces-research                        锁定研究工作区 submodule
vendor/research/aces-research/topics/<slug>/repos/<repo_name>
                                                     课题内研究参考仓 submodule
vendor/ai/maop                                       锁定 AI 引擎 submodule
vendor/runtime/<repo_name>                           运行时或打包资源仓
vendor/assets/<repo_name>                            资源型外部仓
vendor/harness/<repo_name>                           agent、MCP、verifier、workflow harness
vendor/external/<repo_name>                          无法归类但长期保留的外部仓
```

## 执行步骤

1. 检查 `.gitmodules` 是否存在。
2. 检查 `git submodule status --recursive` 和 `git status --short`。
3. 新增 submodule 前，从 URL 推导 `repo_name`、目标路径和用途。
4. 对锁定 submodule，校验 URL 和 path 是否与标准一致；不一致时输出迁移计划，不直接覆盖。
5. 写操作前向用户确认将执行的 `git submodule add`、checkout、update 或 remove 命令。
6. 新增长期 submodule 后，在主仓 `docs/02-development/submodules-index.md` 或等价索引中记录 path、url、pinned ref、边界、消费者、验证方式。
7. 研究课题内参考仓还要更新研究区课题 README 或 `repos-index.md`。

## maop sparse-checkout 执行步骤

新项目初始化或修复 `vendor/ai/maop` 后，执行：

```bash
git submodule add https://github.com/aces-org-zhuang/maop.git vendor/ai/maop
git -C vendor/ai/maop sparse-checkout set --no-cone /.opencode/ /README.md
git -C vendor/ai/maop sparse-checkout list
```

如果项目提供脚本，可封装为 `npm run maop-opencode:sparse` 或等价命令。验证输出必须包含：

```text
/.opencode/
/README.md
```

## .opencode 边界

- 主仓 `.opencode/opencode.json` 是桥接配置。
- `vendor/ai/maop/.opencode/` 是 AI 引擎级配置，由 maop submodule 自身维护。
- 主仓通过 `skills.paths` 和 `maop-opencode` reference 消费 maop 的 `.opencode` 能力。
- 不把 maop 的 `.opencode` 复制回项目仓，也不在主仓维护同一批 skill 文件。

## 安全规则

- 不要求用户粘贴 token、密码或 SSH 私钥。
- 不把凭据写入 `.gitmodules`、docs、evidence 或 skill 输出。
- 远端访问失败时，只基于 Git 命令错误诊断认证、网络、权限或 URL 问题。
- 子模块内部有未提交改动时，不执行更新或删除，先询问用户。

## 关联技能

涉及真实 submodule 写操作、更新、审计、修复或移除时，优先加载 `submodule-manager` 技能执行 Git 细节。本 SOP 只定义初始化项目的路径和治理规则。

## 检查单

- `checklists/submodule-safety.md`

## 常见 RED 点

- 普通 clone 外部仓到主仓，来源不可追踪。
- submodule 已加入但没有主仓索引记录消费者和验证方式。
- 研究参考仓放在研究区根目录，而不是具体课题 `repos/`。
- `.gitmodules` path 与 docs 索引不一致。
- maop 没有 sparse-checkout，或项目 `.opencode/opencode.json` 没有桥接 maop skills，导致项目开发时丢失 AI 引擎能力。
- maop `.opencode` 与项目仓 `.opencode` 双源维护，导致能力版本无法通过 submodule commit 固定。
