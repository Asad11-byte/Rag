from fastapi import APIRouter

from app.services.document_loader import DocumentLoader
from app.services.chunk_service import ChunkService
from app.services.voyage_service import VoyageService

router = APIRouter(
    prefix="/document",
    tags=["Document"],
)


@router.get("/test")
async def test_document():

    text = DocumentLoader.load_document(
        "app/data/documents/AI-Agent-Security.pdf"
    )

    chunks = ChunkService.chunk_text(text)

    voyage = VoyageService()

    embedding = voyage.embed_text(chunks[0])

    return {
        "characters": len(text),
        "chunks": len(chunks),
        "embedding_dimension": len(embedding),
        "embedding_preview": embedding[:5],
    }