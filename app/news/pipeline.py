from app.news.rss_collector import collect_news
from app.news.processor import process_articles
from app.news.deduplicator import deduplicate_articles
from app.news.analyzer import analyze_article
from app.news.deep_analyzer import deep_analyze_articles
from app.content.x_generator import generate_news_x_content


# Safety limits while developing.
MAX_GROQ_ARTICLES = 5
MIN_RELEVANCE = 50
MIN_IMPORTANCE = 50


def collect_and_prepare() -> list[dict]:
    """Collect, clean and deduplicate RSS articles."""

    articles = collect_news()
    processed = process_articles(articles)
    unique = deduplicate_articles(processed)

    return unique


def select_candidates(articles: list[dict]) -> list[dict]:
    """Select potentially useful articles before Groq."""

    candidates = []

    skip_terms = [
        "conference",
        "event",
        "stage",
        "podcast",
        "interview",
        "webinar",
        "disrupt",
    ]

    for article in articles:
        title = article.get("title", "").lower()
        summary = article.get("summary", "").lower()

        text = f"{title} {summary}"

        if any(term in text for term in skip_terms):
            continue

        candidates.append(article)

        if len(candidates) >= MAX_GROQ_ARTICLES:
            break

    return candidates


def analyze_articles(articles: list[dict]) -> list[dict]:
    """Run Groq first-pass intelligence."""

    analyzed = []

    for article in articles:
        try:
            result = analyze_article(article)
            analyzed.append(result)

        except Exception as error:
            print(
                f"Skipping Groq analysis for: "
                f"{article.get('title', '')}"
            )
            print(f"Reason: {error}")

    return analyzed


def filter_important(articles: list[dict]) -> list[dict]:
    """Keep articles worth sending to Gemini."""

    return [
        article
        for article in articles
        if (
            article.get("relevance", 0) >= MIN_RELEVANCE
            and article.get("importance", 0) >= MIN_IMPORTANCE
        )
    ]


def run_news_pipeline() -> dict:
    """Run the complete Jijnasa news intelligence pipeline."""

    print("Collecting news...", flush=True)

    unique_articles = collect_and_prepare()

    print(
        f"Collected: {len(unique_articles)}",
        flush=True,
    )

    candidates = select_candidates(unique_articles)

    print(
        f"Candidates: {len(candidates)}",
        flush=True,
    )

    analyzed_articles = analyze_articles(candidates)

    print(
        f"Groq analyzed: {len(analyzed_articles)}",
        flush=True,
    )

    important_articles = filter_important(analyzed_articles)

    print(
        f"Important: {len(important_articles)}",
        flush=True,
    )

    print("Starting Gemini deep analysis...", flush=True)

    deep_articles = deep_analyze_articles(
        important_articles
    )

    print(
        f"Deep analyzed: {len(deep_articles)}",
        flush=True,
    )

    print("Generating X content...", flush=True)
    x_content = generate_news_x_content(
        deep_articles,
        collected=len(unique_articles),
        candidates=len(candidates),
        analyzed=len(analyzed_articles),
    )
    print("X content generated.", flush=True)

    return {
        "collected": len(unique_articles),
        "candidates": len(candidates),
        "analyzed": len(analyzed_articles),
        "important": len(important_articles),
        "deep_analyzed": len(deep_articles),
        "x_content": x_content,
        "articles": deep_articles,
    }
