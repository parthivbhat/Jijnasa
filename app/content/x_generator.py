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


def generate_x_content(article: dict) -> dict:
    """Generate an X post and thread from Jijnasa intelligence."""

    title = article.get("title", "")
    source = article.get("source", "")
    summary = article.get("summary", "")
    why_it_matters = article.get("why_it_matters", "")
    industry_impact = article.get("industry_impact", "")
    key_takeaway = article.get("key_takeaway", "")
    x_angle = article.get("x_angle", "")

    prompt = f"""
You are Jijnasa's X content writer.

Create high-quality technology content for X (Twitter) based ONLY
on the supplied intelligence.

TITLE:
{title}

SOURCE:
{source}

SUMMARY:
{summary}

WHY IT MATTERS:
{why_it_matters}

INDUSTRY IMPACT:
{industry_impact}

KEY TAKEAWAY:
{key_takeaway}

X ANGLE:
{x_angle}

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

- post must be concise and engaging.
- Keep post under 280 characters.
- thread must contain 3 to 5 posts.
- Each thread post should be useful on its own.
- Start the thread with a strong hook.
- Explain what happened and why it matters.
- Prefer facts over hype.
- Do not invent facts.
- Do not make unsupported claims.
- Do not use excessive hashtags.
- Use at most 2 relevant hashtags.
- Make the writing natural, like a technology builder/intelligence analyst.
"""

    try:
        raw_response = ask_groq(prompt)
        result = parse_json_response(raw_response)

        if result:
            return {
                **article,
                "x_content": result,
            }

    except Exception as error:
        print(f"X generation failed: {error}", flush=True)

    return {
        **article,
        "x_content": {
            "post": "",
            "thread": [],
        },
    }


def generate_x_contents(articles: list[dict]) -> list[dict]:
    """Generate X content for multiple articles."""

    results = []
    total = len(articles)

    for i, article in enumerate(articles, 1):
        print(
            f"Generating X content {i}/{total}: "
            f"{article.get('title', '')}",
            flush=True,
        )

        result = generate_x_content(article)
        results.append(result)

        print(
            f"Finished X content {i}/{total}",
            flush=True,
        )

    return results
