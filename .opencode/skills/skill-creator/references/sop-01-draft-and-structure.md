# SOP-01 Draft and Structure

## Goal and scope

创建新技能或重构已有技能，保留可复用能力并建立短入口、SOP、资源索引和质量链。入口应低于 300 行；本 SOP 承载原有创建、访谈、写作和结构指导。

## Inputs and outputs

Inputs：`sop-00` intake、用户确认的目标/触发/输出/测试意愿、旧 `SKILL.md` 和目录树。Outputs：frontmatter、目标 skill 的执行模型 ASCII 图、router、`references/sop-NN-<feature>.md`、真实资源索引、必要 eval/workspace 计划。只写用户授权的 skill 目录。

## Capture intent

回答并记录：技能让 Claude 做什么；何时触发；预期输出格式；是否设置可验证测试。主动识别边界条件、输入输出、示例文件、依赖和成功标准。复杂修改前先运行 reasoning-map，覆盖目标、触发面、阶段边界、输入、输出、产物、验证、反馈和 RED。

## Design rules

1. frontmatter 保留 `name`、触发导向的 `description`，名称不随改版改变；必要时补 `compatibility`。
2. `SKILL.md` 只做 orientation、首次动作、condition router、完整顺序、资源索引、交付标准。
3. 目标 skill 的执行模型必须显式提示主 LLM 在明确条件下委派代理执行 SOP，并在 ASCII 图里具体指向至少一个真实的 `sop-00-*` / `sop-01-*` / `sop-02-*` / `sop-03-*` 节点；SOP 只是标准流程，不能直接替代执行模型。
4. 目标 skill 的执行模型必须从任务依赖树、round、loop、dialectical 四种基础模型中选择一个或多个组合；不要默认全量聚合。
5. 目标 skill 的执行模型必须要求在实际执行前后更新 `todo/status`，避免目标丢失；每个阶段性动作都要有状态流转点。
6. 阶段细节进入连续编号的 `references/sop-00-*`、`sop-01-*`；每个 SOP 写 goal、pre-read、steps、write boundary、validation、RED。
7. 资源渐进加载：metadata -> router -> 当前 SOP -> `references/target-skill-execution-model.md` -> 目标 skill 的 `templates/`、`checklists/`、`assets/`、`scripts/`。不要把长 schema、例子或实现细节塞回入口，也不要把本技能 bundled 目录和目标 skill 运行时目录混为一谈。
8. 路由、验收和 IPO 只在需要提高可读性时使用结构化列表或表格；生命周期和 producer -> artifact -> validator -> consumer 用 ASCII/Mermaid 表达，细节放在对应 SOP 或目标 skill 资源中。
9. 解释 why，优先祈使句，避免无意义的强制大写；描述聚焦用户意图而非实现。
10. 不写恶意、误导、越权、数据外泄或未经授权的外部副作用。

## Creation flow

```text
intent -> trigger boundary -> output contract -> stage map -> write -> validate -> eval plan
```

先产出 SOP-routed 结构草案，再写正文。新技能默认至少包含 `SKILL.md`、`references/sop-00-intake-and-routing.md`、`references/sop-01-dispatch-execute.md`、`references/sop-02-validate-and-handoff.md` 和 `references/sop-03-handoff.md`；目标 `SKILL.md` 的 ASCII 执行模型必须直接索引这些 SOP 节点，并在满足并行、验证或对抗条件时写明主 LLM 委派代理执行对应 SOP。新技能至少设计 2-3 个真实测试 prompt；有客观输出时把 prompt 和 expectation 保存到目标 skill 的 `evals/evals.json`（若该目录由用户授权且存在/可创建），不能把本技能 bundled 目录误当成目标 skill。

## Existing skill improvement

先保存旧版本到用户授权的 workspace snapshot，再运行 old-skill baseline；比较实际 transcript 和输出，不只比较最终文本。泛化用户反馈，避免只为单个案例增加窄规则；删除不产生行为的冗余指令；重复的 helper 行为应优先沉淀到 `scripts/`。

## Full-link quality chain

必须保持：

```text
Intake -> reasoning-map -> router -> SOP/artifact -> validation/evals -> feedback -> handoff
```

配置就绪后再执行 POC、写入、外部 CLI、构建、打包或验证。需要代理时使用 `sop-00` 的边界和返回合同；最终决策留在主 LLM。失败的 trigger、路由、评测、review、密度或 confidence 应进入有限 auto-remediation round，而非直接要求用户兜底。

## Validation and RED

验证 frontmatter、入口行数、编号连续、引用真实、SOP 独立可读、边界明确、无重复关键规则。常见 RED：入口列了 SOP 却没说明何时读；SOP 缺输入/输出/验证；只优化描述不验证执行；添加资源未更新索引；代理替主 LLM 做最终决策；开始写入前未确认配置。

## Return contract

```text
Finding: <结构和保留能力>
Evidence: <旧/新文件路径与行号>
Confidence: <0..1>
Fidelity: <保留原能力及已迁移部分>
RED: <未覆盖项>
Excluded scope: <未改动目录/未运行外部测试>
Next step: <进入 sop-02/03/04/05>
```
