# SOP 01: Pipeline Routing

按请求选择 path，支持部分执行，不强制完整论文链路。

## Routing

- 资料、链接、趋势、学习资源、知识库、tool/skill 查找 -> Discovery Path。
- 微信关键词搜索、公众号搜索、搜狗微信搜索 -> Weixin Search Path。
- `mp.weixin.qq.com` URL 阅读/总结/提取 -> WeChat Extraction Path。
- 创新方法论、TRIZ、蓝海、设计思维、精益创业、创新机会 -> Innovation Discovery Path。
- 仓库 URL、开源样本、源码洞察、仓库对比 -> Repo Research Path。
- 证据包、claim-evidence、来源验证 -> Evidence Path。
- 论文模型、选题、大纲、核心观点 -> Paper Path。

## Partial Execution

- 用户只要求一个 path 时，只执行该 path。
- 多 path 请求按依赖顺序执行最小闭环。
- 每个 path 完成后更新 `{research_root}/README.md` 的 completed_paths、artifacts、next_suggestions 和 risks。
- 不为轻量请求自动执行仓库研究、证据包或论文建模。
