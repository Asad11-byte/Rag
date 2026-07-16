from app.services.groq_service import GroqService
from app.services.jina_service import JinaService
from app.services.qdrant_service import QdrantService


class RagService:

    def __init__(self):
        self.jina = JinaService()
        self.qdrant = QdrantService()
        self.groq = GroqService()

    def retrieve(
        self,
        question: str,
        limit: int = 8,
        score_threshold: float = 0.60,
    ):
        """
        Retrieve the most relevant document chunks from Qdrant.
        """

        embedding = self.jina.embed_text(question)

        results = self.qdrant.search(
            embedding=embedding,
            limit=limit,
        )

        contexts = []

        citations = []

        seen_chunks = set()

        for result in results:

            score = getattr(result, "score", 0.0)

            payload = getattr(result, "payload", {}) or {}

            text = payload.get("text")

            page = payload.get("page")

            source = payload.get("source")

            if (
                not text
                or score < score_threshold
            ):
                continue

            # Skip duplicate chunks
            if text in seen_chunks:
                continue

            seen_chunks.add(text)

            contexts.append(
                f"""
Document: {source}
Page: {page}

{text}
"""
            )

            citations.append(
                {
                    "source": source,
                    "page": page,
                    "score": round(score, 3),
                }
            )

        context = "\n\n------------------------\n\n".join(contexts)

        print("\n========== RETRIEVED ==========")

        if citations:

            for citation in citations:

                print(
                    f"{citation['source']} | "
                    f"Page {citation['page']} | "
                    f"Score {citation['score']}"
                )

        else:

            print("No chunks found.")

        print("================================\n")

        return {
            "context": context,
            "citations": citations,
        }

    def stream(
        self,
        question: str,
    ):

        retrieval = self.retrieve(question)

        return self.groq.stream_answer(
            context=retrieval["context"],
            question=question,
        )

    def ask(
        self,
        question: str,
    ):

        retrieval = self.retrieve(question)

        return {
            "answer": self.groq.stream_answer(
                context=retrieval["context"],
                question=question,
            ),
            "citations": retrieval["citations"],
        }