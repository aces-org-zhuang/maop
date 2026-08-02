# Selection Evaluation - Detailed Workflow

本文件记录开源仓、框架、库、SDK 或其他依赖选型的详细执行步骤。它是 `technical-design` 的参考流程，不强制项目使用固定目录或固定 workflow runtime。

## Artifact Root

- 优先使用项目已有设计产物目录。
- 没有约定时，先声明并确认 `{selection_artifact_root}`。
- 临时 clone、扫描和缓存使用 `{temp_root}` 或项目允许的临时目录。

## 阶段一：候选清单和推荐

### 任务1：收集用户需求
- 询问搜索关键词（必填）
- 询问编程语言偏好（可选）
- 询问最小star数要求（默认100）
- 询问需要评估的项目数量（默认10）
- 明确这是解决方案依赖选型，不是 research 样本选择；记录目标能力、必须条件、项目构建方式、包管理器、运行时平台、license 边界和禁用项。
- 保存配置到 `{selection_artifact_root}/config.md` 或项目既有设计记录。

### 任务1b：执行 reasoning-map 门禁
- 在推荐候选前，使用 `reasoning-map` 自顶向下推演目标能力、系统架构级方案形态、关键能力块、现有项目边界、候选依赖、集成路径、构建/测试影响、license/security 风险和退出路径。
- 先形成系统级候选空间，再拆到子系统/模块级候选，最后才进入底层库、SDK、框架或具体实现依赖候选；不要从底层库清单直接反推整体方案。
- 每轮选型必须记录候选清单变化：新增了什么、删除了什么、为什么扩大范围、为什么收敛范围、哪些 RED 点仍需继续推演。
- 推荐项关键结论置信度必须 >=90%；低于 90% 时，输出 RED 点和补证动作，不得定版或进入实现计划。
- 置信度依据必须来自可追踪证据，例如 README/API 文档、release、license、security advisory、示例集成、包管理元数据、构建/测试 probe 或项目约束。

### 任务1c：建立自顶向下候选层级
- Architecture-level：系统级方案形态、关键能力组合、是否依赖现成平台/框架/服务，先排除会导致大规模自研或重复造轮子的方向。
- Subsystem/module-level：按能力块选择可组合的模块、服务、SDK、框架或 CLI，并检查它们是否覆盖目标架构中的必要边界。
- Implementation-level：只有当系统级和模块级边界清晰后，才选择底层库、适配器、插件、驱动、协议实现或具体 repo。
- 保存层级化候选记录到 `{selection_artifact_root}/selection-matrix.md` 或等价选型矩阵。

### 任务2：搜索GitHub项目
- 使用 web_search 搜索 GitHub 项目
- 按 star 数排序
- 过滤符合条件的项目
- 提取项目基本信息（名称、URL、star、描述）
- 保存到 `{selection_artifact_root}/data/projects.csv` 或等价候选表。

### 任务3：获取项目详细信息
- 遍历候选项目列表
- 使用可用 GitHub/API/web 工具获取项目详情。
- 提取关键指标：star数、fork数、issue数、最后更新时间、贡献者数
- 检查 README 质量
- 保存到 `{selection_artifact_root}/data/project-details.csv` 或等价详情表。

### 任务4：评估项目活跃度
- 检查最近 commit 时间
- 统计近3个月的 commit 数
- 检查 issue 响应速度
- 计算活跃度得分（0-10分）
- 保存到 `{selection_artifact_root}/temp/activity-scores.csv` 或等价评估记录。

### 任务5：评估项目成熟度
- 检查项目年龄
- 检查 release 版本数
- 检查文档完整性
- 检查测试覆盖率（如果可获取）
- 计算成熟度得分（0-10分）
- 保存到 `{selection_artifact_root}/temp/maturity-scores.csv` 或等价评估记录。

### 任务6：评估社区健康度
- 统计贡献者数量
- 检查 issue 关闭率
- 检查 PR 合并率
- 检查讨论活跃度
- 计算社区得分（0-10分）
- 保存到 `{selection_artifact_root}/temp/community-scores.csv` 或等价评估记录。

### 任务7：生成综合评分和推荐
- 合并所有评分数据
- 计算加权总分；解决方案适配、集成成本、构建完整性和风险优先级不得低于活跃度、成熟度和社区指标。
- 按总分排序
- 为每个项目生成推荐理由
- 标注推荐权重（高/中/低）
- 标注 `decision_confidence`，推荐进入实现或 POC 的方案必须 >=90%。
- 标注 `selection_convergence`：候选是否已覆盖关键架构能力块、模块边界是否清晰、是否已排除重复造轮子风险、是否还有必须扩大范围的 RED 点。
- 标注 `primary_uniqueness`：同一个 feature/capability/module 是否只有一个 primary 依赖；同质候选必须降级为 fallback、alternative 或 rejected，并说明不同时引入的原因。
- 生成备选清单报告
- 默认继续生成后续依赖分析；只有用户明确要求确认、primary 唯一性无法判断、required 配置/授权缺失或关键 tradeoff 需要用户偏好时才等待确认。
- 输出：`{selection_artifact_root}/candidates.md`

### 任务8：分析项目依赖关系
- 检查项目间是否存在直接依赖
- 分析技术栈重叠
- 识别互补关系
- 检查同质依赖冲突：如果两个候选覆盖同一特性或模块边界，必须收敛到一个 primary；另一个只能作为 fallback/alternative/rejected，不能一起进入依赖图。
- 标注依赖层级（基础设施层/应用层）
- 生成依赖关系图（ASCII）
- 标注建议引入方式：package/SDK/framework/service/CLI/submodule；默认以声明依赖接入，非必要不 fork、不 patch、不复制源码自研化。
- 保存到 `{selection_artifact_root}/dependencies.md`

