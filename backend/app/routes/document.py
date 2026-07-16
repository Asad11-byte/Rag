from pathlib import Path

from fastapi import APIRouter

from app.services.document_loader import DocumentLoader
from app.services.chunk_service import ChunkService

router = APIRouter(
    tags=["Documents"],
)

DOCUMENT_FOLDER = Path("app/data/documents")


@router.get("/documents")
async def list_documents():
    """
    Return all uploaded PDF documents.
    """

    pdfs = []

    if DOCUMENT_FOLDER.exists():

        for file in DOCUMENT_FOLDER.glob("*.pdf"):

            pdfs.append(
                {
                    "name": file.name,
                    "url": f"/documents/{file.name}",
                }
            )

    return pdfs


@router.get("/document/test")
async def test_document():
    """
    Test document loading and chunking.
    """

    pages = DocumentLoader.load_document(
        "app/data/documents/AI-Agent-Security.pdf"
    )

    chunks = ChunkService.chunk_text(pages)

    return {
        "pages": len(pages),
        "chunks": len(chunks),
        "first_chunk": chunks[0],
    }