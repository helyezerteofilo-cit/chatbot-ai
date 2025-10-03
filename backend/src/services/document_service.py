import os
import shutil
from typing import List, Dict, Any
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
        self.vector_store_path = os.path.join(backend_dir, settings.VECTOR_STORE_PATH)
        
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
        
        if not os.path.exists(self.documents_folder):
            os.makedirs(self.documents_folder)
            print(f"Created documents folder: {self.documents_folder}")
            return documents
        
        print(f"Loading documents from: {self.documents_folder}")
        
        for root, _, files in os.walk(self.documents_folder):
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
        
        print(f"Loaded {len(documents)} documents")
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