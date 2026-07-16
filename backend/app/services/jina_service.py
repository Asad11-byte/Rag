import httpx

from app.core.config import settings


class JinaService:

    def __init__(self):
        self.api_key = settings.JINA_API_KEY

        self.url = "https://api.jina.ai/v1/embeddings"

        self.model = "jina-embeddings-v3"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def embed_text(self, text: str) -> list[float]:

        payload = {
            "model": self.model,
            "input": [text],
        }

        response = httpx.post(
            self.url,
            headers=self.headers,
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        return data["data"][0]["embedding"]

    def embed_documents(
        self,
        documents: list[str],
    ) -> list[list[float]]:

        payload = {
            "model": self.model,
            "input": documents,
        }

        response = httpx.post(
            self.url,
            headers=self.headers,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return [
            item["embedding"]
            for item in data["data"]
        ]