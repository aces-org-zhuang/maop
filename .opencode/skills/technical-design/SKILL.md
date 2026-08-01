---
name: technical-design
description: 必须用于技术设计、架构影响面、技术方案、接口设计、数据/状态设计、变更边界、兼容性风险、验证策略和实施切片。用户说“需求已确认”“不要写代码”“先设计接入现有系统”“接口和状态”“验证策略”时优先使用本技能；不要用于产品方向判断、代码实现或项目初始化。
---

# Technical Design

本技能用于把已确认的需求转成可实现、可验证、可追踪的技术方案。`SKILL.md` 只做路由和交付约束，阶段步骤按需读取 `references/sop-*.md`。

## 触发后先做什么

1. 读取 `references/sop-00-intake.md`，确认需求输入、项目上下文和设计范围。
2. 涉及复杂影响面、跨模块关系、异步时序、兼容性或根因不明的设计取舍时，先使用 `reasoning-map`。
3. 需要图表时调用 `ipd-uml`；本技能决定是否需要图，`ipd-uml` 决定图表类型和质量。
4. 需要深度开源实现洞察或证据包时转入 `research`；需要快速 GitHub 选型时可使用 `github-selection`。
5. 如果项目缺少基础治理、目录规则或 `.opencode` 桥接，转入 `project-init-manager`，不要在本技能中重建初始化规则。
6. 生成完整技术设计或实施切片前，先执行 Preview Gate，并等待用户确认或明确标注假设后再继续。预览可用 ASCII/Mermaid 架构图、时序图、状态机图、DFD、接口草案或低保真交互草图。
7. 当用户明确要求“先只输出草图 / 不要完整设计 / 不要写代码”时，不做仓库探索、不读取大量文档；只基于已给输入生成预览和待确认假设。
8. 用户未提供项目专有系统名称、路径或运行时能力时，草图必须保持跨项目中性；不要引入当前仓库的产品名、目录、运行时、网关或工具链。
9. 不要把技术设计请求改派给角色型名称；在 maop 技能体系内，本技能就是需求确认后的设计入口。
10. 设计定版、进入实现或高风险 POC 前执行 Review Gate，review 分数必须 >=80；低于 80 先修订并复审。

## Stage Router

```text
任何技术设计请求
  -> Stage 0 Intake: references/sop-00-intake.md

需要理解现有系统、代码位置或项目约束
  -> Stage 1 Context Discovery: references/sop-01-context-discovery.md

需要把需求映射到设计决策
  -> Stage 2 Requirement Trace: references/sop-02-requirement-trace.md

需要比较方案、架构或技术路线
  -> Stage 3 Solution Options: references/sop-03-solution-options.md

需要接口、数据、状态、错误处理或权限设计
  -> Stage 4 Interface Data State: references/sop-04-interface-data-state.md

需要模块变更边界、冻结区或兼容性影响
  -> Stage 5 Change Boundary: references/sop-05-change-boundary.md

需要风险、验证策略和实施切片
  -> Stage 6 Risk Validation Plan: references/sop-06-risk-validation-plan.md

已有设计需要评审或修订
  -> Stage 7 Design Review: references/sop-07-design-review.md
```

## 通用原则

- 优先遵循项目已有架构、文档、平台抽象、编码约束和设计模板。
- 设计必须能追溯到需求，不用个人偏好替代约束。
- 设计阶段不写生产代码；若用户要求实现，转入 `implementation-delivery`。
- 明确变更边界、兼容性、迁移风险和验证方式。
- 长设计前先给低成本预览，避免遗漏影响面后继续放大到实现阶段。
- 复杂影响面、真实脚本运行、构建验证或高成本实现前先用 `reasoning-map` 做推演预检。
- 设计定版前必须 review，分数 >=80 才进入实现阶段。
- AET 的 RAS/RDS/SDD、fence 等只作为可选模式，不作为跨项目硬规则。

## 资源索引

- `references/sop-00-intake.md`: 设计范围、输入和上下文判定。
- `references/sop-01-context-discovery.md`: 项目、文档和代码上下文发现。
- `references/sop-02-requirement-trace.md`: 需求到设计决策映射。
- `references/sop-03-solution-options.md`: 方案选项与取舍。
- `references/sop-04-interface-data-state.md`: 接口、数据、状态、错误和权限设计。
- `references/sop-05-change-boundary.md`: 模块边界、冻结区、兼容性和迁移。
- `references/sop-06-risk-validation-plan.md`: 风险、验证策略和实施切片。
- `references/sop-07-design-review.md`: 设计完整性评审。
- `references/pattern-aet-design.md`: AET 可迁移设计模式。
- `templates/`: 可选设计产物模板。
- `templates/design-sketch.md`: 长技术设计前的设计预览模板；ASCII 只是默认形式之一。
- `checklists/`: 设计质量清单。

## 交付标准

交付时说明：需求追踪、当前系统依据、推荐方案、被拒绝方案、接口/数据/状态影响、变更边界、风险、验证策略、实施切片，以及是否已具备进入 `implementation-delivery` 的条件。
