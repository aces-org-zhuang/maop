---
name: project-init-manager
description: 项目代码仓初始化管理技能。用户要求初始化新项目、把空文件夹变成标准代码仓、补齐 AGENTS.md、docs 体系、.opencode 本地配置、研究区、submodule 机制、目录治理或审计项目初始化完整性时必须使用。本技能采用短 SKILL.md 路由层，按 SOP 文件渐进执行，避免把所有初始化细节塞进入口文件。
---

# Project Init Manager

本技能用于把一个新项目目录初始化为可持续开发、可归档、可被 LLM 协作维护的代码仓。`SKILL.md` 只做路由、阶段选择和交付约束；具体执行步骤必须读取 `references/sop-*.md`。

## 触发后先做什么

1. 先使用 `reasoning-map` 推演本次初始化范围、现有文件风险、目录职责域、研究区、docs、`.opencode` 和 submodule 影响面。
2. 读取 `references/sop-00-intake.md`，完成项目路径、现状和初始化模式判定。
3. 根据 Stage Router 读取后续 SOP。不要提前读取所有 SOP，也不要把所有规则复制到主上下文。
4. 执行写操作前，确认不会覆盖用户已有文件；遇到已存在文件时先读取并增量合并。
5. 完成后读取 `references/sop-08-validation.md` 和 `references/sop-09-feedback-loop.md`，做完整性检查和反哺规则落地。

## 总原则

- `SKILL.md` 是路由层，不承载完整初始化细节。
- 目录设计先按职责域，再按技术栈映射具体目录名。
- 研究区必建，并锁定为 `vendor/research/aces-research` -> `https://github.com/aces-org-zhuang/aces-research.git` submodule，与主仓默认项目知识库隔离。
- AI 引擎默认必建，并锁定为 `vendor/ai/maop` -> `https://github.com/aces-org-zhuang/maop.git` submodule；项目初始化必须通过 maop submodule sparse-checkout 和项目 `.opencode/opencode.json` 桥接 maop 的 `.opencode` 能力面。例外：目标仓库本身就是 `maop` 源仓时，不得把自身再添加为 `vendor/ai/maop`，应切换为 maop 源仓模式。
- `docs/` 只保存长期稳定知识；研究过程、论文、开源对比和证据包进入研究区。
- 新增、重命名或删除索引型文件时，同步更新对应 README 或 index。
- `.opencode/opencode.json` 在普通项目初始化时作为桥接配置生成，至少引用 `../vendor/ai/maop/.opencode/skills`，并登记 `maop-opencode` reference；项目本地组件目录只在项目确有本地覆盖时创建。maop 源仓模式下，`.opencode/skills` 是一等源码目录，`maop-opencode` reference 指向本仓 `.opencode`，不创建嵌套 AI engine submodule。
- 外部参考仓和研究参考仓优先使用 Git submodule，不普通 clone 到主仓。
- 开发规则只生成通用治理元规则，不复制某个项目的技术栈细则；本技能不引入 `profiles` 或 `overlays` 机制。
- 不伪造未知技术栈命令；未知时写 `待补充`，并标明需要从技术栈配置或用户确认中补齐。

## Stage Router

```text
任何初始化或审计请求
  -> Stage 0 Intake: references/sop-00-intake.md

新建或补齐仓库基础
  -> Stage 1 Repo Foundation: references/sop-01-repo-foundation.md

需要设计上层目录结构
  -> Stage 2 Directory Governance: references/sop-02-directory-governance.md

需要 docs 体系、索引机制、反哺机制
  -> Stage 3 Docs System: references/sop-03-docs-system.md

需要生成或修订 AGENTS.md / docs/AGENTS.md
  -> Stage 4 Agent Rules: references/sop-04-agents-rules.md

需要 .opencode 本地配置、skills、agents、commands
  -> Stage 5 OpenCode Config: references/sop-05-opencode-config.md

任何新项目初始化
  -> Stage 6 Research Workspace: references/sop-06-research-workspace.md

需要引入、规划或审计外部仓库
  -> Stage 7 Submodule Governance: references/sop-07-submodule-governance.md

落盘完成或审计完成
  -> Stage 8 Validation: references/sop-08-validation.md

需要说明后续维护、资料归档、实现证据、失效模式
  -> Stage 9 Feedback Loop: references/sop-09-feedback-loop.md
```

## 推荐完整初始化顺序

```text
sop-00-intake
  -> sop-01-repo-foundation
  -> sop-02-directory-governance
  -> sop-03-docs-system
  -> sop-04-agents-rules
  -> sop-05-opencode-config
  -> sop-06-research-workspace
  -> sop-07-submodule-governance
  -> sop-08-validation
  -> sop-09-feedback-loop
```

如果用户只要求审计既有仓库，仍先执行 `sop-00-intake`，再跳到相关 SOP 和 `sop-08-validation`，不要强行重建已有结构。

## 资源索引

- `references/sop-00-intake.md`: 需求采集、现状检查、初始化模式判定。
- `references/sop-01-repo-foundation.md`: Git、README、ignore、基础仓库文件。
- `references/sop-02-directory-governance.md`: 目录职责域、技术栈映射、目录新增规则。
- `references/sop-03-docs-system.md`: docs 分层、索引机制、反哺机制、token 控制。
- `references/sop-04-agents-rules.md`: 根 `AGENTS.md` 和 `docs/AGENTS.md` 生成规则。
- `references/sop-05-opencode-config.md`: `.opencode` 目录、skills、agents、commands 和配置策略。
- `references/sop-06-research-workspace.md`: 必建研究区、课题结构、研究资料隔离。
- `references/sop-07-submodule-governance.md`: `.gitmodules`、vendor 路径、锁定 submodule、研究参考仓 submodule 规则。
- `references/sop-08-validation.md`: 初始化完整性检查和验收输出。
- `references/sop-09-feedback-loop.md`: 后续开发、调试、研究、证据的反哺规则。
- `references/pattern-workflow-workspace.md`: 可选 AI 研发工作区模式；仅在项目明确需要长期保存需求、设计、实现、验证和评审产物时读取，不作为默认初始化规则。
- `templates/`: 可落盘模板，按 SOP 指引读取。
- `checklists/`: 执行前、执行后和 submodule 安全检查。

## 交付标准

交付时必须说明：

- 已初始化或已审计的项目路径。
- 已创建、已更新、保留未覆盖的关键文件。
- 技术栈或能力开发目录映射中仍需用户或配置补齐的项。
- 研究区路径和续点入口。
- 普通宿主项目：AI 引擎 submodule 路径、sparse-checkout 状态和 `.opencode` 桥接边界。
- maop 源仓模式：本仓 `.opencode/skills` 能力源码边界、`.opencode/opencode.json` 本仓引用方式，以及已排除 `vendor/ai/maop` 自嵌套。
- `.opencode/opencode.json` 是否按当前模式正确登记 `maop-opencode` reference。
- 验证结果和未闭环 RED 点。
