---
name: skill-creator
description: Skill 创建与优化技能 - 用于从零创建 skill、修改和改进现有 skill、评估 skill 表现、运行 eval、做性能基准和方差分析，或优化 description 以提升触发准确性。只要用户要设计、重构、评测、比较、迭代、验证或打包一个 skill，就使用本技能。
---

# Skill Creator

## 执行模型

本入口是路由器，不是完整操作手册。先读取本文件，再根据用户意图为**目标 skill** 选择执行模型与最小必要 SOP；复杂请求可继续读取后续 SOP，不要一次加载全部资源。

执行前、每次代理委派前后、每个评测批次前后、每轮修复前后都更新 todo/status。状态至少记录 `pending`、`running`、`blocked`、`failed`、`succeeded` 和 `exited`，并包含当前 SOP、产物路径、证据和下一步。

目标 skill 的执行模型模板不写在本入口；创建或大改目标 skill 时读取 `references/target-skill-execution-model.md`。本入口只负责路由、状态和资源索引。

创建或大改目标 skill 前必须读取 `references/sop-01-draft-and-structure.md` 和 `references/target-skill-execution-model.md`，再输出目标 skill 目录结构或 `SKILL.md` 骨架；不能只读本入口就生成单文件草稿。

本技能 SOP 的代理委派必须绑定明确条件。满足并行评测、独立评分、trigger 试验或多视角对抗条件时，主 LLM 可以委派边界明确的代理执行对应 SOP；纯路由、最终验证和最终交付留在主流程。代理只负责检索、抽取、独立评审或机械执行，不负责最终范围、架构、胜负、完成度或用户决策。代理返回固定字段：`Finding`、`Evidence`、`Confidence`、`Fidelity`、`RED`、`Excluded scope`、`Next step`。缺字段视为阻塞，不能直接采纳。

本入口的执行模型示意。四种基础模型按用户需求选择一个或多个组合，不默认全量聚合；只有满足明确条件的节点才委派代理执行，其他节点由主流程处理。

```text
[目标 skill 生成请求]
   -> [选择基础模型 {1..n}]
        ├─ [任务依赖树 {串行/并行/condition}]
        ├─ [round {发散 -> 验证 -> 收敛}]
        ├─ [loop {重试 -> 退出}]
        └─ [dialectical {多视角 -> 对抗 -> 主流程裁决}]

[本技能执行链]
   -> [sop-00-intake-and-routing {解析需求/定边界}]
        -> [sop-01-draft-and-structure {主流程起草目标 skill}]
        -> [sop-02-evals-and-runs {条件: 需要并行评测时委派代理执行}]
        -> [sop-03-grading-and-benchmark {条件: 需要独立评分/对比时委派代理执行}]
        -> [sop-04-description-optimization {条件: 需要 trigger 试验时委派代理执行}]
        -> [sop-05-validation-and-handoff {主流程验证/交付}]
        -> [sop-06-dialectical-adversarial-merge {条件: 需要多视角对抗时委派代理执行}]
             -> [更新 todo-status / 交付]
```

## 核心契约

统一生命周期：

```text
Entry -> Intake -> Route -> Execute -> Validate -> Handoff -> Exit
             |        |                  |
           blocked   failed          retry/round
```

| 状态 | 进入条件 | 必须动作 | 退出条件 |
| --- | --- | --- | --- |
| Entry | 收到技能创建、改进、评测、比较或打包请求 | 读取本入口，建立 todo/status | 意图和边界已记录 |
| Success | 产物、引用、验证均通过 | 汇总真实证据，说明未执行的外部动作 | 用户可按路径继续或重启 |
| Blocked | 缺配置、缺输入、代理契约不完整或验证前置不满足 | 记录 blocker、RED、所需输入和恢复命令 | blocker 解除，或转失败 |
| Failed | 命令/代理/解析/评测失败且重试不能修复 | 保留日志和中间产物，不伪造结果 | 明确失败原因和下一步 |
| Exit | 成功、阻塞或失败均已收敛 | 更新 todo/status 为 `exited`，交付证据 | 无未声明的进行中动作 |

完整执行必须包含：意图采集、reasoning-map（适用于复杂修改）、SOP 路由、边界明确的委派、产物/日志、验证、反馈闭环和最终 RED。任何引用只允许指向本目录真实存在的文件，或明确标注为目标 skill/workspace 运行时产物。

## 资源索引

按需读取以下真实资源：

| 资源 | 用途 | 何时读取 |
| --- | --- | --- |
| `references/sop-00-intake-and-routing.md` | 意图采集、todo/status、condition 路由、代理契约、生命周期 | 每次触发首先读取 |
| `references/sop-01-draft-and-structure.md` | 创建/重构技能、渐进披露、SOP 设计、完整链路质量 | 需要写或大改技能时 |
| `references/sop-02-evals-and-runs.md` | evals、with-skill/baseline、并行运行、计时和 viewer 输入 | 需要运行测试时 |
| `references/sop-03-grading-and-benchmark.md` | grader、benchmark 聚合、analyzer、blind comparison | 需要评分、基准或比较时 |
| `references/sop-04-description-optimization.md` | 20 条 trigger 集、asset review、`run_loop.py`、描述更新、打包 | 需要优化 description 或打包时 |
| `references/sop-05-validation-and-handoff.md` | 引用/文件/编译检查、confidence、二次 reasoning-map、交付和退出 | 每次完成前读取 |
| `references/sop-06-dialectical-adversarial-merge.md` | 多视角执行、对抗比较、辩证合并、主流程裁决 | 需要最佳决策或对抗合并时 |
| `references/schemas.md` | eval、grading、timing、benchmark、comparison、analysis JSON 结构 | 写对应 JSON 前 |
| `references/self-test-confidence.md` | 90% confidence 的测试集、公式和 gate | 用户要求自测/置信度时 |
| `references/sop-routed-skills.md` | SOP 路由结构原则 | 设计路由时 |
| `references/sop-full-link-quality.md` | intake 到反馈的质量链 | 复杂修改时 |
| `references/sop-consolidating-workflow-skills.md` | 合并重复技能的分类和边界 | 用户要求整合技能时 |
| `references/target-skill-execution-model.md` | 目标 skill 的执行模型、ASCII 图例和生成约束 | 创建或大改目标 skill 时 |
| `agents/grader.md` / `agents/comparator.md` / `agents/analyzer.md` | 评分、盲比、基准/事后分析代理指令 | 委派对应代理时 |
| `scripts/*.py` | 验证、eval、循环、报告、聚合、描述优化、打包 | SOP 指定命令时 |
| `eval-viewer/generate_review.py` + `eval-viewer/viewer.html` | 评测结果 viewer 和反馈 | 有 runs 和 grading 产物时 |
| `assets/eval_review.html` | 描述 trigger eval 集人工编辑模板 | 优化 description 前 |
| `LICENSE.txt` | Apache 2.0 许可文本 | 分发或打包时 |

旧版完整流程已迁移至以上 SOP。不存在的 `templates/`、`checklists/` 或本技能自身 `evals/` 不作为 bundled 资源引用；若目标 skill 有这些运行时目录，路径必须相对于目标 skill/workspace 并先检查存在性。
