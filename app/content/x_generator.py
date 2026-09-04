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


def generate_news_x_content(
    articles: list[dict],
    collected: int = 0,
    candidates: int = 0,
    analyzed: int = 0,
) -> dict:
    """Generate one X post and a thread from the day's important news."""

    news_blocks = []

    for i, article in enumerate(articles, 1):
        deep = article.get("deep_analysis", {})

        news_blocks.append(
            f"""
STORY {i}
TITLE: {article.get("title", "")}
SOURCE: {article.get("source", "")}
SUMMARY: {article.get("summary", "")}
WHY IT MATTERS: {article.get("why_it_matters", "")}
INDUSTRY IMPACT: {article.get("industry_impact", "")}
KEY TAKEAWAY: {article.get("key_takeaway", "")}
X ANGLE: {article.get("x_angle", "")}
DEEP ANALYSIS: {deep}
"""
        )

    prompt = f"""
You are Jijnasa's technology news X content writer.

Create ONE main X post and ONE concise thread from the important
technology news analyzed today.

PIPELINE STATS:
Collected: {collected}
Shortlisted: {candidates}
Groq analyzed: {analyzed}
Important stories: {len(articles)}

NEWS:
{"".join(news_blocks)}

Return ONLY valid JSON:

{{
  "post": "",
  "thread": [
    "",
    "",
    ""
  ]
}}

MAIN POST RULES:
- Tell the reader what the actual news is.
- Mention the most important 2-3 stories.
- Use plain language.
- Include useful context, not just headlines.
- Mention Jijnasa's pipeline stats naturally if they fit.
- Keep it under 280 characters.
- Use emojis sparingly.
- Use at most 2 hashtags.
- Do not invent facts.

THREAD RULES:
- Create one thread post for each important story.
- Number posts dynamically, for example 1/3, 2/3, 3/3.
- Each post should explain what happened and why it matters.
- Keep each post concise.
- Use plain language.
- Start each story with a useful hook.
- Do not invent facts.
- Do not repeat the main post unnecessarily.
- No excessive hashtags.

IMPORTANT:
- Prefer factual reporting over hype.
- Do not claim certainty where the source does not provide it.
- Do not invent sources, statistics, quotes, or events.
"""


    try:
        print("Generating news X content...", flush=True)

        response = ask_groq(prompt)
        result = parse_json_response(response)

        if result:
            print("News X content generated.", flush=True)
            return result

        print("Could not parse news X content.", flush=True)

    except Exception as error:
        print(
            f"News X generation failed: {error}",
            flush=True,
        )

    return {
        "post": "",
        "thread": [],
    }
