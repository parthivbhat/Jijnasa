import json
import re
from pathlib import Path

from app.llm.groq import ask_groq


LEARNING_PATH = (
    Path.home()
    / "jijnasa"
    / "obsidian"
    / "Jijnasa"
    / "Learning"
)


def parse_json_response(response: str) -> dict:
    response = response.strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass

    response = re.sub(
        r"^```json\s*",
        "",
        response,
        flags=re.IGNORECASE,
    )
    response = re.sub(r"^```\s*", "", response)
    response = re.sub(r"\s*```$", "", response)

    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", response, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return {}


def learn(topic: str) -> dict:
    """Convert a learning topic into structured knowledge."""

    prompt = f"""
You are Jijnasa's learning intelligence layer.

Teach the following topic clearly for a technical learner.

TOPIC:
{topic}

Return ONLY valid JSON:

{{
  "concept": "",
  "explanation": "",
  "key_points": [],
  "example": "",
  "common_mistakes": [],
  "interview_questions": [
    {{
      "question": "",
      "answer": ""
    }}
  ],
  "related_topics": []
}}

Rules:
- Explain in simple technical language.
- Start from fundamentals.
- Do not invent facts.
- Use accurate examples.
- Keep it concise but useful.
- Include 3 to 5 key points.
- Include 2 to 3 interview questions.
- Include 2 to 4 related topics.
"""

    try:
        print("Calling Groq for learning...", flush=True)

        response = ask_groq(prompt)

        print("Groq responded.", flush=True)

        result = parse_json_response(response)

        if result:
            print("Learning JSON parsed successfully.", flush=True)
            return result

        print("Learning JSON parsing failed.", flush=True)
        print("Raw response:", response, flush=True)

    except Exception as error:
        print(f"Learning Groq error: {error}", flush=True)

    return {}

def save_learning(topic: str, knowledge: dict) -> Path:
    """Save structured learning to Obsidian."""

    LEARNING_PATH.mkdir(parents=True, exist_ok=True)

    safe_topic = re.sub(r'[<>:"/\\|?*]', "", topic)
    safe_topic = " ".join(safe_topic.split()).strip()

    if not safe_topic:
        safe_topic = "Untitled"

    path = LEARNING_PATH / f"{safe_topic[:150]}.md"

    key_points = "\n".join(
        f"- {point}"
        for point in knowledge.get("key_points", [])
    )

    mistakes = "\n".join(
        f"- {item}"
        for item in knowledge.get("common_mistakes", [])
    )

    questions = "\n".join(
        f"### {item.get('question', '')}\n"
        f"{item.get('answer', '')}\n"
        for item in knowledge.get("interview_questions", [])
    )

    related = ", ".join(
        knowledge.get("related_topics", [])
    )

    content = f"""# {topic}

## 🧠 Concept

{knowledge.get("concept", "")}

## 📖 Explanation

{knowledge.get("explanation", "")}

## 🔑 Key Points

{key_points}

## 💻 Example

{knowledge.get("example", "")}

## ⚠️ Common Mistakes

{mistakes}

## 🎯 Interview Questions

{questions}

## 🔗 Related Topics

{related}
"""

    path.write_text(content, encoding="utf-8")

    return path


def learn_and_save(topic: str) -> tuple[Path, dict]:
    """Learn a topic, save it to Obsidian, and return both."""

    print(f"Learning: {topic}", flush=True)

    knowledge = learn(topic)

    if not knowledge:
        raise RuntimeError("Could not generate learning content.")

    path = save_learning(topic, knowledge)

    print(f"Saved learning: {path}", flush=True)

    return path, knowledge
