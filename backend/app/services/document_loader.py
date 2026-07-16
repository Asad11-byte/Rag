import fitz  # PyMuPDF


class DocumentLoader:
    @staticmethod
    def load_document(file_path: str) -> list[dict]:
        """
        Load a PDF and return text page-by-page.

        Returns:
        [
            {
                "page": 1,
                "text": "..."
            },
            ...
        ]
        """

        document = fitz.open(file_path)

        pages = []

        for page_number, page in enumerate(document, start=1):

            text = page.get_text("text").strip()

            # Skip empty pages
            if not text:
                continue

            pages.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

        document.close()

        return pages