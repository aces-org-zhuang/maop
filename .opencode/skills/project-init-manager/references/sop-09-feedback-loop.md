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
  -> vendor/ai/maop/
  -> maop 自身 .opencode 和仓库规则
  -> 主仓只记录消费关系、pinned commit 和验证方式
```

## 执行规则

1. 每次新增、重命名或删除索引型文件，必须同步对应 index。
2. 文档常读入口保持短，长推演和阶段过程不要塞进 README。
3. 行动前若涉及复杂问题、架构、文档体系、研究边界或 submodule，先用 `reasoning-map`。
4. 行动后再用 `reasoning-map` 复核是否覆盖原 RED 点。
5. 验证事实优先使用真实命令、测试、日志、Workbench feedback 或源码路径，不只靠口头描述。
6. 技术栈细则只在目标项目出现真实配置、源码、测试或用户确认后写入；不要通过 profiles 或 overlays 预置多套规则。

## 长期维护信号

- 新增顶层目录后，根 `AGENTS.md` 和 README 是否知道它。
- 新增 docs 文件后，最近的 README 或 index 是否能找到它。
- 新增研究课题后，研究区 index 是否有续点。
- 新增 submodule 后，`.gitmodules` 和 docs 索引是否一致。
- maop 变更是否留在 maop submodule 内，项目仓只更新 pinned commit 或消费文档。
- 修复 bug 后，是否需要失效模式或实现证据记录。

## 常见 RED 点

- 只在最终回复中说明变更，没有落盘到 docs 或 index。
- 研究成果直接污染主仓 docs。
- 失效模式、调试记录、证据文件没有同步索引。
- 规则变更只改根 AGENTS，未同步 docs 局部规则。
