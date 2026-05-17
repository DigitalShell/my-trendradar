"""Collect RSS items whose titles match watchlist keywords."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import feedparser
import yaml


@dataclass
class NewsItem:
    title: str
    link: str
    source: str


def _load_watchlist(root: Path) -> tuple[list[str], int]:
    path = root / "watchlist.yaml"
    if not path.exists():
        path = root / "watchlist.yaml.example"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    terms = list(data.get("keywords") or []) + list(data.get("symbols") or [])
    max_items = int(data.get("max_items") or 15)
    return [str(t).strip() for t in terms if str(t).strip()], max_items


def _load_feeds(root: Path) -> list[tuple[str, str]]:
    path = root / "social_digest" / "rss_sources.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    feeds = data.get("feeds") or []
    return [(f.get("name", "RSS"), f["url"]) for f in feeds if f.get("url")]


def collect(extensions_root: Path) -> list[NewsItem]:
    terms, max_items = _load_watchlist(extensions_root)
    if not terms:
        return []

    items: list[NewsItem] = []
    seen: set[str] = set()
    for source, url in _load_feeds(extensions_root):
        parsed = feedparser.parse(url)
        for entry in parsed.entries:
            title = (entry.get("title") or "").strip()
            link = (entry.get("link") or "").strip()
            if not title or not link:
                continue
            if not any(t in title for t in terms):
                continue
            key = link
            if key in seen:
                continue
            seen.add(key)
            items.append(NewsItem(title=title, link=link, source=source))
            if len(items) >= max_items:
                return items
    return items
