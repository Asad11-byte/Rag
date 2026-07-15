from pathlib import Path

import fitz  # PyMuPDF
from docx import Document


class DocumentLoader:
    @staticmethod
    def load_pdf(file_path: str) -> str:
        """Load text from a PDF."""
        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text

    @staticmethod
    def load_docx(file_path: str) -> str:
        """Load text from a DOCX."""
        document = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    @staticmethod
    def load_txt(file_path: str) -> str:
        """Load text from a TXT."""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def load_document(file_path: str) -> str:
        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return DocumentLoader.load_pdf(file_path)

        if extension == ".docx":
            return DocumentLoader.load_docx(file_path)

        if extension == ".txt":
            return DocumentLoader.load_txt(file_path)

        raise ValueError(f"Unsupported file type: {extension}")