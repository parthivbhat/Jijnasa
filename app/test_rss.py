from news.rss_collector import collect_news


articles = collect_news()

print(f"Collected {len(articles)} articles\n")

for i, article in enumerate(articles[:10], 1):
    print(f"{i}. {article['title']}")
    print(f"   Source: {article['source']}")
    print(f"   URL: {article['url']}")
    print()
