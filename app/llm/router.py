from app.llm.groq import ask_groq
from app.llm.gemini import ask_gemini


def ask(task: str, complexity: str = "simple") -> str:
    """
    Route a task to the appropriate LLM.

    simple  -> Groq
    complex -> Gemini
    """

    if complexity == "complex":
        return ask_gemini(task)

    return ask_groq(task)
