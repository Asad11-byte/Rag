from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.request_model import ChatRequest
from app.services.rag_service import RagService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

rag = RagService()


@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
):
    generator = rag.stream(request.question)

    return StreamingResponse(
        generator,
        media_type="text/plain",
    )