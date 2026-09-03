from llm.groq import ask_groq

response = ask_groq(
    "You are Jijnasa, a technology intelligence agent. "
    "Reply with exactly: Jijnasa Groq is online."
)

print(response)
