#!/usr/bin/env python3
"""Social digest MVP: RSS + watchlist → LLM → DingTalk."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from social_digest.collect_rss import collect
from social_digest.dingtalk import send_markdown
from social_digest.summarize import summarize


def main() -> None:
    items = collect(ROOT)
    body = summarize(items)
    text = f"## [投资舆情] RSS 监测摘要\n\n{body}\n\n> MVP：标题级 RSS；社媒评论见 extensions/README.md"
    send_markdown("[投资舆情]", text)
    print(f"Sent digest with {len(items)} items")


if __name__ == "__main__":
    main()
