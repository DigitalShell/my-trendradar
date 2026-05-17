#!/usr/bin/env python3
"""Startup digest: Product Hunt RSS → LLM → DingTalk."""

from __future__ import annotations

import sys
from pathlib import Path

import feedparser

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from social_digest.dingtalk import send_markdown


FEED_URL = "https://www.producthunt.com/feed"


def main() -> None:
    parsed = feedparser.parse(FEED_URL)
    entries = parsed.entries[:12]
    if not entries:
        send_markdown("[创业]", "## [创业] 今日无 Product Hunt 条目")
        return

    lines = [f"- [{e.title}]({e.link})" for e in entries if e.get("title") and e.get("link")]
    body = "\n".join(lines)

    api_key = __import__("os").environ.get("AI_API_KEY", "").strip()
    if api_key:
        from litellm import completion

        model = __import__("os").environ.get("AI_MODEL", "deepseek/deepseek-chat")
        resp = completion(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "根据下列 Product Hunt 今日产品列表，用中文写一段创业机会摘要"
                        "（趋势、可借鉴方向、2～3 个值得点开的产品），markdown，保留链接：\n"
                        + body
                    ),
                }
            ],
            api_key=api_key,
            timeout=120,
        )
        body = (resp.choices[0].message.content or body).strip()

    text = f"## [创业] 每日摘要\n\n{body}"
    send_markdown("[创业]", text)
    print("Sent startup digest")


if __name__ == "__main__":
    main()
