# Submodule Safety Checklist

执行 submodule 写操作前检查：

- 已读取或检查 `.gitmodules`。
- 已运行或计划运行 `git status --short`。
- 已运行或计划运行 `git submodule status --recursive`。
- 目标 URL、path、用途和消费者已明确。
- 目标路径不存在冲突。
- 目标 submodule 内没有未提交改动。
- 不要求用户粘贴 token、密码或 SSH 私钥。
- 写操作命令已展示给用户确认。
- 新增长期 submodule 后会更新主仓索引。
- 研究工作区锁定路径和 URL 为 `vendor/research/aces-research` -> `https://github.com/aces-org-zhuang/aces-research.git`。
- AI 引擎锁定路径和 URL 为 `vendor/ai/maop` -> `https://github.com/aces-org-zhuang/maop.git`。
- 研究参考仓路径为 `vendor/research/aces-research/topics/<research_slug>/repos/<repo_name>`。
