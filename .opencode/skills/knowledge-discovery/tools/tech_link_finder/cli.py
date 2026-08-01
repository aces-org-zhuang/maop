import argparse
import datetime as _dt
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Iterable, Optional

import requests


_BULLET_RE = re.compile(r"^\s*[-+*]\s+")


@dataclass(frozen=True)
class LinkItem:
    kind: str  # "article" | "repo"
    title: str
    url: str
    source: str
    score: Optional[int] = None
    published_at: Optional[str] = None


def _read_queries_from_markdown(path: str) -> list[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    queries: list[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if not _BULLET_RE.match(line):
                continue

            # Prefer quoted query like: - "LLM inference optimization" 2026
            # If not quoted, fall back to the bullet text.
            quoted = re.findall(r"\"([^\"]+)\"", line)
            if quoted:
                q = " ".join(quoted)
            else:
                q = _BULLET_RE.sub("", line)
            q = q.strip()
            if q:
                queries.append(q)

    # Deduplicate but keep order
    seen = set()
    out: list[str] = []
    for q in queries:
        if q in seen:
            continue
        seen.add(q)
        out.append(q)
    return out


def _hn_search(query: str, hits: int, timeout_s: int) -> list[LinkItem]:
    url = "https://hn.algolia.com/api/v1/search_by_date"
    params = {"query": query, "tags": "story", "hitsPerPage": str(hits)}
    r = requests.get(url, params=params, timeout=timeout_s)
    r.raise_for_status()
    data = r.json()
    items: list[LinkItem] = []
    for hit in data.get("hits", []):
        title = hit.get("title") or hit.get("story_title") or "(no title)"
        link = hit.get("url") or hit.get("story_url")
        if not link:
            continue
        published_at = hit.get("created_at")
        score = hit.get("points")
        items.append(
            LinkItem(
                kind="article",
                title=str(title),
                url=str(link),
                source="HackerNews",
                score=int(score) if isinstance(score, int) else None,
                published_at=str(published_at) if published_at else None,
            )
        )
    return items


def _github_repo_search(query: str, hits: int, timeout_s: int) -> list[LinkItem]:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        return []

    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": str(hits)}
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "knowledge-discovery-sources/1.0.1",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    r = requests.get(url, params=params, headers=headers, timeout=timeout_s)
    # If token is present but invalid, don't hard fail the whole run.
    if r.status_code >= 400:
        return []
    data = r.json()

    items: list[LinkItem] = []
    for repo in data.get("items", []):
        full_name = repo.get("full_name") or "(unknown)"
        html_url = repo.get("html_url")
        desc = (repo.get("description") or "").strip()
        stars = repo.get("stargazers_count")
        title = f"{full_name} - {desc}" if desc else str(full_name)
        if not html_url:
            continue
        items.append(
            LinkItem(
                kind="repo",
                title=title,
                url=str(html_url),
                source="GitHub",
                score=int(stars) if isinstance(stars, int) else None,
                published_at=repo.get("updated_at"),
            )
        )
    return items


def _dedupe(items: Iterable[LinkItem]) -> list[LinkItem]:
    seen = set()
    out: list[LinkItem] = []
    for it in items:
        key = (it.kind, it.url)
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out


def _to_markdown(queries: list[str], by_query: dict[str, list[LinkItem]]) -> str:
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = []
    lines.append("# Tech Links (AI Research)")
    lines.append("")
    lines.append(f"Generated at: {now}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")

    total_articles = sum(
        1 for q in queries for it in by_query.get(q, []) if it.kind == "article"
    )
    total_repos = sum(
        1 for q in queries for it in by_query.get(q, []) if it.kind == "repo"
    )
    lines.append(f"- Queries: {len(queries)}")
    lines.append(f"- Articles (HN): {total_articles}")
    lines.append(f"- Repos (GitHub): {total_repos}")
    lines.append("")

    for q in queries:
        items = by_query.get(q, [])
        if not items:
            continue
        lines.append(f"## Query: {q}")
        lines.append("")
        lines.append("| Type | Title | Source | Score | Time | Link |")
        lines.append("|------|-------|--------|-------|------|------|")
        for it in items:
            score = "" if it.score is None else str(it.score)
            t = "" if not it.published_at else str(it.published_at)
            title = it.title.replace("|", " ")
            link = it.url
            lines.append(
                f"| {it.kind} | {title} | {it.source} | {score} | {t} | {link} |"
            )
        lines.append("")

    return "\n".join(lines) + "\n"


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="knowledge-discovery-sources", add_help=True)
    p.add_argument(
        "--input", required=True, help="Markdown file containing bullet queries"
    )
    p.add_argument("--output", required=True, help="Markdown output path")
    p.add_argument("--max-queries", type=int, default=8, help="Max queries to run")
    p.add_argument("--hn-hits", type=int, default=5, help="HN hits per query")
    p.add_argument(
        "--gh-hits",
        type=int,
        default=5,
        help="GitHub repos per query (requires GH_TOKEN)",
    )
    p.add_argument("--timeout", type=int, default=20, help="Request timeout seconds")
    p.add_argument(
        "--debug-json", default="", help="Optional path to write raw JSON results"
    )
    args = p.parse_args(argv)

    queries = _read_queries_from_markdown(args.input)
    if not queries:
        print("No queries found in input file.", file=sys.stderr)
        return 2

    queries = queries[: max(1, args.max_queries)]

    by_query: dict[str, list[LinkItem]] = {}
    raw_debug: dict[str, dict[str, object]] = {}
    for q in queries:
        items: list[LinkItem] = []
        hn_items: list[LinkItem] = []
        gh_items: list[LinkItem] = []
        hn_error: str = ""
        gh_error: str = ""

        try:
            if args.hn_hits and args.hn_hits > 0:
                hn_items = _hn_search(q, hits=args.hn_hits, timeout_s=args.timeout)
        except requests.exceptions.RequestException as e:
            hn_error = f"{type(e).__name__}: {e}"

        try:
            # Treat gh-hits <= 0 as an explicit opt-out. This avoids hard failures
            # in environments where GitHub is slow/blocked.
            if args.gh_hits and args.gh_hits > 0:
                gh_items = _github_repo_search(
                    q, hits=args.gh_hits, timeout_s=args.timeout
                )
        except requests.exceptions.RequestException as e:
            gh_error = f"{type(e).__name__}: {e}"

        items.extend(hn_items)
        items.extend(gh_items)
        by_query[q] = _dedupe(items)
        raw_debug[q] = {
            "hn": {
                "items": [it.__dict__ for it in hn_items],
                "error": hn_error,
            },
            "github": {
                "items": [it.__dict__ for it in gh_items],
                "error": gh_error,
            },
        }

    md = _to_markdown(queries, by_query)
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md)

    if args.debug_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.debug_json)), exist_ok=True)
        with open(args.debug_json, "w", encoding="utf-8") as f:
            json.dump(raw_debug, f, ensure_ascii=False, indent=2)

    print(f"Wrote: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
