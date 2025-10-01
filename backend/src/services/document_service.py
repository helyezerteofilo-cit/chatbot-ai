import os
from typing import List, Dict, Any
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from src.config.settings import settings

class DocumentService:
    """
    Service to handle document loading, processing, and embedding
    """
    def __init__(self):
        self.documents_folder = settings.RAG_DOCUMENTS_FOLDER
        self.vector_store_path = settings.VECTOR_STORE_PATH
        self.embedding_model_name = settings.EMBEDDING_MODEL
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
        
    def load_documents(self) -> List[Document]:
        """
        Load documents from the specified folder
        
        Returns:
            List of loaded documents
        """
        documents = []
        
        # Ensure the documents folder exists
        if not os.path.exists(self.documents_folder):
            os.makedirs(self.documents_folder)
            print(f"Created documents folder: {self.documents_folder}")
            return documents
        
        # Walk through the documents folder
        for root, _, files in os.walk(self.documents_folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1].lower()
                
                try:
                    # Load text files
                    if file_extension == '.txt':
                        loader = TextLoader(file_path)
                        documents.extend(loader.load())
                    
                    # Load PDF files
                    elif file_extension == '.pdf':
                        loader = PyPDFLoader(file_path)
                        documents.extend(loader.load())
                        
                except Exception as e:
                    print(f"Error loading document {file_path}: {str(e)}")
        
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
        
        return self.text_splitter.split_documents(documents)
    
    def create_vector_store(self, documents: List[Document]) -> FAISS:
        """
        Create a vector store from the processed documents
        
        Args:
            documents: List of processed document chunks
            
        Returns:
            FAISS vector store
        """
        if not documents:
            return None
        
        # Create vector store directory if it doesn't exist
        os.makedirs(os.path.dirname(self.vector_store_path), exist_ok=True)
        
        # Create and save the vector store
        vector_store = FAISS.from_documents(documents, self.embeddings)
        vector_store.save_local(self.vector_store_path)
        
        return vector_store
    
    def load_vector_store(self) -> FAISS:
        """
        Load the vector store from disk
        
        Returns:
            FAISS vector store or None if it doesn't exist
        """
        if os.path.exists(self.vector_store_path):
            return FAISS.load_local(self.vector_store_path, self.embeddings)
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
        
        return vector_store.similarity_search(query, k=k)
    
    def setup_rag_system(self) -> Dict[str, Any]:
        """
        Set up the RAG system by loading documents, processing them, and creating a vector store
        
        Returns:
            Status dictionary
        """
        try:
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