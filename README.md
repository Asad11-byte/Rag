# AI Agent Security RAG Application

A Retrieval-Augmented Generation (RAG) application built with **FastAPI**, **React (Vite)**, **Groq LLM**, **Voyage AI Embeddings**, and **Qdrant Vector Database**. The application allows users to upload PDF documents, index them into a vector database, and ask natural language questions with answers generated from the uploaded document.

---

# Features

* 📄 Upload PDF documents
* ✂️ Automatic document chunking
* 🧠 Generate embeddings using Voyage AI
* 🗄️ Store vectors in Qdrant Cloud
* 🔍 Semantic search over document chunks
* 🤖 AI-powered answers using Groq LLM
* ⚡ Streaming responses
* 💬 ChatGPT-inspired interface
* 🌐 FastAPI REST API
* ⚛️ React + Vite frontend

---

# Technology Stack

## Backend

* FastAPI
* Python 3.11+
* Groq API
* Voyage AI
* Qdrant Cloud
* PyMuPDF (PDF text extraction)
* Pydantic

## Frontend

* React
* Vite
* Axios
* React Markdown
* Lucide React

---

# Project Structure

```text
Rag/
│
├── backend/
│   ├── app/
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── routes/
│   │   ├── chat.py
│   │   └── upload.py
│   │
│   ├── services/
│   │   ├── chunk_service.py
│   │   ├── document_loader.py
│   │   ├── groq_service.py
│   │   ├── index_service.py
│   │   ├── qdrant_service.py
│   │   ├── rag_service.py
│   │   └── voyage_service.py
│   │
│   ├── models/
│   │   ├── request_model.py
│   │   └── response_model.py
│   │
│   ├── data/
│   │   └── documents/
│   │
│   └── main.py
│
├── frontend/
│   ├── src/
│   │
│   ├── components/
│   ├── hooks/
│   ├── pages/
│   ├── services/
│   ├── styles/
│   ├── App.jsx
│   └── main.jsx
│
├── .env
├── README.md
└── requirements.txt
```

---

# RAG Workflow

```text
                Upload PDF
                     │
                     ▼
          Extract Text (PyMuPDF)
                     │
                     ▼
            Split into Chunks
                     │
                     ▼
        Generate Voyage Embeddings
                     │
                     ▼
        Store Vectors in Qdrant
                     │
                     ▼
          User asks a Question
                     │
                     ▼
        Generate Question Embedding
                     │
                     ▼
        Semantic Search (Qdrant)
                     │
                     ▼
        Retrieve Relevant Chunks
                     │
                     ▼
      Send Context + Question to Groq
                     │
                     ▼
         Stream AI Response to User
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
# Groq
GROQ_API_KEY=your_groq_api_key

# Voyage AI
VOYAGE_API_KEY=your_voyage_api_key

# Qdrant
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/ai-agent-security-rag.git

cd ai-agent-security-rag
```

---

## Backend Setup

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run backend

```bash
uvicorn app.main:app --reload
```

Backend URL

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

Navigate to frontend

```bash
cd frontend
```

Install dependencies

```bash
npm install
```

Create `.env`

```env
VITE_API_URL=http://127.0.0.1:8000
```

Run

```bash
npm run dev
```

Frontend

```
http://localhost:5173
```

---

# API Endpoints

## Upload PDF

```
POST /upload/
```

Uploads a PDF document and automatically indexes it into Qdrant.

---

## Chat

```
POST /chat/stream
```

Streams AI-generated responses based on the uploaded document.

Example Request

```json
{
  "question": "What is Prompt Injection?"
}
```

---

# How It Works

1. Upload a PDF document.
2. The backend extracts text from the PDF.
3. The text is split into smaller chunks.
4. Voyage AI generates embeddings for each chunk.
5. The embeddings are stored in Qdrant.
6. When a user asks a question, the question is embedded.
7. Qdrant retrieves the most relevant chunks.
8. The retrieved context and user question are sent to Groq.
9. Groq streams a contextual response back to the frontend.

---

# Current Limitations

* Supports PDF documents only.
* Free Voyage AI accounts have rate limits.
* Uploaded documents are not persisted across a fresh Qdrant collection reset.
* No authentication or multi-user document separation.

---

# Future Improvements

* Multiple document support
* Conversation history
* Source citations with page numbers
* Document management (list/delete)
* Drag-and-drop uploads
* User authentication
* Hybrid search (keyword + vector)
* Reranking retrieved chunks
* Docker support
* Cloud deployment

---

# Screenshots

Add screenshots of:

* Home Page
* Upload PDF
* Chat Interface
* Streaming Response

---

# License

This project is developed for educational purposes as part of a Retrieval-Augmented Generation (RAG) assignment.

---

# Author

**Asad Ali**

BS Computer Science

AI Agent Security RAG Application

---

## Acknowledgements

* FastAPI
* React
* Groq
* Voyage AI
* Qdrant
* PyMuPDF
* Vite


