import json
import re

from app.llm.gemini import ask_gemini
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


def build_prompt(article: dict) -> str:
    """Build the deep-analysis prompt."""

    title = article.get("title", "")
    summary = article.get("summary", "")
    source = article.get("source", "")
    url = article.get("url", "")
    category = article.get("category", "Other")
    event_type = article.get("event_type", "Other")
    relevance = article.get("relevance", 0)
    importance = article.get("importance", 0)

    return f"""
You are Jijnasa's deep technology intelligence layer.

Analyze this technology news article.

TITLE:
{title}

SOURCE:
{source}

URL:
{url}

CATEGORY:
{category}

EVENT TYPE:
{event_type}

RELEVANCE:
{relevance}

IMPORTANCE:
{importance}

ARTICLE SUMMARY:
{summary}

Return ONLY valid JSON:

{{
  "summary": "",
  "context": "",
  "why_it_matters": "",
  "industry_impact": "",
  "developer_impact": "",
  "key_takeaway": "",
  "x_angle": "",
  "confidence": 0
}}

Rules:
- Keep every field concise.
- Separate facts from interpretation.
- Do not invent facts.
- Use ONLY information supported by the supplied article.
- Do not make unsupported predictions.
- Do not introduce companies, products, people, numbers, or claims
  that are not supported by the supplied information.
- developer_impact can be empty when not relevant.
- confidence must be an integer from 0 to 100.
"""


def empty_analysis() -> dict:
    """Return a safe empty analysis."""

    return {
        "summary": "",
        "context": "",
        "why_it_matters": "",
        "industry_impact": "",
        "developer_impact": "",
        "key_takeaway": "",
        "x_angle": "",
        "confidence": 0,
    }


def deep_analyze_article(article: dict) -> dict:
    """
    Deep-analyze an article.

    Gemini is the primary model.
    Groq is used as a fallback if Gemini fails.
    """

    prompt = build_prompt(article)

    # ---------------------------------------------------------
    # PRIMARY: GEMINI
    # ---------------------------------------------------------

    try:
        print("  Trying Gemini...", flush=True)

        raw_response = ask_gemini(prompt)
        result = parse_json_response(raw_response)

        if result:
            print("  Gemini succeeded.", flush=True)

            return {
                **article,
                "deep_analysis": result,
                "deep_model": "Gemini",
            }

        print(
            "  Gemini returned invalid JSON. "
            "Trying Groq fallback...",
            flush=True,
        )

    except Exception as error:
        print(
            f"  Gemini failed: {error}",
            flush=True,
        )
        print(
            "  Trying Groq fallback...",
            flush=True,
        )

    # ---------------------------------------------------------
    # FALLBACK: GROQ
    # ---------------------------------------------------------

    try:
        raw_response = ask_groq(prompt)
        result = parse_json_response(raw_response)

        if result:
            print("  Groq fallback succeeded.", flush=True)

            return {
                **article,
                "deep_analysis": result,
                "deep_model": "Groq Fallback",
            }

        print(
            "  Groq fallback returned invalid JSON.",
            flush=True,
        )

    except Exception as error:
        print(
            f"  Groq fallback failed: {error}",
            flush=True,
        )

    # ---------------------------------------------------------
    # BOTH FAILED
    # ---------------------------------------------------------

    print(
        "  Both Gemini and Groq failed.",
        flush=True,
    )

    return {
        **article,
        "deep_analysis": empty_analysis(),
        "deep_model": "Failed",
    }


def deep_analyze_articles(articles: list[dict]) -> list[dict]:
    """Deep-analyze multiple articles."""

    results = []
    total = len(articles)

    for i, article in enumerate(articles, 1):

        print(
            f"Deep analyzing {i}/{total}: "
            f"{article.get('title', '')}",
            flush=True,
        )

        result = deep_analyze_article(article)

        results.append(result)

        print(
            f"Finished {i}/{total} "
            f"[{result.get('deep_model', 'Unknown')}]",
            flush=True,
        )

    return results
