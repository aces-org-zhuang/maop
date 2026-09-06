# SOP 09: Feedback Loop

## 目标

把项目后续开发、调试、研究和实现证据反哺到正确位置，保持仓库长期可维护。

## 反哺路由

```text
代码实现完成
  -> 评估是否写入 docs/evidences/ 并更新 index

观察、定位或修复可复用问题
  -> docs/failure-modes/<timestamp>-<slug>.md
  -> docs/failure-modes/index.md

复杂调试过程
  -> docs/debugs/<timestamp>-<slug>.md
  -> docs/debugs/index.md

长期架构事实、契约、开发规则
  -> docs/ 对应分层目录
  -> 对应 README 或 docs/README.md

非研究类阶段性工程记录
  -> guides/

研究过程、论文、开源项目对比、证据包
  -> vendor/research/aces-research/topics/<research_slug>/
  -> 研究区 index 和课题 README

AI 引擎能力、engine-side skills/agents/commands
  -> maop 源仓模式：本仓 .opencode/ 和 maop 仓库规则
  -> 普通宿主项目：vendor/ai/maop/ submodule
  -> 普通宿主项目主仓只记录消费关系、pinned commit 和验证方式

真实脚本/CLI/构建/测试/部署/外部工具操作
  -> 检查是否存在可迁移作业经验
  -> 脱敏、去项目化、单行化、去重
  -> docs/07-llm/operational-experiences.md
```

## 执行规则

1. 每次新增、重命名或删除索引型文件，必须同步对应 index。
2. 文档常读入口保持短，长推演和阶段过程不要塞进 README。
3. 行动前若涉及复杂问题、架构、文档体系、研究边界或 submodule，先用 `reasoning-map`。
4. 行动后再用 `reasoning-map` 复核是否覆盖原 RED 点。
5. 验证事实优先使用真实命令、测试、日志、Workbench feedback 或源码路径，不只靠口头描述。
6. 技术栈细则只在目标项目出现真实配置、源码、测试或用户确认后写入；不要通过 profiles 或 overlays 预置多套规则。
7. 只影响当前项目业务或架构的内容进入项目 docs；可迁移到多个项目或环境的处理方式进入作业经验。
8. 没有真实验证证据的一次性处理不沉淀为作业经验。
9. 作业经验必须保持单行格式 `[触发条件] -> [动作] -> [验证信号]`，同义经验更新原条目而不是重复追加。

## 长期维护信号

- 新增顶层目录后，根 `AGENTS.md` 和 README 是否知道它。
- 新增 docs 文件后，最近的 README 或 index 是否能找到它。
- 新增研究课题后，研究区 index 是否有续点。
- 新增 submodule 后，`.gitmodules` 和 docs 索引是否一致。
- maop 源仓模式下，maop 能力变更是否留在本仓 `.opencode/`；普通宿主项目是否只更新 maop submodule pinned commit 或消费文档。
- 修复 bug 后，是否需要失效模式或实现证据记录。

## 常见 RED 点

- 只在最终回复中说明变更，没有落盘到 docs 或 index。
- 研究成果直接污染主仓 docs。
- 失效模式、调试记录、证据文件没有同步索引。
- 规则变更只改根 AGENTS，未同步 docs 局部规则。
- 真实作业经验只在最终回复中出现，没有沉淀到经验文件。
- 项目规则、业务事实或长篇复盘误写入作业经验文件。
