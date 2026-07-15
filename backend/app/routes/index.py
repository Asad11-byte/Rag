from fastapi import APIRouter

from app.services.index_service import IndexService

router = APIRouter(
    prefix="/index",
    tags=["Index"],
)

service = IndexService()


@router.post("/")
async def index_document():

    return service.index_document(
        "app/data/documents/AI-Agent-Security.pdf"
    )