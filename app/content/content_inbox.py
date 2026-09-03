from datetime import datetime
from pathlib import Path
import re


CONTENT_PATH = (
    Path.home()
    / "jijnasa"
    / "obsidian"
    / "Jijnasa"
    / "Content"
)


def save_learning_content(
    topic: str,
    post: str,
    thread: list,
) -> Path:
    """Save generated learning X content to the Obsidian Content Inbox."""

    CONTENT_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    date = datetime.now().strftime("%Y-%m-%d")

    safe_topic = re.sub(
        r'[<>:"/\\|?*]',
        "",
        topic,
    )

    safe_topic = " ".join(
        safe_topic.split()
    ).strip()

    if not safe_topic:
        safe_topic = "Untitled"

    filename = f"{date}-{safe_topic[:100]}.md"

    path = CONTENT_PATH / filename

    thread_content = "\n\n".join(
        f"{index}. {item}"
        for index, item in enumerate(thread, 1)
    )

    content = f"""# {topic}

**Created:** {date}

**Status:** Draft

---

## 𝕏 Post

{post}

---

## 🧵 X Thread

{thread_content}

---

## 📚 Source

This content was generated from the Jijnasa learning pipeline.

Topic: **{topic}**
"""

    path.write_text(
        content,
        encoding="utf-8",
    )

    print(
        f"📥 Content saved: {path}",
        flush=True,
    )

    return path
