from pathlib import Path

from app.services.document_loader import DocumentLoader
from app.services.chunk_service import ChunkService
from app.services.jina_service import JinaService
from app.services.qdrant_service import QdrantService


class IndexService:

    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = ChunkService()
        self.embedding = JinaService()
        self.qdrant = QdrantService()

    def index_document(self, file_path: str):

        # Load PDF page-by-page
        pages = self.loader.load_document(file_path)

        if not pages:
            raise Exception("No text could be extracted from the PDF.")

        # Create chunks (each chunk contains text + page)
        chunks = self.chunker.chunk_text(pages)

        if not chunks:
            raise Exception("No chunks were created from the document.")

        # -------------------------------------------------
        # TEMPORARY FOR JINA FREE TIER TESTING
        # Remove this line once you want to index the full PDF
        # -------------------------------------------------
        chunks = chunks[:3]

        # Extract only text for embedding
        chunk_texts = [
            chunk["text"]
            for chunk in chunks
        ]

        # Generate embeddings
        embeddings = self.embedding.embed_documents(
            chunk_texts
        )

        if not embeddings:
            raise Exception("Embedding generation failed.")

        # Create collection if it doesn't exist
        self.qdrant.create_collection(
            vector_size=len(embeddings[0])
        )

        # Source filename
        source_name = Path(file_path).name

        # Upload vectors with metadata
        self.qdrant.upload_vectors(
            embeddings=embeddings,
            chunks=chunks,
            source_name=source_name,
        )

        return {
            "status": "success",
            "source": source_name,
            "pages": len(pages),
            "chunks": len(chunks),
            "vectors_uploaded": len(embeddings),
        }