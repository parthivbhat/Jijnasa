import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def find_tech_news() -> str:
    prompt = """
You are Jijnasa, a technology intelligence agent.

Find important recent technology news.

Cover:
- Artificial Intelligence
- LLMs and AI companies
- Cloud computing
- Software
- Cybersecurity
- Big Tech
- Startups
- Funding and acquisitions
- Tech layoffs
- CEO and leadership changes
- Developer tools
- Hardware
- Emerging technologies

Prioritize genuinely important developments.

For each important story provide:
1. Headline
2. What happened
3. Why it matters
4. Company/technology involved
5. Source

Avoid rumors and duplicate stories.
Prefer reliable and recent sources.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        ),
    )

    return response.text
