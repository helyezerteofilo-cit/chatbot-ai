import os
import shutil
import uuid
from typing import List, Dict, Any, Optional
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.config.settings import settings

class DocumentService:
    """
    Service to handle document loading, processing, and embedding
    """
    def __init__(self):
        backend_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
        self.documents_folder = os.path.join(backend_dir, settings.RAG_DOCUMENTS_FOLDER)
        self.uploads_folder = os.path.join(backend_dir, settings.UPLOADS_FOLDER)
        self.vector_store_path = os.path.join(backend_dir, settings.VECTOR_STORE_PATH)
        
        self.embedding_model_name = settings.EMBEDDING_MODEL
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
        
        # Create necessary folders if they don't exist
        os.makedirs(self.documents_folder, exist_ok=True)
        os.makedirs(self.uploads_folder, exist_ok=True)
        
    def load_documents(self) -> List[Document]:
        """
        Load documents from the specified folder
        
        Returns:
            List of loaded documents
        """
        documents = []
        
        # Load pre-loaded documents
        documents.extend(self._load_from_folder(self.documents_folder))
        
        # Load user-uploaded documents
        documents.extend(self._load_from_folder(self.uploads_folder))
        
        print(f"Loaded {len(documents)} documents in total")
        return documents
    
    def _load_from_folder(self, folder_path: str) -> List[Document]:
        """
        Load documents from a specific folder
        
        Args:
            folder_path: Path to the folder containing documents
            
        Returns:
            List of loaded documents
        """
        documents = []
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
            return documents
        
        print(f"Loading documents from: {folder_path}")
        
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1].lower()
                
                try:
                    if file_extension == '.txt':
                        print(f"Loading text file: {file_path}")
                        loader = TextLoader(file_path)
                        documents.extend(loader.load())
                    
                    elif file_extension == '.pdf':
                        print(f"Loading PDF file: {file_path}")
                        loader = PyPDFLoader(file_path)
                        documents.extend(loader.load())
                        
                except Exception as e:
                    print(f"Error loading document {file_path}: {str(e)}")
        
        print(f"Loaded {len(documents)} documents from {folder_path}")
        return documents
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """
        Process documents by splitting them into chunks
        
        Args:
            documents: List of documents to process
            
        Returns:
            List of document chunks
        """
        if not documents:
            return []
        
        chunks = self.text_splitter.split_documents(documents)
        print(f"Split documents into {len(chunks)} chunks")
        return chunks
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """
        Create a vector store from the processed documents using Chroma
        
        Args:
            documents: List of processed document chunks
            
        Returns:
            Chroma vector store
        """
        if not documents:
            return None
        
        if os.path.exists(self.vector_store_path):
            shutil.rmtree(self.vector_store_path)
        
        os.makedirs(self.vector_store_path, exist_ok=True)
        
        print(f"Creating Chroma vector store at: {self.vector_store_path}")
        
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.vector_store_path
        )
        
        vector_store.persist()
        
        return vector_store
    
    def load_vector_store(self) -> Chroma:
        """
        Load the vector store from disk
        
        Returns:
            Chroma vector store or None if it doesn't exist
        """
        if not os.path.exists(self.vector_store_path):
            return None
        
        try:
            vector_store = Chroma(
                persist_directory=self.vector_store_path,
                embedding_function=self.embeddings
            )
            return vector_store
        except Exception as e:
            print(f"Error loading vector store: {str(e)}")
            return None
    
    def query_vector_store(self, query: str, k: int = 5) -> List[Document]:
        """
        Query the vector store for relevant documents
        
        Args:
            query: The query string
            k: Number of documents to retrieve
            
        Returns:
            List of relevant document chunks
        """
        vector_store = self.load_vector_store()
        if not vector_store:
            return []
        
        # Get results from vector store
        results = vector_store.similarity_search(query, k=k)
        return results
    
    def setup_rag_system(self) -> Dict[str, Any]:
        """
        Set up the RAG system by loading documents, processing them, and creating a vector store
        Checks if vector store already exists and is up-to-date before reprocessing
        
        Returns:
            Status dictionary
        """
        try:
            if os.path.exists(self.vector_store_path):
                vector_store_mtime = os.path.getmtime(self.vector_store_path)
                
                # Check if any documents in either folder are newer than the vector store
                should_rebuild = False
                
                for folder in [self.documents_folder, self.uploads_folder]:
                    if os.path.exists(folder):
                        latest_doc_mtime = 0
                        for root, _, files in os.walk(folder):
                            for file in files:
                                file_path = os.path.join(root, file)
                                file_mtime = os.path.getmtime(file_path)
                                if file_mtime > latest_doc_mtime:
                                    latest_doc_mtime = file_mtime
                        
                        if latest_doc_mtime > vector_store_mtime:
                            should_rebuild = True
                            break
                
                if not should_rebuild and self.load_vector_store() is not None:
                    return {
                        "status": "success", 
                        "message": "Vector store is up-to-date, skipping document processing"
                    }
            
            documents = self.load_documents()
            if not documents:
                return {"status": "warning", "message": "No documents found to process"}
            
            processed_docs = self.process_documents(documents)
            vector_store = self.create_vector_store(processed_docs)
            
            return {
                "status": "success", 
                "message": f"Successfully processed {len(documents)} documents into {len(processed_docs)} chunks"
            }
        except Exception as e:
            return {"status": "error", "message": f"Error setting up RAG system: {str(e)}"}
    
    def save_uploaded_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Save an uploaded document to the uploads folder
        
        Args:
            file_content: The binary content of the uploaded file
            filename: The name of the uploaded file
            
        Returns:
            Status dictionary with document ID
        """
        try:
            # Create a unique ID for the document
            doc_id = str(uuid.uuid4())
            
            # Get file extension
            _, file_extension = os.path.splitext(filename)
            
            # Only accept supported file types
            if file_extension.lower() not in ['.txt', '.pdf']:
                return {
                    "status": "error",
                    "message": f"Unsupported file type: {file_extension}. Only .txt and .pdf files are supported."
                }
            
            # Create a unique filename
            unique_filename = f"{doc_id}{file_extension}"
            file_path = os.path.join(self.uploads_folder, unique_filename)
            
            # Save the file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Rebuild the vector store to include the new document
            rebuild_status = self.setup_rag_system()
            
            if rebuild_status["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Document saved but error rebuilding vector store: {rebuild_status['message']}"
                }
            
            return {
                "status": "success",
                "message": "Document uploaded and processed successfully",
                "document_id": doc_id,
                "document_name": filename
            }
        except Exception as e:
            return {"status": "error", "message": f"Error saving document: {str(e)}"}