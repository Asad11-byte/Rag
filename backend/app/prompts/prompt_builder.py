class PromptBuilder:

    @staticmethod
    def build(context: str, question: str) -> str:
        return f"""
You are an AI Agent Security expert.

Instructions:

- Answer ONLY using the provided context.
- Never invent information.
- If the answer is not in the context, reply:
  "I couldn't find that information in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""