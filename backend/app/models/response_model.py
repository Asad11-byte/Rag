from pydantic import BaseModel


class Source(BaseModel):
    score: float
    text: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]