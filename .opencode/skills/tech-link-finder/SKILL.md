---
name: tech-link-finder
description: "Combine wide-area keyword search with time-series analysis to intelligently discover and collect latest technical articles, open source projects, and high-quality technical content. Use when searching for: (1) Latest technology articles and tutorials, (2) New open source projects, (3) Building technical knowledge bases, (4) Understanding technology trends, (5) Finding learning resources, (6) Technology selection research."
---

# Tech Link Finder

## Overview

Intelligent technical link discovery system combining broad keyword search with time-series trend analysis to identify high-quality, valuable technical content.

## Core Capabilities

### 1. Smart Link Discovery
- **Wide-area keyword search**: Multi-level keyword granularity from broad to specific
- **Web search aggregation**: Discover latest technical articles via web_search
- **GitHub project mining**: Find popular and emerging open source projects
- **Multi-language support**: Search Chinese and English technical content
- **Domain classification**: AI, frontend, backend, DevOps, mobile development, etc.

### 2. Time-Series Trend Analysis
- **Keyword popularity tracking**: Analyze technical keyword popularity over time
- **Trend identification**: Detect rising, mature, and declining technologies
- **Growth rate calculation**: Calculate month-over-month and year-over-year growth
- **Dynamic ranking**: Rank technical keywords by popularity for different time periods

### 3. Quality Content Filtering
- **Hotness-weighted sorting**: Intelligently sort links based on trend hotness
- **Time window optimization**: Prioritize content from optimal time periods
- **Quality assessment**: Combine Star counts, update frequency, source authority
- **Relevance analysis**: Ensure content highly relevant to keywords

### 4. Smart Knowledge Base Construction
- **Multi-dimensional classification**: Organize by tech stack, hotness, type, importance
- **Metadata extraction**: Title, description, publish time, author, hotness index
- **Deduplication mechanism**: Avoid duplicate link collection
- **Regular updates**: Auto-refresh expired links, maintain freshness

## Usage Patterns

### Exploration Mode
```bash
# Broad exploration from wide keywords
tech-link-finder --query "AI" --mode explore

# Analyze trend after broad search
tech-link-finder --query "machine learning" --trend hot --period 3month

# Discover emerging technologies
tech-link-finder --query "emerging tech" --filter emerging
```

### Trend Analysis Mode
```bash
# Analyze single technology trend
tech-link-finder --query "React" --analyze trend --period 12month

# Compare multiple technologies
tech-link-finder --query "React,Vue,Angular" --compare trend

# Predict emerging technologies
tech-link-finder --query "future tech" --predict emerging --timeframe 6month
```

### Targeted Collection Mode
- 使用web-search进行检索
- 使用playwright查找

## Trigger Keywords

Use this skill when user mentions:
- "最新" + "技术文章" / "教程" / "项目"
- "发现" + "开源项目" / "GitHub项目"
- "搜索" + "技术资源" / "学习资料"
- "收集" + "技术链接" / "知识库"
- "趋势" + "技术" / "框架" / "工具"

## Technical Sources

### Enterprise Blogs
- Alibaba Cloud, Tencent Engineering, Huawei Developer Community
- ByteDance Tech Blog, Baidu AI Open Platform, Meituan Tech Team

### Technical Communities
- CSDN, Juejin, InfoQ China, OSCHINA, V2EX, SegmentFault

### International Sources
- Medium Tech Blogs, Dev.to, Hacker News, Reddit Programming, Stack Overflow Blog

### Mobile & Social
- WeChat Official Accounts, Zhihu Columns, Bilibili Tech, Xiaohongshu

## Best Practices

### Search Optimization
- Use specific technical terms instead of generic words
- Add time constraints (latest, 2026, this month)
- Combine multiple related keywords
- Target specific technical sources

### Quality Assurance
- Prioritize official documentation and known technical blogs
- Focus on major tech teams and expert authors
- Consider Star counts and update frequency
- Verify link validity and freshness

### Knowledge Management
- Regularly update collected links
- Establish classification system for easy retrieval
- Record value and usage scenarios of links
- Create collections by source type

## Key Features

### Search Mode Evolution
1. **Explore**: Broad keyword exploration
2. **Analyze**: Trend analysis of discovered technologies
3. **Targeted**: High-quality content collection based on analysis
4. **Optimized**: Continuous monitoring and updates
5. **Auto**: One-click complete process ⭐

### Time-Series Analysis
- Real-time hotness tracking
- Trend prediction based on historical data
- Seasonal pattern detection
- Anomaly detection for sudden hotspots

### Smart Filtering
- Hotness-weighted sorting
- Multi-dimensional quality assessment
- Relevance matching
- Freshness control
- Source authority weighting


## References

For detailed command options, search strategies, and configuration:
- references\workflow.md - Workflow for discovery, analysis, collection, and organization
