---
name: knowledge-discovery
description: Use when the user needs external knowledge, technical links, latest articles, WeChat mp.weixin.qq.com extraction, learning resources, trend discovery, tool/skill discovery, or wants to find/install agent skills. Routes search, source extraction, skills ecosystem lookup, source quality filtering, and handoff to research, technical-design, or expression-delivery.
---

# Knowledge Discovery

统一承接“找资料、找链接、读文章、发现工具/skill、构建轻量知识库”的入口。它替代分散的技术链接发现、微信文章提取和 skill 生态查找入口，但不吞并深度研究、开源仓选型或表达产物生成。

## Trigger Matrix

- 用户提供 `mp.weixin.qq.com` 并要求阅读、总结、分析或提取信息：使用 WeChat extraction path。
- 用户要求“最新技术文章 / 教程 / 学习资料 / 技术趋势 / 技术链接 / 知识库”：使用 technical source discovery path。
- 用户要求“找 skill / 有没有 skill / 如何扩展 agent 能力 / 安装某个 skill”：使用 skills ecosystem path。
- 用户要求深度研究、论文、证据包或课题续点：只做 sources discovery 后转入 `research`。
- 用户要求开源仓候选评估、技术选型或依赖选型：发现候选后转入 `technical-design` 的 Selection Evaluation 子阶段。
- 用户要求把发现结果做图表、slides、原型、图片或可视化：转入 `expression-delivery`。

## Non-goals

- 不替代 `research` 的研究工作区、证据包和论文流水线。
- 不替代 `technical-design` 的技术选型决策、风险比较和验证策略。
- 不替代 `expression-delivery` 的视觉、图表、slides、图片和原型产物。
- 不安装或运行第三方 skill，除非用户明确同意。

## Workflow

1. Intake Gate：明确用户要找的是 source、article、skill/tool，还是混合需求。
2. Scope Gate：确认主题、语言、时效性、来源类型、质量阈值和输出格式。
3. Discovery Gate：按路径使用 web search、browser、GitHub search、skills CLI 或已有资料。
4. Extraction Gate：对网页、微信文章、GitHub repo 或 skill metadata 提取结构化信息。
5. Quality Gate：按来源权威性、时效性、相关性、可访问性、重复度和安全性筛选。
6. Synthesis Gate：输出链接索引、摘要、来源表、趋势判断、学习路径或候选清单。
7. Handoff Gate：需要深度研究、开源选型或表达产物时，转入对应流水线。
8. Verification Gate：检查链接有效性、引用来源、浏览器资源释放、安装命令风险和结果可追踪。

## Path: Technical Source Discovery

- 使用宽到窄关键词组合，覆盖中英文资料源。
- 优先官方文档、企业技术博客、主流社区、高质量开源仓和近期资料。
- 可按热度、更新时间、来源权威、相关性、Star/update frequency 排序。
- 需要开源仓进一步比较时，停止在候选清单并转入 `technical-design`。
- 详细流程见 `references/technical-sources/workflow.md`。

## Path: WeChat Article Extraction

- 只在 URL 包含 `mp.weixin.qq.com` 且用户请求阅读/总结/分析/提取时触发。
- 优先使用 browser/Playwright，因为普通 fetch 经常被反爬阻断。
- 加载页面后等待内容稳定，必要时滚动加载懒加载内容。
- 提取标题、正文、关键段落、代码块、图片说明和可引用元数据。
- 结束后关闭浏览器资源。
- 详细安全、技术和输出格式见 `references/wechat-extraction/`。

## Path: Skills Ecosystem Discovery

- 当用户想找 agent skill、工具、模板或工作流时使用。
- 先理解需求域和任务，再搜索 skill 生态。
- 可使用 `npx skills find <query>` 搜索；安装前必须先向用户确认。
- 推荐前检查来源声誉、安装量、GitHub stars、维护状态和权限风险。
- 未找到合适 skill 时，说明结果并可转入 `skill-creator` 创建新技能。

## Quality Rules

- 不把搜索结果原样堆给用户；必须去重、分类、标注来源和价值。
- 外部资料结论必须可追踪到链接或来源描述。
- 对趋势判断标注时间窗口和证据质量。
- 对 third-party skill 安装命令标注作用域、风险和是否需要 `-g`。
- 对微信文章提取标注可能的反爬、登录、图片懒加载或正文缺失风险。

## References And Assets

- `references/technical-sources/workflow.md`: 技术链接发现、趋势分析和知识库整理流程。
- `references/wechat-extraction/TECHNICAL_GUIDE.md`: 微信文章提取技术指南。
- `references/wechat-extraction/SECURITY.md`: 浏览器和 URL 安全规则。
- `references/wechat-extraction/OUTPUT_FORMATS.md`: 摘要与结构化输出模板。
- `references/wechat-extraction/workflow.md`: 微信文章提取工作流。
- `tools/`: 技术链接发现 CLI 原型与辅助脚本。
