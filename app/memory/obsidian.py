from pathlib import Path
from datetime import datetime


VAULT_PATH = Path.home() / "jijnasa" / "obsidian" / "Jijnasa"
NEWS_PATH = VAULT_PATH / "News"


def safe_name(name: str) -> str:
    """Convert text into a safe Markdown filename."""
    invalid = '<>:"/\\|?*'
    for char in invalid:
        name = name.replace(char, "")
    return " ".join(name.split()).strip()[:150]


def category_folder(category: str) -> Path:
    """Return the Obsidian folder for a news category."""
    folder = NEWS_PATH / safe_name(category or "Other")
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def save_news_article(article: dict) -> Path:
    """Save a final analyzed news article to Obsidian."""

    category = article.get("category", "Other")
    title = article.get("title", "Untitled")

    folder = category_folder(category)

    filename = safe_name(title)
    if not filename:
        filename = "Untitled"

    path = folder / f"{filename}.md"

    saved_at = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    content = f"""# {title}

## 📝 Summary

{article.get("summary", "")}

## 🎯 Why It Matters

{article.get("why_it_matters", "")}

## 🏭 Industry Impact

{article.get("industry_impact", "")}

## 👨‍💻 Developer Impact

{article.get("developer_impact", "")}

## 💡 Key Takeaway

{article.get("key_takeaway", "")}

## 𝕏 X Angle

{article.get("x_angle", "")}

## 📊 Intelligence

- **Category:** {category}
- **Event:** {article.get("event_type", "Other")}
- **Relevance:** {article.get("relevance", 0)}
- **Importance:** {article.get("importance", 0)}
- **Confidence:** {article.get("confidence", 0)}

## 🌐 Source

- **Publication:** {article.get("source", "")}
- **URL:** {article.get("url", "")}
- **Published:** {article.get("published", "")}

## 🕒 Jijnasa

Saved: {saved_at}
"""

    path.write_text(content, encoding="utf-8")

    return path
