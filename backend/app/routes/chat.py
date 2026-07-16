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
    """
    Streaming endpoint.
    Streams only the answer.
    """

    generator = rag.stream(request.question)

    return StreamingResponse(
        generator,
        media_type="text/plain",
    )


@router.post("/retrieve")
async def retrieve_context(
    request: ChatRequest,
):
    """
    Retrieve the context and citations without calling the LLM.
    Useful for debugging and future frontend citations.
    """

    retrieval = rag.retrieve(request.question)

    return {
        "context": retrieval["context"],
        "citations": retrieval["citations"],
    }


@router.post("/ask")
async def ask(
    request: ChatRequest,
):
    """
    Non-streaming endpoint.

    Returns the answer together with citations.
    This is useful for testing and will later be
    replaced by SSE streaming with citations.
    """

    result = rag.ask(request.question)

    answer = ""

    for token in result["answer"]:
        answer += token

    return {
        "answer": answer,
        "citations": result["citations"],
    }