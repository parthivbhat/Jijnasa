IMPORTANT_KEYWORDS = {
    "ai": 10,
    "artificial intelligence": 10,
    "llm": 10,
    "openai": 10,
    "google": 8,
    "microsoft": 8,
    "nvidia": 8,
    "anthropic": 10,
    "meta": 8,
    "aws": 8,
    "azure": 8,
    "cybersecurity": 10,
    "hack": 9,
    "breach": 10,
    "vulnerability": 10,
    "acquisition": 9,
    "acquire": 9,
    "merger": 9,
    "funding": 7,
    "layoff": 8,
    "layoffs": 8,
    "ceo": 7,
    "cto": 7,
    "gpu": 7,
    "chip": 7,
    "kubernetes": 6,
    "docker": 6,
    "github": 6,
    "open source": 7,
    "regulation": 8,
    "antitrust": 8,
    "ipo": 8,
}


def score_article(article: dict) -> int:
    """Calculate an importance score for an article."""

    title = article.get("title", "").lower()
    summary = article.get("summary", "").lower()

    text = f"{title} {summary}"

    score = 0

    # Keywords appearing anywhere in the article
    for keyword, points in IMPORTANT_KEYWORDS.items():
        if keyword in text:
            score += points

    # Give extra weight to keywords in the title
    for keyword, points in IMPORTANT_KEYWORDS.items():
        if keyword in title:
            score += points

    return score


def rank_articles(articles: list[dict]) -> list[dict]:
    """Score and rank articles from most important to least important."""

    ranked = []

    for article in articles:
        item = article.copy()

        item["importance_score"] = score_article(item)

        if item["importance_score"] >= 15:
            item["importance"] = "critical"
        elif item["importance_score"] >= 8:
            item["importance"] = "high"
        elif item["importance_score"] >= 4:
            item["importance"] = "medium"
        else:
            item["importance"] = "low"

        ranked.append(item)

    ranked.sort(
        key=lambda article: article["importance_score"],
        reverse=True,
    )

    return ranked
