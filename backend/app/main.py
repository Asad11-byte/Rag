from pathlib import Path
import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routes.document import router as document_router
from app.routes.index import router as index_router
from app.routes.chat import router as chat_router
from app.routes.upload import router as upload_router


app = FastAPI(
    title=settings.Rag_APP_NAME,
    version=settings.APP_VERSION,
)

# ==================================================
# Documents Directory (served as static files)
# Mounted at /api/documents so it's covered by the same
# vercel.json rule that already routes /api/(.*) -> api/index.py
# — no separate routing rule needed.
# ==================================================
BASE_DIR = Path(__file__).resolve().parent
IS_VERCEL = bool(os.getenv("VERCEL"))

DOCUMENTS_DIR = BASE_DIR / "data" / "documents"

if not IS_VERCEL:
    # Local dev: create the folder if it doesn't exist yet
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

if DOCUMENTS_DIR.exists():
    # On Vercel this directory is read-only but that's fine —
    # StaticFiles only needs read access. We never call .mkdir()
    # here since the deployment filesystem is read-only outside /tmp.
    app.mount("/api/documents", StaticFiles(directory=DOCUMENTS_DIR), name="documents")

# ==================================================
# CORS
# ==================================================

ALLOWED_ORIGINS = [
    "http://localhost:5173",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================================
# API Router (prefixed with /api to match vercel.json
# routing and the frontend's VITE_API_URL=/api)
# ==================================================

api_router = APIRouter(prefix="/api")

api_router.include_router(document_router)
api_router.include_router(index_router)
api_router.include_router(chat_router)
api_router.include_router(upload_router)


@api_router.get("/")
async def root():
    return {
        "status": "running",
        "application": settings.Rag_APP_NAME,
        "version": settings.APP_VERSION,
    }


@api_router.get("/health")
async def health():
    return {
        "status": "healthy",
    }


app.include_router(api_router)