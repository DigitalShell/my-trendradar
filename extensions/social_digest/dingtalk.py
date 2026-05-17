"""Send markdown text to DingTalk group robot webhook."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


def send_markdown(title: str, text: str) -> None:
    url = os.environ.get("DINGTALK_WEBHOOK_URL", "").strip()
    if not url:
        raise RuntimeError("DINGTALK_WEBHOOK_URL is not set")

    body = {
        "msgtype": "markdown",
        "markdown": {"title": title[:64], "text": text[:18000]},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode())
        if payload.get("errcode") != 0:
            raise RuntimeError(f"DingTalk error: {payload}")
