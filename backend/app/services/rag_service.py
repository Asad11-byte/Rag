from app.services.voyage_service import VoyageService
from app.services.qdrant_service import QdrantService
from app.services.groq_service import GroqService


class RagService:

    def __init__(self):

        self.voyage = VoyageService()
        self.qdrant = QdrantService()
        self.groq = GroqService()

    def ask(
        self,
        question: str,
    ):

        embedding = self.voyage.embed_text(question)

        results = self.qdrant.search(
            embedding=embedding,
            limit=5,
        )

        # collect texts from results with a minimum score
        contexts = []
        for result in results:
            try:
                score = getattr(result, "score", None)
                text = result.payload.get("text") if getattr(result, "payload", None) else None
            except Exception:
                score = None
                text = None

            if score is not None and score >= 0.70 and text:
                contexts.append(text)

        context = "\n\n".join(contexts)

        return self.groq.stream_answer(
        context=context,
        question=question,
       )

        return {
            "answer": answer,
            "sources": contexts,
        }