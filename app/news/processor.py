from datetime import datetime
from urllib.parse import urlsplit, urlunsplit


def clean_text(text: str) -> str:
    """Normalize whitespace in text."""
    if not text:
        return ""

    return " ".join(text.split()).strip()


def normalize_url(url: str) -> str:
    """Normalize a URL so equivalent links are easier to compare."""
    if not url:
        return ""

    parts = urlsplit(url.strip())

    return urlunsplit((
        parts.scheme.lower(),
        parts.netloc.lower(),
        parts.path.rstrip("/"),
        "",
        "",
    ))


def process_article(article: dict) -> dict:
    """Convert a raw RSS article into a normalized Jijnasa article."""
    published = clean_text(article.get("published", ""))

    return {
        "source": clean_text(article.get("source", "")),
        "title": clean_text(article.get("title", "")),
        "url": normalize_url(article.get("url", "")),
        "published": published,
        "summary": clean_text(article.get("summary", "")),
    }


def process_articles(articles: list[dict]) -> list[dict]:
    """Process a collection of RSS articles."""
    return [process_article(article) for article in articles]
