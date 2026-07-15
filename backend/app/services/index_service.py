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

        # Load document
        text = self.loader.load_document(file_path)

        # Split into chunks
        chunks = self.chunker.chunk_text(text)

        # Temporary for testing (remove later)
        chunks = chunks[:3]

        # Generate embeddings
        embeddings = self.embedding.embed_documents(chunks)

        # Create collection
        self.qdrant.create_collection(
            vector_size=len(embeddings[0])
        )

        # Upload vectors
        self.qdrant.upload_vectors(
            embeddings,
            chunks,
        )

        return {
            "status": "success",
            "characters": len(text),
            "chunks": len(chunks),
            "vectors_uploaded": len(embeddings),
        }