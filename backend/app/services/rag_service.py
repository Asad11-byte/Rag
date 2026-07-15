from app.services.voyage_service import VoyageService
from app.services.qdrant_service import QdrantService
from app.services.groq_service import GroqService


class RagService:

    def __init__(self):
        self.voyage = VoyageService()
        self.qdrant = QdrantService()
        self.groq = GroqService()

    def stream(
        self,
        question: str,
    ):
        # Create embedding for the user's question
        embedding = self.voyage.embed_text(question)

        # Search Qdrant
        results = self.qdrant.search(
            embedding=embedding,
            limit=5,
        )

        # Build context from the retrieved chunks
        contexts = []

        for result in results:

            score = getattr(result, "score", 0)

            payload = getattr(result, "payload", {})

            text = payload.get("text")

            if score >= 0.70 and text:
                contexts.append(text)

        context = "\n\n".join(contexts)

        # Stream answer from Groq
        return self.groq.stream_answer(
            context=context,
            question=question,
        )