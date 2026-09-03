import re


def normalize_title(title: str) -> str:
    """Normalize a title for duplicate comparison."""
    title = title.lower()
    title = re.sub(r"[^a-z0-9\s]", " ", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title


def deduplicate_articles(articles: list[dict]) -> list[dict]:
    """
    Remove duplicate articles using normalized URL and title.

    Keeps the first occurrence of each article.
    """
    seen_urls = set()
    seen_titles = set()
    unique_articles = []

    for article in articles:
        url = article.get("url", "").strip()
        title = normalize_title(article.get("title", ""))

        if url and url in seen_urls:
            continue

        if title and title in seen_titles:
            continue

        if url:
            seen_urls.add(url)

        if title:
            seen_titles.add(title)

        unique_articles.append(article)

    return unique_articles
