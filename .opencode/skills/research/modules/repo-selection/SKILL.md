---
name: repo-selection
description: |
  代码仓选型 skill：在 research 统一入口下，基于研究主题与约束，生成候选代码仓清单、评分维度与选型结论，并写入根入口传入的 vendor/research/aces-research/topics/<research_slug>/selection/ 与 repos-index.md。
---

# Repo Selection

## 输入
- 研究主题（topic）与目标
- 技术栈偏好（可选）
- 约束（stars/license/活跃度等，可选）
- `{research_root}`：由统一入口指定，格式必须是 `vendor/research/aces-research/topics/<research_slug>`；缺失时先回到根入口确定，不要自行猜测

## 输出（必须写入）
- `{research_root}/selection/candidates.md`
- `{research_root}/selection/selection.md`
- `{research_root}/repos-index.md`

## 约束
- 选择任何核心样本仓库前，必须先使用 `reasoning-map` 执行研究对象门禁推演，先判断研究主题的直接系统对象、用户工作流、系统边界、架构闭环和底层依赖层级；不要直接从关键词相似度进入仓库清单。
- 选型过程本身必须符合 `reasoning-map` 推演模式：先从系统架构级研究对象和架构闭环建立候选空间，再下钻到子系统/模块级样本，最后才考虑底层实现或基础设施样本；不得跳过系统级和模块级直接进入底层技术栈。
- 候选清单必须迭代演进：每轮 reasoning-map 可以增加候选、删除候选、扩大搜索范围或收敛范围；`candidates.md` 和 `selection.md` 必须记录每轮扩展/收敛原因、RED 点和退出条件。
- 只有满足收敛条件时才冻结核心样本：Level1 直接研究对象覆盖关键架构能力块、兄弟候选已比较、重复造轮子风险已排除、Level0 只作为必要支撑对象、未闭环 RED 点不再阻塞研究目标。
- 输出必须可追溯：包含仓库URL、选择理由、评分维度、层级归属和 evidence notes。
- 多因子选型：课题直接性 / 工作流一致性 / 架构一致性 / 产物一致性 / 代码质量 / 文档 / 社区活跃度 / 技术相关性。
- 核心样本仓库必须满足 `topic_directness >= 0.90`，并在 `selection.md` 说明置信度依据；低于 0.90 的仓库只能进入候选池或 Level0 支撑技术池，不能写入冻结核心样本。
- 必须先覆盖足够的 Level1 直接研究对象，再扩展 Level0 底层支撑对象。Level1 指与课题在问题域、研发/用户工作流、系统边界和架构闭环上直接同构的开源项目；Level0 指 RAG、向量库、LLM orchestration、workflow engine、sandbox、browser automation、terminal execution、MCP 等底层能力或依赖。
- 当研究主题是 AI 辅助研发、自动化编程、coding agent、软件工程 agent、代码修改/验证闭环时，优先选择自动化编程或 AI coding agent 开源项目作为 Level1；不要把 RAG、向量数据库、通用 agent 框架或 prompt framework 作为主研究对象，除非它们被证明补足了 Level1 架构中的关键瓶颈。
- 如果候选清单主要由 Level0 基础技术栈组成，或缺少 Level1 代表性样本，必须把 selection 标记为 RED/未通过，重新搜索并补齐直接研究对象后再冻结 `repos-index.md`。
- `repos-index.md` 是论文可复现样本边界；深度阅读前必须冻结或明确标记为暂定。
- 进入核心样本或后续需要源码洞察的仓库，必须记录目标 submodule 路径 `{research_root}/repos/<repo_name>`；不得规划为普通 clone、主仓 `vendor/research/<repo_name>` 或 `aces-research` 根目录子仓。
- 写入后同步更新 `{research_root}/README.md` 的当前阶段、下一步和样本仓库冻结点。
