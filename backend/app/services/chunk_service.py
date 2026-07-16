from typing import List


class ChunkService:

    @staticmethod
    def chunk_text(
        pages: List[dict],
        chunk_size: int = 700,
        overlap: int = 120,
    ) -> List[dict]:
        """
        Split PDF pages into overlapping chunks while preserving
        page numbers and removing unnecessary whitespace.
        """

        chunks = []

        for page in pages:

            page_number = page["page"]

            text = page["text"].strip()

            if not text:
                continue

            start = 0

            while start < len(text):

                end = min(start + chunk_size, len(text))

                chunk = text[start:end].strip()

                if chunk:

                    chunks.append(
                        {
                            "text": chunk,
                            "page": page_number,
                        }
                    )

                if end == len(text):
                    break

                start += chunk_size - overlap

        return chunks