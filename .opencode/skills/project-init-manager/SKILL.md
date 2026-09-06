---
name: project-init-manager
description: 项目代码仓初始化管理技能。用户要求初始化新项目、把空文件夹变成标准代码仓、补齐 AGENTS.md、docs 体系、.opencode 本地配置、研究区、submodule 机制、目录治理或审计项目初始化完整性时必须使用。本技能采用短 SKILL.md 路由层，按 SOP 文件渐进执行，避免把所有初始化细节塞进入口文件。
---

# Project Init Manager

本技能用于把一个新项目目录初始化为可持续开发、可归档、可被 LLM 协作维护的代码仓。SKILL.md 只做路由、阶段选择和交付约束；具体执行步骤必须读取 references 下的 SOP 文件。

## 执行模型

选择的基础模型：任务依赖树 + round + loop + dialectical。主 LLM 按条件派发代理执行只读探索、独立审查或证据整理；纯路由、写入决策、最终验证和交付由主流程完成。

```text
intake -> round: 审计/候选边界 -> sop-01..07 执行
      -> loop: validation/feedback 修复 -> sop-08 -> sop-09
      -> dialectical: 仅在多个初始化方案冲突时派发独立审查并由主流程裁决
```

每个阶段执行前后更新 todo/status；代理只在满足并行探索、独立评分或多视角审查条件时派发，并返回可定位证据，不替代最终决策。

## 核心契约

- 初始化必须先读取 sop-00，再按 Stage Router 渐进读取后续 SOP。
- 写入前确认边界，写入后执行 sop-08 验证，并由 sop-09 处理可迁移作业经验。
- 作业经验与项目规则分离，经验只通过 docs/07-llm/operational-experiences.md 单行沉淀。
- 复杂初始化影响面、submodule、docs 体系或作业经验边界不清时，委派代理执行 reasoning-map 收敛候选路径后再写入。


## 触发后先做什么

1. 先使用 `reasoning-map` 推演本次初始化范围、现有文件风险、目录职责域、研究区、docs、`.opencode` 和 submodule 影响面。
2. 读取 `references/sop-00-intake.md`，完成项目路径、现状和初始化模式判定。
3. 执行任何初始化写入、submodule 添加、`.opencode` 生成或 docs/research 目录落盘前，先按 development-workflow 的 configuration-readiness-gate 统一确认项目路径、初始化模式、允许写入范围、submodule URL/path/ref、研究区策略、`.opencode` 桥接、验证命令和用户授权；不要在执行中途零散索要配置。
4. 根据 Stage Router 读取后续 SOP。不要提前读取所有 SOP，也不要把所有规则复制到主上下文。
5. 执行写操作前，确认不会覆盖用户已有文件；遇到已存在文件时先读取并增量合并。
6. 完成后读取 `references/sop-08-validation.md` 和 `references/sop-09-feedback-loop.md`，做完整性检查和反哺规则落地；完整性检查不达标时按 development-workflow 的 auto-remediation-gate-loop 自动补缺失结构、索引、桥接、验证记录和反哺规则，硬阻断才询问用户。

## 总原则

- 初始化过程默认按供需式协作处理：用户提供目标、授权和验收，Agent 负责审计、规划、写入、验证和归档。
- 初始化中不得把完整 SOP、目录治理细则、submodule 细节或长方案一次性抛给用户要求理解；除非用户明确要求完整方案。
- 需要用户确认时，每次只提出一个会影响写入边界、付费、凭据、外部授权或不可逆操作的决策。
- 对用户只输出当前最小动作、关键风险和完成后反馈信号；完整执行细节由 Agent 内部按 SOP、质量门禁和验证规则消化。
- 供需式协作不降低 Reasoning、Preview、POC、Review、Verification、Confidence 和 Stop Rule 等质量门禁；它只约束门禁结果的对用户呈现方式。
- `SKILL.md` 是路由层，不承载完整初始化细节。
- 目录设计先按职责域，再按技术栈映射具体目录名。
- 研究区必建，并锁定为 `vendor/research/aces-research` -> `https://github.com/aces-org-zhuang/aces-research.git` submodule，与主仓默认项目知识库隔离。
- AI 引擎默认必建，并锁定为 `vendor/ai/maop` -> `https://github.com/aces-org-zhuang/maop.git` submodule；项目初始化必须通过 maop submodule sparse-checkout 和项目 `.opencode/opencode.json` 桥接 maop 的 `.opencode` 能力面。例外：目标仓库本身就是 `maop` 源仓时，不得把自身再添加为 `vendor/ai/maop`，应切换为 maop 源仓模式。
- `docs/` 只保存长期稳定知识；研究过程、论文、开源对比和证据包进入研究区。
- 新增、重命名或删除索引型文件时，同步更新对应 README 或 index。
- `.opencode/opencode.json` 在普通项目初始化时作为桥接配置生成，至少引用 `vendor/ai/maop/.opencode/skills`，并登记 `maop-opencode` reference；项目本地组件目录只在项目确有本地覆盖时创建。maop 源仓模式下，`.opencode/skills` 是一等源码目录，`maop-opencode` reference 指向本仓 `.opencode`，不创建嵌套 AI engine submodule。
- 外部参考仓和研究参考仓优先使用 Git submodule，不普通 clone 到主仓。
- 开发规则只生成通用治理元规则，不复制某个项目的技术栈细则；本技能不引入 `profiles` 或 `overlays` 机制。
- 不伪造未知技术栈命令；未知时写 `待补充`，并标明需要从技术栈配置或用户确认中补齐。
- POC、正式初始化和写操作前必须一次性列出 required/optional/unknown 配置并确认；缺少 required 配置时停止，不在执行过程中临时索要。
- Output Budget Rule：默认 compact 输出，只说明初始化模式、将执行的 SOP、写入边界、关键风险和下一步；完整初始化报告仅在完整初始化、用户明确要求或交付阶段输出。
- Todo Planning Rule：初始化、审计、写入、submodule、验证前，先更新 todo；每个 SOP 阶段、写入动作、索引同步、submodule 操作和验证动作都应有对应 todo。单文件小修或纯问答可跳过。
- Write Budget Rule：先审计，再写入；每轮写入只覆盖当前 SOP 的最小文件集。已存在文件只增量合并，不覆盖用户内容；覆盖风险、写入范围不清、required 配置缺失或 submodule 授权缺失时立即停止。
- Submodule Budget Rule：研究区和 AI 引擎 submodule 必建规则只适用于完整新项目初始化；审计、轻量补齐或非普通宿主项目只报告 submodule 差距，不默认执行 add/update。submodule 写操作必须有用户授权、明确 URL/path/ref 和对应 todo；复杂 submodule 操作转入 `submodule-manager`。
- Auto-remediation Rule：普通初始化补缺默认自动修复 1-2 轮；完整初始化或用户明确要求可按 auto-remediation gate 扩展。连续 1 轮无进展、覆盖风险、写入范围不清、submodule 配置/授权缺失或 required 配置缺失时立即停止。

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
- `references/sop-04-agents-rules.md`: 根 AGENTS 和 docs/AGENTS 生成规则。
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
