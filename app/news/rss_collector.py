import json
from pathlib import Path

import feedparser


CONFIG_PATH = (
    Path(__file__).resolve().parents[2]
    / "config"
    / "sources.json"
)


def load_news_sources() -> dict:
    """Load active news RSS sources from configuration."""

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = json.load(file)

    return config.get("news", {})


def collect_news():
    """Collect articles from all active RSS sources."""

    articles = []
    news_sources = load_news_sources()

    for source, url in news_sources.items():
        print(f"Collecting from {source}...", flush=True)

        try:
            feed = feedparser.parse(url)

            for entry in feed.entries:
                articles.append({
                    "source": source,
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", ""),
                })

        except Exception as error:
            print(f"Source failed: {source} | {error}", flush=True)

    return articles
