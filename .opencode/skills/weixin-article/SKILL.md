---
name: weixin-article
description: Extract and summarize WeChat official account articles (mp.weixin.qq.com) using Playwright browser. Use when user provides a WeChat article URL containing 'mp.weixin.qq.com' AND requests reading, summarizing, analyzing content, or extracting information. Must use browser tool as web_fetch is blocked by anti-scraping mechanisms. Supports content extraction, structured summarization, workflow generation, and visualization creation for technical articles.
---

# Weixin Article Extractor

## Quick Start

Extract and summarize WeChat official account articles using Playwright browser automation. This skill handles anti-scraping measures and provides structured output.

### Basic Usage
- **URL Detection**: Automatically triggers on URLs containing `mp.weixin.qq.com`
- **Content Extraction**: Full article text with title and body content
- **Structured Summary**: Concise summary with key points and insights
- **Visualization**: Automatic chart generation for technical content

### Output Format
```
[Core Summary 100-150 words]
This article covers [main topic]. [Key insights and value proposition]

---

**Background/Problem** [50 words]
**Key Points** [3-5 bullet points]
**Technical Details** [If applicable]
**Visualizations** [Mermaid diagrams for technical content]
**Summary** [20 words]
```

## Workflow

1. **URL Validation**: Verify mp.weixin.qq.com domain
2. **Browser Setup**: Configure anti-detection settings
3. **Content Loading**: Open page and wait for network idle
4. **Scroll Loading**: Execute incremental scrolling for lazy content
5. **Content Extraction**: Capture title and article body
6. **Processing**: Generate summary and visualizations
7. **Cleanup**: Close browser and release resources

## Advanced Features

### Content Extraction Options
- **Full Text**: Complete article content extraction
- **Summary Only**: Condensed version with key points
- **Technical Analysis**: In-depth analysis for development articles
- **Workflow Generation**: Create flowcharts for process documentation

### Anti-Scraping Configuration
- User-Agent spoofing
- Viewport and timezone settings
- Randomized interaction delays
- Network idle detection

### Visualization Support
- **Architecture Diagrams**: For system design articles
- **Flowcharts**: For process and workflow documentation
- **Sequence Diagrams**: For API and integration guides
- **Data Flow**: For data processing pipelines

## References

For detailed implementation guidance, see:

- [references\TECHNICAL_GUIDE.md](references/TECHNICAL_GUIDE.md) - Code extraction, diagram generation, API documentation
- [references\SECURITY.md](references/SECURITY.md) - URL validation, browser security, anti-detection
- [references\OUTPUT_FORMATS.md](references/OUTPUT_FORMATS.md) - Output templates, visualization standards, quality guidelines
- [references\workflow.md](references/workflow.md) - Workflow creation and management

## Checklists

### Pre-Execution
- [ ] URL contains `mp.weixin.qq.com` domain
- [ ] User explicitly requests article processing
- [ ] URL format validation completed
- [ ] Browser resources available

### Execution
- [ ] Browser context configured with anti-detection settings
- [ ] Page loaded and network idle confirmed
- [ ] Content fully loaded via scrolling
- [ ] Title and content successfully extracted
- [ ] Browser resources properly closed

### Post-Execution
- [ ] Content processed and formatted
- [ ] Summary generated within length limits
- [ ] Visualizations created for technical content
- [ ] Output validated for completeness
- [ ] Resources cleaned up successfully

### Troubleshooting
- [ ] Verify URL accessibility and format
- [ ] Check browser automation tool status
- [ ] Confirm anti-scraping measures active
- [ ] Validate extracted content completeness