"""Summarize news items via LiteLLM or plain bullet list."""

from __future__ import annotations

import os

from social_digest.collect_rss import NewsItem


def summarize(items: list[NewsItem]) -> str:
    if not items:
        return "今日 watchlist 相关 RSS 无新标题命中。"

    api_key = os.environ.get("AI_API_KEY", "").strip()
    model = os.environ.get("AI_MODEL", "deepseek/deepseek-chat").strip()
    if not api_key:
        lines = ["**命中条目（未配置 AI_API_KEY，仅列表）**\n"]
        for i, it in enumerate(items, 1):
            lines.append(f"{i}. [{it.title}]({it.link}) — {it.source}")
        return "\n".join(lines)

    from litellm import completion

    bullet = "\n".join(f"- {it.title} | {it.source} | {it.link}" for it in items)
    prompt = (
        "你是投资资讯助理。根据下列新闻标题（含链接），用中文输出：\n"
        "1) 3～5 条要点摘要\n"
        "2) 一句风险/情绪判断\n"
        "3) 保留关键链接（markdown）\n"
        "不要编造正文没有的信息。\n\n"
        f"{bullet}"
    )
    resp = completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        api_key=api_key,
        api_base=os.environ.get("AI_API_BASE") or None,
        timeout=120,
    )
    return (resp.choices[0].message.content or "").strip()
