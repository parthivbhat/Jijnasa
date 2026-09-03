import json
import re

from app.llm.groq import ask_groq


VALID_CATEGORIES = {
    "AI",
    "Cloud",
    "Cybersecurity",
    "Developer",
    "Hardware",
    "Startup",
    "Business",
    "Leadership",
    "Regulation",
    "Research",
    "Other",
}

VALID_EVENT_TYPES = {
    "Model Release",
    "Product Launch",
    "Acquisition",
    "Funding",
    "Layoffs",
    "Security Incident",
    "Regulation",
    "Leadership Change",
    "Research",
    "Partnership",
    "Other",
}


def parse_json_response(response: str) -> dict:
    """Extract a JSON object from a model response."""

    if not response:
        return {}

    response = response.strip()

    # Direct JSON
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass

    # Remove markdown code fences
    cleaned = re.sub(
        r"^```json\s*",
        "",
        response,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned.strip())
    except json.JSONDecodeError:
        pass

    # Find JSON object inside additional text
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return {}


def safe_score(value, default=0):
    """Convert a model score into an integer between 0 and 100."""

    try:
        value = int(value)
    except (TypeError, ValueError):
        return default

    return max(0, min(100, value))


def analyze_article(article: dict) -> dict:
    """Use Groq for first-pass news intelligence."""

    title = article.get("title", "")
    summary = article.get("summary", "")
    source = article.get("source", "")
    url = article.get("url", "")

    prompt = f"""
You are the first-pass intelligence layer of Jijnasa.

Analyze the technology news article below.

TITLE:
{title}

SOURCE:
{source}

URL:
{url}

SUMMARY:
{summary}

Return ONLY a JSON object.

Required structure:

{{
  "category": "AI | Cloud | Cybersecurity | Developer | Hardware | Startup | Business | Leadership | Regulation | Research | Other",
  "event_type": "Model Release | Product Launch | Acquisition | Funding | Layoffs | Security Incident | Regulation | Leadership Change | Research | Partnership | Other",
  "relevance": 0,
  "importance": 0,
  "reason": ""
}}

Rules:

- category MUST be exactly one of the provided categories.
- event_type MUST be exactly one of the provided event types.
- relevance must be an integer from 0 to 100.
- importance must be an integer from 0 to 100.
- relevance = usefulness to Jijnasa as a technology intelligence agent.
- importance = significance to the technology industry.
- Do not inflate scores because a famous company is mentioned.
- Promotional events, conferences, interviews and minor announcements
  should normally receive lower scores.
- Major AI releases, major acquisitions, major security incidents,
  major regulations and industry-changing events should receive higher scores.
- Base the judgment ONLY on the supplied information.
- Do not invent facts.
- Keep the reason concise.
"""

    raw_response = ask_groq(prompt)
    result = parse_json_response(raw_response)

    if not result:
        return {
            **article,
            "category": "Other",
            "event_type": "Other",
            "relevance": 0,
            "importance": 0,
            "reason": "Could not parse Groq response.",
        }

    category = result.get("category", "Other")
    event_type = result.get("event_type", "Other")

    if category not in VALID_CATEGORIES:
        category = "Other"

    if event_type not in VALID_EVENT_TYPES:
        event_type = "Other"

    relevance = safe_score(result.get("relevance"))
    importance = safe_score(result.get("importance"))

    return {
        **article,
        "category": category,
        "event_type": event_type,
        "relevance": relevance,
        "importance": importance,
        "reason": str(result.get("reason", "")).strip(),
    }
