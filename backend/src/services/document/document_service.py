import os
from typing import List, Dict, Any, Optional
from langchain.schema import Document

from src.config.settings import settings
from .document_loader import DocumentLoader
from .document_processor import DocumentProcessor
from .vector_store_manager import VectorStoreManager
from .upload_handler import UploadHandler


class DocumentService:
    """
    Main interface for document operations - coordinates all document-related services
    """
    
    def __init__(self):
        """Initialize the document service with all required components"""
        backend_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        
        self.documents_folder = os.path.join(backend_dir, settings.RAG_DOCUMENTS_FOLDER)
        self.uploads_folder = os.path.join(backend_dir, settings.UPLOADS_FOLDER)
        self.vector_store_path = os.path.join(backend_dir, settings.VECTOR_STORE_PATH)
        
        self.processor = DocumentProcessor(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        self.vector_store_manager = VectorStoreManager(
            vector_store_path=self.vector_store_path,
            embedding_model_name=settings.EMBEDDING_MODEL
        )
        
        self.upload_handler = UploadHandler(
            uploads_folder=self.uploads_folder,
            processor=self.processor
        )
        
        os.makedirs(self.documents_folder, exist_ok=True)
        os.makedirs(self.uploads_folder, exist_ok=True)
    
    def load_all_documents(self) -> List[Document]:
        """
        Load documents from all configured folders
        
        Returns:
            List of loaded documents
        """
        folder_paths = [self.documents_folder, self.uploads_folder]
        return DocumentLoader.load_multiple_folders(folder_paths)
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """
        Process documents using the document processor
        
        Args:
            documents: List of documents to process
            
        Returns:
            List of processed document chunks
        """
        return self.processor.process_documents(documents)
    
    def create_vector_store(self, documents: List[Document]) -> Optional[object]:
        """
        Create vector store from processed documents
        
        Args:
            documents: List of processed document chunks
            
        Returns:
            Vector store instance or None
        """
        return self.vector_store_manager.create_vector_store(documents)
    
    def load_vector_store(self) -> Optional[object]:
        """
        Load existing vector store
        
        Returns:
            Vector store instance or None
        """
        return self.vector_store_manager.load_vector_store()
    
    def query_vector_store(self, query: str, k: int = 5) -> List[Document]:
        """
        Query the vector store for relevant documents
        
        Args:
            query: The query string
            k: Number of documents to retrieve
            
        Returns:
            List of relevant document chunks
        """
        return self.vector_store_manager.query_vector_store(query, k)
    
    def setup_rag_system(self) -> Dict[str, Any]:
        """
        Set up the RAG system by coordinating all components
        
        Returns:
            Status dictionary
        """
        try:
            folder_paths = [self.documents_folder, self.uploads_folder]
            
            existing_vector_store = self.vector_store_manager.load_vector_store()
            if existing_vector_store and not self.vector_store_manager.is_vector_store_outdated(folder_paths):
                return {
                    "status": "success", 
                    "message": "Vector store is up-to-date, skipping document processing"
                }
            
            print("Building/rebuilding vector store...")
            documents = self.load_all_documents()
            
            if not documents:
                return {"status": "warning", "message": "No documents found to process"}
            
            processed_docs = self.process_documents(documents)
            vector_store = self.create_vector_store(processed_docs)
            
            if vector_store is None:
                return {"status": "error", "message": "Failed to create vector store"}
            
            return {
                "status": "success", 
                "message": f"Successfully processed {len(documents)} documents into {len(processed_docs)} chunks"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error setting up RAG system: {str(e)}"}
    
    def save_uploaded_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Handle document upload with intelligent vector store updating
        
        Args:
            file_content: The binary content of the uploaded file
            filename: The name of the uploaded file
            
        Returns:
            Status dictionary with document information
        """
        try:
            save_result = self.upload_handler.save_uploaded_file(file_content, filename)
            
            if save_result["status"] == "error":
                return save_result
            
            file_path = save_result["file_path"]
            doc_id = save_result["document_id"]
            
            try:
                processed_new_docs = self.upload_handler.load_and_process_uploaded_file(file_path)
                
                if self.vector_store_manager.add_documents_to_existing_store(processed_new_docs):
                    return {
                        "status": "success",
                        "message": "Document uploaded and added to existing vector store successfully",
                        "document_id": doc_id,
                        "document_name": filename
                    }
                else:
                    print("Could not add to existing store, rebuilding...")
                    
            except Exception as e:
                print(f"Error adding to existing store: {e}, rebuilding...")
            
            rebuild_status = self.setup_rag_system()
            
            if rebuild_status["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Document saved but error rebuilding vector store: {rebuild_status['message']}"
                }
            
            return {
                "status": "success",
                "message": "Document uploaded and processed successfully (vector store rebuilt)",
                "document_id": doc_id,
                "document_name": filename
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error processing upload: {str(e)}"}