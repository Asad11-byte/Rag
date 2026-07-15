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
                    "content": "Answer only from the provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            stream=True,
        )

        for chunk in stream:

            delta = chunk.choices[0].delta.content

            if delta:
                yield delta