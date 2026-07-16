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

UPLOAD_FOLDER = Path("app/data/documents")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

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