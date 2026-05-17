# 个人助理扩展（my-trendradar）

与上游 TrendRadar 主流程并列，通过 **独立 GitHub Actions** 跑。

## 合规

- 仅个人学习与小规模自用；控制频率，遵守各平台服务条款。  
- 推送内容以 **摘要 + 链接** 为主，勿传播未核实原文。  
- 社媒评论全量爬取请在本机完成，CI 仅做摘要推送（见下）。

## 目录

| 路径 | 说明 |
|------|------|
| `watchlist.yaml.example` | 投资舆情关键词示例 → 复制为 `watchlist.yaml` |
| `social_digest/` | RSS 关键词命中 + LLM 摘要 + 钉钉（MVP） |
| `startup_digest/` | 创业 RSS 摘要 + 钉钉（可选 workflow） |

## 社媒评论（MVP → 完整）

**当前 MVP**：从 `rss_sources.yaml` 拉取资讯 RSS，按 `watchlist.yaml` 过滤标题，LLM 摘要后以 `[投资舆情]` 推送钉钉。  

**下一步（你要的评论）**：

1. 本机运行 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 按 watchlist 采微博/小红书评论  
2. 导出 `extensions/data/comments.json`  
3. 扩展 `social_digest/collect.py` 读取该文件再摘要（或 workflow 上传 artifact）  

## Secrets

与主项目相同：`DINGTALK_WEBHOOK_URL`、`AI_API_KEY` 等，见 maids 仓 `personal-assistant/config/SECRETS.md`。
