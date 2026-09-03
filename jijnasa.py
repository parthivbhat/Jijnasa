import re
import sys

from app.news.pipeline import run_news_pipeline
from app.learning.learner import learn_and_save
from app.content.learning_x import generate_learning_x_content


def extract_learning_topic(text: str) -> str | None:
    """Extract a learning topic from natural language."""

    patterns = [
        r"^i\s+learnt\s+(?:about\s+)?(.+)$",
        r"^i\s+learned\s+(?:about\s+)?(.+)$",
        r"^today\s+i\s+learnt\s+(?:about\s+)?(.+)$",
        r"^today\s+i\s+learned\s+(?:about\s+)?(.+)$",
    ]

    text = text.strip()

    for pattern in patterns:
        match = re.match(pattern, text, re.IGNORECASE)

        if match:
            topic = match.group(1).strip()

            if topic:
                return topic

    return None


def run_learning(topic: str):
    """Run the complete learning pipeline."""

    print(f"🧠 Learning: {topic}", flush=True)

    path, knowledge = learn_and_save(topic)

    print()
    print("🗂️ Learning saved:")
    print(path)

    # Load the generated learning content.
    # The learner already created the Markdown file, so we
    # use the topic knowledge through the existing learning API.
    try:
        x_content = generate_learning_x_content(
            topic,
            knowledge,
        )

        print()
        print("=== 𝕏 TODAY I LEARNED — POST ===")
        print(x_content.get("post", ""))

        print()
        print("=== 𝕏 TODAY I LEARNED — THREAD ===")

        for i, post in enumerate(
            x_content.get("thread", []),
            1,
        ):
            print(f"{i}. {post}")

    except Exception as error:
        print()
        print(f"X content generation failed: {error}")


def interactive_mode():
    """Run Jijnasa as a natural-language CLI."""

    print("🕉️ JIJNASA")
    print("Type something like: I learnt Docker")
    print("Type 'news' for today's news.")
    print("Type 'exit' to quit.")
    print()

    while True:
        try:
            text = input("Jijnasa > ").strip()

        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not text:
            continue

        if text.lower() in {"exit", "quit"}:
            break

        if text.lower() == "news":
            print()
            print("=== JIJNASA NEWS ===", flush=True)

            result = run_news_pipeline()

            print()
            print("=== SUMMARY ===")
            print("Collected:", result["collected"])
            print("Candidates:", result["candidates"])
            print("Analyzed:", result["analyzed"])
            print("Important:", result["important"])
            print("Deep analyzed:", result["deep_analyzed"])
            print("Saved:", result["saved"])
            print()

            continue

        topic = extract_learning_topic(text)

        if topic:
            print()
            run_learning(topic)
            print()
            continue

        print(
            "I didn't understand that. "
            "Try: I learnt Docker"
        )


def main():
    # No arguments → interactive Jijnasa mode.
    if len(sys.argv) < 2:
        interactive_mode()
        return

    command = sys.argv[1].lower()

    # Keep existing news command.
    if command == "news":
        print("=== JIJNASA NEWS ===", flush=True)

        result = run_news_pipeline()

        print()
        print("=== SUMMARY ===")
        print("Collected:", result["collected"])
        print("Candidates:", result["candidates"])
        print("Analyzed:", result["analyzed"])
        print("Important:", result["important"])
        print("Deep analyzed:", result["deep_analyzed"])
        print("Saved:", result["saved"])

    # Keep existing learn command.
    elif command == "learn":
        if len(sys.argv) < 3:
            print('Usage: python jijnasa.py learn "topic"')
            return

        topic = " ".join(sys.argv[2:])
        run_learning(topic)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
