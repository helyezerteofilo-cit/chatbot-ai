import uvicorn
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import router as api_router
from src.services.document.document_service import DocumentService
from src.config.settings import settings

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for the FastAPI application
    """
    # Create necessary folders
    backend_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    documents_folder = os.path.join(backend_dir, settings.RAG_DOCUMENTS_FOLDER)
    uploads_folder = os.path.join(backend_dir, settings.UPLOADS_FOLDER)
    
    os.makedirs(documents_folder, exist_ok=True)
    os.makedirs(uploads_folder, exist_ok=True)
    
    print(f"Documents folder: {documents_folder}")
    print(f"Uploads folder: {uploads_folder}")
    
    # Initialize RAG system
    print("Initializing RAG system...")
    doc_service = DocumentService()
    rag_status = doc_service.setup_rag_system()
    print(f"RAG system initialization: {rag_status['status']}")
    print(f"Message: {rag_status['message']}")
    print("Initialization complete!")
    
    yield
    
    print("Shutting down...")

app = FastAPI(
    title="CI&T Flow RAG Chatbot",
    description="A chatbot that uses RAG with CI&T Flow API",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)