## 阶段二：安全扫描和暴露面分析

### 任务9：License合规性分析
- 识别项目 License 类型（MIT/Apache/GPL/BSD等）
- 分析 License 感染性（强感染/弱感染/无感染）
- 统计代码行数（使用 cloc 或 tokei）
- 评估代码仓活跃度（commit频率、贡献者数）
- 评估成熟度（项目年龄、版本数）
- 搜索业界应用案例（知名公司使用情况）
- 分析受众类型（企业级/个人开发者/学术研究）
- 保存到 `{selection_artifact_root}/license-security-risk.md` 或项目既有 license 风险记录。
- 列：代码仓名称、链接、License类型、感染分析、活跃度、行数、成熟度、业界应用、受众类型

### 任务10：安全漏洞扫描
- 使用 [skill: github] 检查 Security Advisories
- 检查依赖项漏洞
- 查看 CVE 记录
- 统计漏洞数量和严重程度
- 保存到 `{selection_artifact_root}/data/security-scan.csv` 或等价安全扫描记录。

### 任务11：暴露面分析
- 浅克隆项目到 `{temp_root}/repos/` 目录（depth=1）
- 扫描配置文件中的网络监听设置（如端口、host配置）
- 检查默认配置的暴露风险（如0.0.0.0监听、默认密码）
- 分析 README 和 docs 中的部署说明
- 检查环境变量要求和敏感配置
- 统计第三方依赖数量和风险等级
- 生成暴露面报告
- 默认继续进入功能版图分析；只有 license/security RED 阻塞、required 配置/授权缺失或用户明确要求确认时才等待确认。
- 输出：`{selection_artifact_root}/license-security-risk.md`

## 阶段三：功能版图分析

### 任务12：功能模块梳理
- 使用已克隆的代码（`{temp_root}/repos/`）
- 扫描 README.md 提取使用场景和示例
- 检查 docs/ 目录获取教程和用例
- 读取 examples/ 或 demo/ 目录的示例代码
- 提取 issue 和 discussion 中的高频使用场景
- 识别主要功能入口和 API
- 保存到 `{selection_artifact_root}/data/usecases.csv` 或等价功能覆盖记录。

### 任务13：生成功能版图
- 基于 usecases.csv 整理使用场景
- 用 EARS 句法表述（WHEN <触发条件> IF <前置条件> THEN <系统行为>）
- 按场景分类（核心场景、扩展场景、边缘场景）
- 对比不同项目的场景覆盖度
- 绘制场景关系图（ASCII）
- 生成功能版图报告
- 默认继续进入集成建议；只有功能覆盖方向需要用户偏好、required 配置/授权缺失或用户明确要求确认时才等待确认。
- 输出：`{selection_artifact_root}/feature-coverage.md`

## 阶段四：集成建议

### 任务14：生成集成建议
- 先读取 `references/sop-03c-deployment-integration.md`，按 deployment-first adoption order 声明依赖引入方式、版本锁定策略、构建/测试完整性保障、license/security 处理和回滚/替换路径。
- 优先考虑 managed service/API、package、SDK/framework、CLI/release binary、container image、system package 或 pinned submodule；只有部署引入不足时才设计 source-build、fork/patch 或自研替代。
- 目录规划必须统一到项目 tech 流水线：优先使用项目已有 scripts/tools/infra/ops/build/docker/artifacts/config 规范；没有规范时先提出候选并通过 Configuration Readiness Gate 确认，不默认 `.aces/deploy` 或历史脚本目录。
- 如果设计 build/install 入口，只定义命令契约、配置来源、输出产物、日志位置和验证信号；真实安装、构建、镜像构建或脚本生成转入 `implementation-delivery`。
- 只有存在明确不可替代缺口、上游不可接受修复、license 允许且维护成本可控时，才建议 fork/patch 或自研替代；必须把该判断作为 RED 风险交给用户确认。
- 需要真实集成、安装、验证或交付时，转入 `implementation-delivery`。
- 只需要方案表达、部署流程图或演示材料时，转入 `expression-delivery`。
- 输出：`{selection_artifact_root}/integration-plan.md`

### 任务15：生成项目软件构建图
- 输出 `{selection_artifact_root}/software-build-map.md`，使用 ASCII 或 Mermaid 展示项目软件构建图。
- 图中必须清晰区分 first-party 自研组件、third-party 开源组件、外部服务/CLI/SDK、构建工具链和运行时边界。
- 对每个开源组件标注引入方式（package/SDK/framework/service/CLI/submodule）、adoption form（service/API、package、SDK/framework、CLI/binary、image、system package、submodule、source-build、fork/patch/self-build）、为什么不采用更高优先级部署方式、版本锁定位置、license/security 检查点和 build/test 验证命令或等价验证动作。
- 对每个自研组件标注它消费哪些开源组件、输出哪些构建产物、在哪个环节被测试或打包。
- 图后必须补充 Markdown table，记录组件间交互逻辑和关键 IPO（输入、处理、输出）；复杂字段放进表格，不要污染构建图可读性。
- 如果构建图中存在 fork/patch/源码复制或自研替代，必须标为 RED 风险并说明为什么声明依赖不足。
