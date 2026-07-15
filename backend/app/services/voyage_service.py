import voyageai

from app.core.config import settings


class VoyageService:
    def __init__(self):
        self.client = voyageai.Client(
            api_key=settings.VOYAGE_API_KEY
        )

        # Recommended embedding model
        self.model = "voyage-3-large"

    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        result = self.client.embed(
            texts=[text],
            model=self.model,
            input_type="document",
        )

        return result.embeddings[0]

    def embed_documents(
        self,
        documents: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple chunks.
        """

        result = self.client.embed(
            texts=documents,
            model=self.model,
            input_type="document",
        )

        return result.embeddings