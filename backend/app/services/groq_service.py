from groq import Groq

from app.core.config import settings
from app.prompts.prompt_builder import PromptBuilder


class GroqService:

    def __init__(self):
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = "llama-3.3-70b-versatile"

    def stream_answer(
        self,
        context: str,
        question: str,
    ):

        prompt = PromptBuilder.build(
            context=context,
            question=question,
        )

        stream = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI Research Assistant that answers questions using Retrieval-Augmented Generation (RAG).

Rules:

1. Answer ONLY from the retrieved document context.

2. The answer may require combining information from multiple retrieved chunks.

3. Do NOT require the exact wording from the user's question.

4. If the context contains enough information to answer, summarize it naturally.

5. Never invent facts that are not supported by the retrieved context.

6. If only partial information is available, answer with the available information and mention any limitations.

7. Only reply:

"I couldn't find that information in the indexed documents."

when the retrieved context contains no relevant information whatsoever.

8. Write clear, concise answers using Markdown bullet points whenever appropriate.
"""
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            temperature=0.1,

            max_tokens=1024,

            top_p=0.9,

            stream=True,
        )

        for chunk in stream:

            delta = chunk.choices[0].delta.content

            if delta:
                yield delta