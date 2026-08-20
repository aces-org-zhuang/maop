# SOP-00 Intake and Routing

## Goal and scope

把用户请求转换成可执行的技能创建/改进/评测任务，并选择最小资源集合。适用于每次触发；不在本阶段修改技能内容。

## Pre-read and todo/status

1. Read `../SKILL.md` only through the skill root path as `SKILL.md`, then read this SOP.
2. 建立 todo：`intake`、`route`、每个代理/批次/审查/benchmark、`validate`、`handoff`。
3. 每项记录 `status`、owner、输入、输出、证据路径和下一步；开始执行前置为 `running`。
4. 若请求是复杂重构、并行委派、评测或 benchmark，不得跳过 todo/status。

## Intake record

记录：

| 字段 | 内容 |
| --- | --- |
| Goal | 技能要让 LLM 做什么 |
| Trigger | should-trigger 语境、near-miss should-not-trigger 语境 |
| Output | 文件、JSON、报告、viewer、包或描述 |
| Inputs | 用户输入文件、旧技能、约束、模型和命令 |
| Boundary | 可写目录、不可修改目录、外部副作用和授权 |
| Success | 可观察验收条件 |
| Risks | RED、缺配置、缺依赖、不可验证声明 |

先从对话提取已有答案；仅在影响执行的缺口上提问。没有明确输入时，不臆造示例数据、外部验证或用户反馈。

## Condition routing

```text
request
  -> create/new or improve/existing
  -> draft/structure: sop-01
  -> eval/run: sop-02
  -> grade/benchmark/compare: sop-03
  -> optimize description/package: sop-04
  -> dialectical/adversarial merge: sop-06
  -> every terminal path: sop-05
```

使用 `condition` 而非关键词堆叠：如果阶段有依赖则串行；独立 eval、文件检查或审查可并行；需要候选、实验或修复时以 round 发散后收敛；失败有明确新输入时 loop，最多按验证 SOP 的上限重试。

## Bounded delegation

每个代理任务必须包含：一个问题、最小上下文、允许读取的路径、禁止写入/决策的范围、停止条件和以下返回模板：

```text
Finding: <观察到的事实或未发现>
Evidence: <精确路径、行号、命令输出或产物>
Confidence: <0..1；只代表该 finding>
Fidelity: <原文/结构/行为保持程度及损失>
RED: <风险、矛盾、阻塞；无则 none>
Excluded scope: <明确未检查或不负责的范围>
Next step: <主 LLM 可执行的下一动作>
```

代理可做广泛检索、文档/代码探索、抽取、独立评分和机械校验；主 LLM 保留意图、范围、路由、收敛、最终选择和用户结论。返回缺字段、证据不可定位或置信度无依据时，标记 `blocked` 并补派或内联核验。

## Unified lifecycle

- Entry：意图、边界和 todo 已创建。
- Success：目标产物和验证证据齐全，未执行的外部动作明确写出。
- Blocked：缺输入/配置/权限/依赖，记录恢复条件，不继续假设。
- Failed：命令、解析或代理失败；保留日志，最多在有新证据时重试。
- Exit：更新所有 todo/status；交付产物、证据、RED、excluded scope 和 next step。

## Validation

检查已选 SOP 与真实文件存在；检查写边界未越界；检查每项委派有返回契约；检查 status 没有遗留 `running`。把本阶段 finding 写入工作区/对话，不把临时状态写进不属于用户授权的目录。
