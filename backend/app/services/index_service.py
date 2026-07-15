from pathlib import Path

from app.services.document_loader import DocumentLoader
from app.services.chunk_service import ChunkService
from app.services.voyage_service import VoyageService
from app.services.qdrant_service import QdrantService


class IndexService:

    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = ChunkService()
        self.embedding = VoyageService()
        self.qdrant = QdrantService()

    def index_document(self, file_path: str):

        # Load PDF
        text = self.loader.load_document(file_path)

        if not text.strip():
            raise Exception("No text could be extracted from the PDF.")

        # Create chunks
        chunks = self.chunker.chunk_text(text)

        if not chunks:
            raise Exception("No chunks were created from the document.")

        # Remove this line after testing if you want the full document indexed
        chunks = chunks[:3]

        # Generate embeddings
        embeddings = self.embedding.embed_documents(chunks)

        if not embeddings:
            raise Exception("Embedding generation failed.")

        # Create collection
        self.qdrant.create_collection(
            vector_size=len(embeddings[0])
        )

        # Get filename for metadata
        source_name = Path(file_path).name

        # Upload vectors
        self.qdrant.upload_vectors(
            embeddings=embeddings,
            chunks=chunks,
            source_name=source_name,
        )

        return {
            "status": "success",
            "source": source_name,
            "characters": len(text),
            "chunks": len(chunks),
            "vectors_uploaded": len(embeddings),
        }