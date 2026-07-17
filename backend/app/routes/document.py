from pathlib import Path

from fastapi import APIRouter

from app.services.document_loader import DocumentLoader
from app.services.chunk_service import ChunkService

router = APIRouter(
    tags=["Documents"],
)

# --- DYNAMIC PATH RESOLUTION ---
# This climbs up from this file's location to find the main repository root
# and safely anchors the path inside 'backend/app/data/documents'
_current_file = Path(__file__).resolve()
_root_dir = _current_file
for _ in range(5):
    if (_root_dir / "backend").exists():
        break
    _root_dir = _root_dir.parent

DOCUMENT_FOLDER = _root_dir / "backend" / "app" / "data" / "documents"
# -------------------------------


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
    # Safely build the absolute path to your test file
    test_file_path = DOCUMENT_FOLDER / "AI-Agent-Security.pdf"

    if not test_file_path.exists():
        return {"error": f"File not found at resolved path: {test_file_path}"}

    # Convering the Path object to a string since most loaders expect a string path
    pages = DocumentLoader.load_document(str(test_file_path))

    chunks = ChunkService.chunk_text(pages)

    return {
        "pages": len(pages),
        "chunks": len(chunks),
        "first_chunk": chunks[0],
    }