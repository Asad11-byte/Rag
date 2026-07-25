import os
import shutil
import tempfile
import uuid
from pathlib import Path

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

# ==========================================
# Upload Directory
# ==========================================
# On Vercel, only /tmp is writable — and it does NOT persist across
# cold starts or across concurrent instances. That's fine here: the
# PDF only needs to exist long enough for index_service to parse and
# embed it into Qdrant, which IS the durable store. We write to a
# per-request temp path and delete it once indexing is done, rather
# than treating local disk as permanent storage.

IS_VERCEL = bool(os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))

if IS_VERCEL:
    UPLOAD_FOLDER = Path(tempfile.gettempdir()) / "uploads"
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    UPLOAD_FOLDER = BASE_DIR / "data" / "documents"

# NOTE: this is safe to call at import time because /tmp itself always
# exists and is writable on Vercel — we're just creating a subfolder
# inside it, not trying to write to a read-only project directory
# like the old `BASE_DIR / "data" / "documents"` path did in production.
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# ==========================================
# Services
# ==========================================

index_service = IndexService()


# ==========================================
# Upload PDF
# ==========================================

@router.post("/")
async def upload_pdf(
    file: UploadFile = File(...)
):
    """
    Upload a PDF and automatically index it into Qdrant.

    The PDF itself is only kept on disk for the duration of this
    request (long enough for index_service to parse/chunk/embed it).
    The durable result of this call is what ends up in Qdrant, not
    the file on disk.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    original_filename = Path(file.filename).name

    # Prefix with a uuid so concurrent uploads of files with the same
    # name never collide on the same instance.
    destination = UPLOAD_FOLDER / f"{uuid.uuid4().hex}_{original_filename}"

    try:

        # Save uploaded PDF to the request-scoped temp location
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Index into Qdrant — this is the step that actually persists
        result = index_service.index_document(
            str(destination)
        )

        return {
            "status": "success",
            "message": "PDF uploaded and indexed successfully.",
            "filename": original_filename,
            **result,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload/index PDF: {str(e)}"
        )

    finally:

        file.file.close()

        # Clean up the temp file — it's already embedded into Qdrant,
        # no reason to keep it around (and /tmp space is limited).
        destination.unlink(missing_ok=True)