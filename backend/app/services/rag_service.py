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

        Returns:
        {
            "context": str,
            "citations": [...],
            "retrieved": [...]
        }
        """

        # Generate embedding for the user query
        embedding = self.jina.embed_text(question)

        # Search Qdrant
        results = self.qdrant.search(
            embedding=embedding,
            limit=limit,
        )

        contexts = []

        citations = []

        retrieved = []

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

            item = {
                "rank": len(citations) + 1,
                "source": source,
                "page": page,
                "score": round(score, 3),
            }

            citations.append(item)

            retrieved.append(item)

        context = "\n\n------------------------\n\n".join(contexts)

        print("\n========== RETRIEVED ==========")

        if retrieved:

            for item in retrieved:

                print(
                    f"[{item['rank']}] "
                    f"{item['source']} | "
                    f"Page {item['page']} | "
                    f"Score {item['score']}"
                )

        else:

            print("No relevant chunks found.")

        print("================================\n")

        return {
            "context": context,
            "citations": citations,
            "retrieved": retrieved,
        }

    def stream(
        self,
        question: str,
    ):
        """
        Stream the LLM response.
        """

        retrieval = self.retrieve(question)

        return self.groq.stream_answer(
            context=retrieval["context"],
            question=question,
        )

    def ask(
        self,
        question: str,
    ):
        """
        Non-streaming response.
        """

        retrieval = self.retrieve(question)

        return {
            "answer": self.groq.stream_answer(
                context=retrieval["context"],
                question=question,
            ),
            "citations": retrieval["citations"],
        }