import json
import re

from app.llm.groq import ask_groq


def parse_json_response(response: str) -> dict:
    """Extract JSON from an LLM response."""

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


def generate_learning_x_content(
    topic: str,
    knowledge: dict,
) -> dict:
    """Generate personal 'Today I Learned' X content."""

    concept = knowledge.get("concept", "")
    explanation = knowledge.get("explanation", "")
    key_points = knowledge.get("key_points", [])
    example = knowledge.get("example", "")

    prompt = f"""
You are Jijnasa's personal learning-to-X writer.

The user learned this topic TODAY:

TOPIC:
{topic}

CONCEPT:
{concept}

EXPLANATION:
{explanation}

KEY POINTS:
{key_points}

EXAMPLE:
{example}

Create personal X content describing what the user learned today.

Return ONLY valid JSON:

{{
  "post": "",
  "thread": [
    "",
    "",
    ""
  ]
}}

Rules:
- Write in first person.
- Start naturally with "Today I learned..." or a natural variation.
- Make it sound like a real learner sharing a useful discovery.
- Explain what the concept is and what the user understood.
- Do not sound like a textbook.
- Do not claim the user built or used something unless supplied.
- Do not invent facts.
- Post must be under 280 characters.
- Thread should contain 3 to 4 posts.
- Keep the thread educational and concise.
- Avoid excessive hashtags.
- Use at most 2 relevant hashtags.
"""

    try:
        print("Generating learning X content...", flush=True)

        response = ask_groq(prompt)

        result = parse_json_response(response)

        if result:
            print("Learning X content generated.", flush=True)
            return result

        print("Could not parse learning X content.", flush=True)

    except Exception as error:
        print(
            f"Learning X generation failed: {error}",
            flush=True,
        )

    return {
        "post": "",
        "thread": [],
    }
