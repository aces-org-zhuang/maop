# SOP 03: Weixin Search

通过关键词 + Playwright MCP 检索 `https://weixin.sogou.com/`，扩充微信公众平台来源。

## When To Use

- 用户要求微信关键词搜索、公众号文章搜索、行业案例、中文技术/产品/竞品资料。
- Discovery 或 Innovation path 需要中文高价值来源。

## Steps

1. 先读取 `paths/sop-retrieval-reasoning.md`，用 reasoning-map 规划微信检索的扩展/收敛轮次。
2. 生成 Round 1 关键词组合：主关键词、同义词、行业词、时间词、场景词、公众号类型和反例词。
3. 使用 Playwright MCP 打开 `https://weixin.sogou.com/`。
4. 搜索关键词，收集 title、account、date、snippet、url。
5. 对 Round 1 结果去重、分层、标注线索价值和 RED 点；围绕未闭环 RED 点生成 Round N 关键词再检索。
6. 限制翻页和结果数量，避免高频抓取。
7. 遇到 CAPTCHA、登录、阻断或异常风控时立即停止，不绕过。
8. 可降级为 web search：`site:mp.weixin.qq.com <keywords>`。
9. 对可访问 `mp.weixin.qq.com` 结果，使用 WeChat Extraction Path 提取正文。
10. 写入 `{research_root}/discovery/weixin-search.md` 和 `{research_root}/sources/source-index.md`，并记录每轮扩展/收敛、删除线索原因和退出条件。

## Evidence Rules

- 搜狗搜索结果只是线索，不等同于正文证据。
- 正文证据必须来自可访问文章页或用户提供的可信内容。
- 每条来源标注可访问性、采集时间、公众号、发布时间和摘要可靠性。

## Safety Rules

- 不绕过验证码。
- 不模拟登录账号。
- 不批量高频抓取。
- 不保存敏感 cookie 或账号信息。

## Related Assets

- `assets/discovery/wechat-extraction/`
