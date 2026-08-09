# SOP: Retrieval Reasoning Loop

用于 Discovery、Weixin Search、WeChat Extraction、Innovation Discovery 和 Innovation Report 中的资料检索、链接发现、趋势判断、学习资源、知识库、tool/skill 查找、公众号搜索、文章提取证据化和创新报告素材整合。

## 目标

让检索本身符合 `reasoning-map` 推演模式：先扩展检索空间，再收敛证据，再根据 RED 点继续扩展，再收敛，直到满足退出条件。不要一次性关键词搜索后直接写结论。

## 检索推演循环

```text
[Intake / research question]
  -> [Round N Expand]
       扩展关键词、来源类型、语种、时间窗口、平台、同义词、反例和邻近领域
  -> [Round N Converge]
       去重、分层、证据评级、主题聚类、排除低质来源、标记 RED 点
  -> [Need more evidence?]
       yes -> [Round N+1 Expand]
       no  -> [Final Evidence Set + Exit]
```

## 检索预算

- 轻量请求默认只执行 1 轮 Expand + 1 轮 Converge。
- 标准研究默认最多 3 轮 Expand/Converge。
- 只有存在阻塞结论的 RED 点时才继续扩展；不得为了覆盖面而泛化扩展。
- 超出预算前，先说明当前缺口、继续检索收益和建议停止/继续决策。

## 执行步骤

1. Intake：明确本轮研究问题、目标产物、时间窗口、语种、地域、来源类型、必须覆盖的主题和不需要覆盖的边界。
2. Round 1 Expand：使用 `reasoning-map` 画出系统级检索空间，不只列关键词；至少覆盖主题主线、同义表达、上游背景、下游应用、竞品/替代方案、反例/质疑、中文/英文来源和高质量来源类型。
3. Round 1 Converge：去重、分类、评价来源质量，标注哪些来源可以作为证据，哪些只是线索，哪些 RED 点仍缺材料。
4. Round N Expand：围绕未闭环 RED 点继续增加检索，不盲目扩大；可以增加关键词、平台、公众号、论文、官网、GitHub、标准文档、技术博客、报告、工具目录或专家材料。
5. Round N Converge：收敛到与研究问题直接相关的证据集，删除重复、低可信、过旧、过泛或只提供底层背景但不支撑主问题的来源。
6. Exit Gate：只有当核心问题、关键分支、反例/风险、趋势证据、来源质量和证据缺口都已闭环或明确标为不阻塞时，才停止检索并进入写作、证据化、创新机会或报告输出。

## Path 适配

| Path | Expand 示例 | Converge 示例 |
| --- | --- | --- |
| Discovery Path | 扩展资料、链接、趋势、学习资源、知识库、tool/skill 来源 | 收敛到 source-index、links、technical-sources 和 skills-tools 中的高价值来源 |
| Weixin Search Path | 扩展关键词、公众号、行业词、场景词、时间词和 `site:mp.weixin.qq.com` 查询 | 收敛到可访问、可信、与主题直接相关的公众号文章线索 |
| WeChat Extraction Path | 扩展同主题文章、原文引用、作者/公众号上下文和关联链接 | 收敛为可证据化正文、摘要、关键观点和来源可靠性判断 |
| Innovation Discovery Path | 扩展方法论、痛点、机会、约束、反例、竞品和验证路径 | 收敛为可验证创新机会、假设、风险和 validation-plan |
| Innovation Report Path | 扩展背景、业界方案、创新方案、技术壁垒、取证方法和效果证据 | 收敛为报告章节可引用证据和未闭环风险 |

## 必须落盘

- 轻量请求只需在对应 path 产物或 README 中记录检索轮次、关键来源、收敛依据和未闭环 RED 点。
- 标准研究、报告或证据包任务才需要完整记录扩展范围、删除来源原因，并在 `sources/source-index.md` 区分 evidence、lead、background、rejected 四类来源。
- 生成报告或创新机会前，必须能追溯到已收敛证据集；未收敛材料只能作为假设或风险，不能写成结论。

## 常见 RED 点

- 只搜索一次关键词就写结论。
- 只扩展不收敛，导致来源堆叠。
- 只收敛不再扩展，导致关键 RED 点缺证据。
- 搜索过早掉到底层技术或泛资料，未覆盖系统级问题和直接应用场景。
- 微信搜索结果当作正文证据使用。
- 创新报告中出现没有来源支撑的趋势、壁垒或效果判断。
