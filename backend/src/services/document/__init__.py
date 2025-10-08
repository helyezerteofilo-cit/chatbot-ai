"""
Document Service Module

This module provides a modular approach to document processing, including:
- Document loading from various sources
- Text processing and chunking
- Vector store management
- Document upload handling

Usage:
    from src.services.document import DocumentService
    
    # Initialize the service
    doc_service = DocumentService()
    
    # Set up RAG system
    result = doc_service.setup_rag_system()
    
    # Upload a document
    upload_result = doc_service.save_uploaded_document(file_content, filename)
    
    # Query documents
    results = doc_service.query_vector_store("your query here")
"""

from .document_service import DocumentService
from .document_loader import DocumentLoader
from .document_processor import DocumentProcessor
from .vector_store_manager import VectorStoreManager
from .upload_handler import UploadHandler

__all__ = [
    'DocumentService',
    'DocumentLoader', 
    'DocumentProcessor',
    'VectorStoreManager',
    'UploadHandler'
]