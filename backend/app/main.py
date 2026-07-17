from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.routes.document import router as document_router

from backend.app.routes.index import router as index_router
from backend.app.routes.chat import router as chat_router
from backend.app.routes.upload import router as upload_router
from backend.app.routes import document
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title=settings.Rag_APP_NAME,
    version=settings.APP_VERSION,
)

app.mount(
    "/documents",
    StaticFiles(directory="app/data/documents"),
    name="documents",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://rag-ldnzouwi6-asad11-bytes-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_router)
app.include_router(index_router)
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(document.router)

@app.get("/")
async def root():
    return {
        "status": "running",
        "application": settings.Rag_APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }