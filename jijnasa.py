import re
import sys

from app.news.pipeline import run_news_pipeline
from app.learning.learner import learn_and_save
from app.content.learning_x import generate_learning_x_content
from app.content.content_inbox import save_learning_content
from app.content.notifier import send_notification


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

        content_path = save_learning_content(
            topic,
            x_content.get("post", ""),
            x_content.get("thread", []),
        )

        send_notification(
            title="🧠 Jijnasa Learning Complete",
            message=(
                f"Topic: {topic}\n"
                f"📚 Learning note saved\n"
                f"✍️ X content generated\n"
                f"📥 Content Inbox saved\n\n"
                f"Open Obsidian to review it."
            ),
            tags="brain,notebook",
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


def run_learn_topic(topic):
    """Teach a topic and save the structured learning note to Obsidian."""
    print(f"📖 Learning topic: {topic}", flush=True)

    try:
        path, knowledge = learn_and_save(topic)

        print()
        print("=== 📚 LEARNING NOTE ===", flush=True)

        print(f"🧠 Concept: {knowledge.get('concept', '')}", flush=True)

        print()
        print("📖 Explanation:", flush=True)
        print(knowledge.get("explanation", ""), flush=True)

        print()
        print("🔑 Key Points:", flush=True)
        for point in knowledge.get("key_points", []):
            print(f"- {point}", flush=True)

        print()
        print("💻 Example:", flush=True)
        print(knowledge.get("example", ""), flush=True)

        print()
        print("⚠️ Common Mistakes:", flush=True)
        for mistake in knowledge.get("common_mistakes", []):
            print(f"- {mistake}", flush=True)

        print()
        print("🎯 Interview Questions:", flush=True)
        for item in knowledge.get("interview_questions", []):
            print(f"Q: {item.get('question', '')}", flush=True)
            print(f"A: {item.get('answer', '')}", flush=True)

        print()
        print("🔗 Related Topics:", flush=True)
        for related in knowledge.get("related_topics", []):
            print(f"- {related}", flush=True)

        print()
        print(f"🗂️ Saved to: {path}", flush=True)

    except Exception as error:
        print(f"❌ Learning failed: {error}", flush=True)


def interactive_mode():
    """Run Jijnasa as a natural-language CLI."""

    print("🕉️ JIJNASA")
    print()
    print("📰 Type 'news' → Today's technology news")
    print("📖 Type 'learn <topic>' → Learn and save a topic")
    print("🧠 Type 'I learnt <topic>' → Save learning + generate X content")
    print("🚪 Type 'exit' → Quit")
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
            x_content = result.get("x_content", {})
            print("🐦 X POST:")
            print(x_content.get("post", ""))
            print()
            print("🧵 X THREAD:")
            for i, post in enumerate(x_content.get("thread", []), 1):
                print(f"{i}. {post}")
            print()

            continue

        # --------------------------------------------------
        # FEATURE: Learn a new topic
        # Example:
        # learn dropout in deep learning
        # --------------------------------------------------

        learn_prefix = text.lower().startswith("learn ")

        if learn_prefix:
            topic = text[6:].strip()

            if topic:
                print()
                run_learn_topic(topic)
                print()
                continue

            print("Please provide a topic. Example: learn Docker")
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
