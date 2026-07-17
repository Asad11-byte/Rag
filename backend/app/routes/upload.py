import os
from pathlib import Path
import shutil

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.services.index_service import IndexService

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

# --- DYNAMIC VERCEL-SAFE PATH RESOLUTION ---
if os.environ.get("VERCEL"):
    # Vercel serverless functions can only write files into the /tmp directory
    UPLOAD_FOLDER = Path("/tmp/documents")
else:
    # Local setup: dynamically climbs directories to anchor to your 'backend' folder
    _current_file = Path(__file__).resolve()
    _root_dir = _current_file
    for _ in range(5):
        if (_root_dir / "backend").exists():
            break
        _root_dir = _root_dir.parent
    UPLOAD_FOLDER = _root_dir / "backend" / "app" / "data" / "documents"

# This creates the directory safely without throwing read-only errors on Vercel
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
# ---------------------------------------------

index_service = IndexService()


@router.post("/")
async def upload_pdf(
    file: UploadFile = File(...)
):
    """
    Upload a PDF and automatically index it into Qdrant.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    filename = Path(file.filename).name

    destination = UPLOAD_FOLDER / filename

    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = index_service.index_document(
            str(destination)
        )

        return {
            "status": "success",
            "message": "PDF uploaded and indexed successfully.",
            "filename": filename,
            **result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Indexing failed: {str(e)}"
        )

    finally:
        file.file.close()