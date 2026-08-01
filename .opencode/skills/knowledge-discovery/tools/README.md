# knowledge-discovery technical source tool (minimal)

This is a minimal, self-contained implementation used by the research ticket template.

Data sources:
- Hacker News Algolia API (articles)
- GitHub Search API (projects) if `GH_TOKEN` is available

Usage:

```bash
python -m tech_link_finder --input path/to/search_keywords.md --output path/to/technical-sources.md
```
