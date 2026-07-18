from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routes.document import router as document_router
from app.routes.index import router as index_router
from app.routes.chat import router as chat_router
from app.routes.upload import router as upload_router
from app.routes import document


app = FastAPI(
    title=settings.Rag_APP_NAME,
    version=settings.APP_VERSION,
)

# ==================================================
# Documents Directory
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/documents",
    StaticFiles(directory=DOCUMENTS_DIR),
    name="documents",
)

# ==================================================
# CORS
# ==================================================

ALLOWED_ORIGINS = [
    "http://localhost:5173",

    # Replace with your actual Vercel domain
    "https://rag-gold-sigma.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================================
# Routes
# ==================================================

app.include_router(document_router)
app.include_router(index_router)
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(document.router)

# ==================================================
# Health
# ==================================================

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
        "status": "healthy",
    }