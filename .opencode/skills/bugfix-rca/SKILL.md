---
name: bugfix-rca
description: 用于问题定位、修复和“不再复现”验证。用户说“定位故障”“做 RCA”“修复后验证”“确认问题不再复现”“回归/复现验证”时优先使用本技能。必须先建立一份单一真相源的 RCA 追踪报告，再用 reasoning-map 收敛故障最小窗口，最后通过构建、API、WebUI、回归或手工复现验证问题不再复现；不要把“修复已实施”误判为完成。
---
# Bugfix RCA

## 执行模型

选择的基础模型：任务依赖树 + round + loop。

本技能以一份 RCA 追踪报告为唯一事实载体；`document-generation` 负责把报告逐段初始化和更新，`reasoning-map` 负责收敛故障窗口与验证边界，`implementation-delivery` 负责真实修复与 fresh verification。完成条件只看“原问题不再复现”，不看“修复已提交”。

```text
RCA single source of truth
  -> sop-00-intake-and-routing {归类为 bug / regression / verification failure / RCA trace}
  -> document-generation {初始化并持续更新 fix-rca-trace.md}
  -> sop-01-bugfix-trace-init {定义现象、环境、复现、影响和证据}
  -> reasoning-map {收敛故障最小窗口与候选根因}
  -> sop-02-reasoning-map-slice {锁定最小切片、排除项和验证路径}
  -> sop-03-repair-and-fresh-verification {修复并用 build/API/WebUI/回归验证不再复现}
       -> {仍可复现} loop 回到 reasoning-map / repair
       -> {不可复现} -> sop-04-handoff
  -> sop-04-handoff {交付 RCA 结论、验证证据和残余风险}
```

只有当问题边界、复现条件、环境差异、验证入口或时序关系不清时，才在主流程中使用 reasoning-map 收敛；边界明确的日志抽取、最小复现执行、验证脚本运行和证据整理可委派边界明确的代理执行。代理只负责检索、抽取、复现、验证或审阅，不负责最终根因、修复方向或完成判断。

## 核心契约

- **Single source of truth**：一次任务只允许一份 `fix-rca-trace.md` 逻辑报告和一个与之对应的文档状态。
- **Completion rule**：只有当前证据下原问题不可复现，才允许进入完成态。
- **Reasoning gate**：最小窗口、时序边界、候选根因和验证路径不清时，先用 `reasoning-map`。
- **Verification gate**：必须覆盖与问题最相关的验证入口，优先级通常是最小复现 > API > WebUI > 回归 > 构建/静态检查。
- **Document update**：报告只能通过 `document-generation` 的 CLI 片段更新，不手写第二份真相源。
- **Fresh evidence**：完成声明必须绑定本轮实际执行的验证结果，不能用“修复已实施”替代“不再复现”。

## 资源索引

- `references/sop-00-intake-and-routing.md`
- `references/sop-01-bugfix-trace-init.md`
- `references/sop-02-reasoning-map-slice.md`
- `references/sop-03-repair-and-fresh-verification.md`
- `references/sop-04-handoff.md`
- `templates/fix-rca-trace.md`
- `templates/rca-steps-plan.json`
