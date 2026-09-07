---
name: frontend-management-ops
description: 必须用于面向现有前端管理域落地项目、习惯、成员、交付、团队等实体的 CRUD、批量操作、导入导出、doctor 诊断和构建安装后的 CLI 操作能力。用户说“项目/习惯/成员/交付/团队管理”“管理后台 CRUD”“数据导入导出”“给前端补 CLI”“doctor 诊断”“安装后用技能操作管理数据”时优先使用；不要用于纯视觉设计、无代码产品定义或与前端管理域无关的通用 CLI。
---

# Frontend Management Ops

本技能用于把当前前端管理功能变成可由 UI 和 CLI 共同操作的可验证管理能力。`SKILL.md` 只做执行模型、核心契约、资源索引和交付标准；具体步骤按需读取资源索引中的 SOP 文件。

## 执行模型

选用基础模型：`任务依赖树 + round + loop`。`round` 用于实体契约发现、CRUD/CLI 草案、验证反馈之间的发散和收敛；`loop` 用于失败后的有限修复和重跑。`dialectical` 不默认启用，仅当存在两套以上互斥 CLI/schema/持久化方案且风险相近时，才委派代理执行多视角对抗评审，最终裁决仍由主流程负责。当同一批实体需要并行源码发现、测试面盘点或 CLI 证据抽取时，允许委派代理执行有边界的只读 SOP；最终范围、数据契约、代码修改、验证结论和交付声明必须由主流程裁决。

代理派发条件：仅在并行源码发现、独立测试面盘点、证据抽取或对抗评审节点派发代理执行对应 SOP；纯路由、最终验证和最终交付不派发给代理。

```text
[前端管理操作请求]
   -> [sop-00-intake-and-routing {主流程：识别实体/动作/边界}]
        -> [sop-01-domain-contract-map {可委派：并行只读发现 UI/IPC/store/schema/测试}]
             -> [sop-02-crud-cli-implementation {主流程实现；可委派测试面/风险审查}]
                  -> [sop-03-import-export-doctor {主流程实现诊断与数据搬运}]
                       -> [sop-04-validate-and-handoff {主流程验证/交付}]
                            -> [Exit]

loop:
  验证失败 -> 收敛失败实体/命令/契约 -> 修复 -> 重跑 fresh verification -> 最多 7 轮或硬阻塞退出

round:
  实体/契约发散 -> 方案和命令收敛 -> 实现验证反馈 -> 下一轮修复或退出

dialectical:
  仅在互斥方案风险相近时启用 -> 多视角对抗评审 -> 主流程裁决
```

每次实际执行前后更新 `todo/status`，状态至少包含 `pending`、`running`、`blocked`、`failed`、`succeeded`、`exited`，并记录当前 SOP、实体集合、产物路径、验证证据和下一步。

## 核心契约

- 默认管理实体包括 `projects`、`habits`、`members`、`deliverables`、`teams`；若仓库已有不同命名，以源码事实为准并建立映射，不擅自发明持久化 schema。
- CRUD 必须覆盖 `list`、`get`、`create`、`update`、`delete`，并按项目实际需要补 `archive`、`restore`、`assign`、`bulk` 等动作。
- CLI 必须在项目构建并安装后可用；若当前项目没有 CLI 入口，先按 `sop-02` 设计并实现可打包入口，再声明完成。
- 导入导出必须有格式版本、dry-run、冲突策略、校验报告和回滚/备份边界；不允许直接覆盖用户数据。
- `doctor` 必须检查 CLI 可执行性、存储路径、schema 版本、权限、i18n、IPC/preload/shared types、数据一致性、导入导出样例和构建产物。
- 前端用户可见文本必须使用 `react-i18next` translation keys，并同步更新 `apps/frontend/src/shared/i18n/locales/{en,fr,zh-CN}/`。
- 涉及平台路径、进程、安装位置或可执行文件发现时，优先使用项目已有平台抽象，不直接散落平台判断。
- 修改 IPC、preload、shared types、启动/关闭、MCP Gateway、Workbench Runtime 或文档规则前，按项目规则先读对应 `docs/` 入口。
- 当存在多个实现方案时，委派代理执行 reasoning-map 收敛候选路径，再比较可行性、风险和置信度。
- 若存在上游生成物或状态交接，委派代理执行 reasoning-map 检查生产者、提交点和消费者，并检查时序边界。
- 交付前委派代理执行 reasoning-map 检查是否仍有未闭环 RED 节点，补齐关键信息后再继续。

## 资源索引

- `references/sop-00-intake-and-routing.md`: 识别管理实体、动作、边界、成功标准和路由。
- `references/sop-01-domain-contract-map.md`: 建立 UI、IPC、preload、shared types、store、持久化、测试和 CLI 的源码图谱。
- `references/sop-02-crud-cli-implementation.md`: 实现 CRUD、批量操作、CLI 命令、帮助文本和打包入口。
- `references/sop-03-import-export-doctor.md`: 实现导入导出、dry-run、冲突策略、诊断和修复建议。
- `references/sop-04-validate-and-handoff.md`: fresh verification、打包安装验证、证据、RED 和交付。
- `templates/cli-command-spec.md`: 管理域 CLI 命令规格模板。
- `templates/domain-contract-map.md`: 实体到 UI/API/store/schema/测试的映射模板。
- `references/target-skill-execution-model.md`: 本 skill 的执行模型选择、派发条件和退出语义。
- `evals/evals.json`: 触发与验收 prompt 样例。

## 交付标准

完成声明必须包含：实体覆盖范围、UI 与 CLI 的数据契约、实际修改文件、导入导出格式、doctor 检查项、fresh verification 命令与结果、安装后 CLI 验证状态、未验证外部范围和剩余 RED。没有运行构建或安装后 CLI 时，只能声明为未验证或 blocked，不能写成完成。
