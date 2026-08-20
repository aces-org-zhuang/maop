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

### reasoning-map 点状注入库

创建目标 skill 时，按命中场景从下列短句中挑选 1..n 条注入到目标 skill 的执行模型或核心契约中，不展开解释；注入句必须保留“委派代理执行”字样，让目标 skill 的执行模型显式出现可委派语义。

#### diagnosis

- `遇到 bug、异常、回归或未知根因时，委派代理执行 reasoning-map 定位，再进入复现。`
- `当症状与根因不一致时，委派代理执行 reasoning-map 区分直接症状和根本原因。`
- `若存在上游生成物或状态交接，委派代理执行 reasoning-map 检查生产者、提交点和消费者。`
- `当时序可能影响结果时，委派代理执行 reasoning-map 识别竞态、延迟和就绪信号。`
- `定位未收敛前，不直接进入大范围 POC。`

#### design

- `当存在多个方案时，委派代理执行 reasoning-map 比较可行性、风险和置信度。`
- `在方案选择前，委派代理执行 reasoning-map 排除明显不成立的路径。`
- `若方案依赖多个阶段，委派代理执行 reasoning-map 画出依赖链后再实施。`
- `当方案置信度不足时，委派代理执行 reasoning-map 调整到高置信路径，再进入实现。`
- `reasoning-map 负责缩小方案空间，POC 负责验证已收敛假设；必要时委派代理执行 reasoning-map 补充边界。`

#### verification

- `必要时委派代理执行 reasoning-map 验证，直到置信度达到 90% 以上。`
- `在进入 POC、实现或最终交付前，委派代理执行 reasoning-map 收敛候选路径。`
- `若问题仍存在证据缺口，委派代理执行 reasoning-map 补齐关键信息，再继续执行。`
- `若验证结果冲突，委派代理执行 reasoning-map 更新候选和证据。`
- `reasoning-map 用于提升置信度与缩小验证范围，不替代目标 skill 的主功能；必要时委派代理执行 reasoning-map 做复核。`

#### handoff

- `交付前委派代理执行 reasoning-map 检查是否仍有未闭环 RED 节点。`
- `若仍有高风险不确定性，委派代理执行 reasoning-map 边界化后再继续交付。`
- `最终输出前，委派代理执行 reasoning-map 给出最小行动路径。`
- `若结论置信度不足，委派代理执行 reasoning-map 再输出最终结论。`
- `交付结果必须能回溯到 reasoning-map 的关键判断点，必要时委派代理执行 reasoning-map 补证。`

#### poc-gate

- `进入 POC 前，必要时委派代理执行 reasoning-map 验证假设是否足够收敛。`
- `若 POC 成本高，委派代理执行 reasoning-map 降低试错范围。`
- `当验证门槛未达成时，不进入最终交付。`
- `必要时委派代理执行 reasoning-map 反复迭代，直到达到约定置信门槛。`
- `POC 的职责是验证已收敛假设，reasoning-map 的职责是减少验证前的不确定性；必要时委派代理执行 reasoning-map 先做收敛。`

#### timing

- `当状态流转会影响结果时，委派代理执行 reasoning-map 检查时序边界。`
- `若存在异步交接，委派代理执行 reasoning-map 建模生产者、就绪信号和消费者。`
- `当执行顺序可能影响正确性时，委派代理执行 reasoning-map 收敛时序风险，再进入实施。`
- `若结果依赖持久化或提交点，委派代理执行 reasoning-map 验证状态是否已就绪。`
- `reasoning-map 应优先暴露时序风险，而不是等 POC 失败后再发现；必要时委派代理执行 reasoning-map 提前暴露风险。`

#### confidence

- `若目标是比较两个技能方案，委派代理执行 reasoning-map 做选择前收敛。`
- `若用户关注置信度与试错成本，委派代理执行 reasoning-map 评估再进入验证。`
- `若任务可能走错方向，委派代理执行 reasoning-map 排除低收益路径。`
- `当候选很多时，委派代理执行 reasoning-map 把问题缩成少数高置信分支。`
- `reasoning-map 只作为门禁与收敛工具，不改变目标 skill 的核心职责；必要时委派代理执行 reasoning-map 做复核。`

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
