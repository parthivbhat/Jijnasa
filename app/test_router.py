from llm.router import ask

print("=== GROQ TEST ===")
print(ask(
    "Reply with exactly: Router selected Groq.",
    complexity="simple"
))

print("\n=== GEMINI TEST ===")
print(ask(
    "Reply with exactly: Router selected Gemini.",
    complexity="complex"
))
