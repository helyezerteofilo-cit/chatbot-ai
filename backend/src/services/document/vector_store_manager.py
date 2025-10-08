import os
import shutil
from typing import List, Optional
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


class VectorStoreManager:
    """
    Manages vector store operations for document embeddings
    """
    
    def __init__(self, vector_store_path: str, embedding_model_name: str):
        """
        Initialize the vector store manager
        
        Args:
            vector_store_path: Path to store the vector database
            embedding_model_name: Name of the embedding model to use
        """
        self.vector_store_path = vector_store_path
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self._vector_store_cache = None
    
    def create_vector_store(self, documents: List[Document]) -> Optional[Chroma]:
        """
        Create a vector store from processed documents
        
        Args:
            documents: List of processed document chunks
            
        Returns:
            Chroma vector store or None if creation fails
        """
        if not documents:
            print("No documents provided for vector store creation")
            return None
        
        try:
            # Clean up existing vector store
            self._cleanup_existing_store()
            
            # Ensure directory exists
            os.makedirs(self.vector_store_path, exist_ok=True)
            
            print(f"Creating Chroma vector store at: {self.vector_store_path}")
            
            vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.vector_store_path
            )
            
            # Update cache
            self._vector_store_cache = vector_store
            print("Vector store created successfully")
            
            return vector_store
            
        except Exception as e:
            print(f"Error creating vector store: {str(e)}")
            raise e
    
    def load_vector_store(self) -> Optional[Chroma]:
        """
        Load the vector store from disk or cache
        
        Returns:
            Chroma vector store or None if it doesn't exist
        """
        # Return cached instance if available
        if self._vector_store_cache is not None:
            return self._vector_store_cache
        
        if not self._vector_store_exists():
            return None
        
        try:
            vector_store = Chroma(
                persist_directory=self.vector_store_path,
                embedding_function=self.embeddings
            )
            
            # Cache the loaded instance
            self._vector_store_cache = vector_store
            print("Loaded persistent vector store")
            return vector_store
            
        except Exception as e:
            print(f"Error loading vector store: {str(e)}")
            return None
    
    def add_documents_to_existing_store(self, new_documents: List[Document]) -> bool:
        """
        Add new documents to existing vector store
        
        Args:
            new_documents: List of new document chunks to add
            
        Returns:
            True if successful, False otherwise
        """
        vector_store = self.load_vector_store()
        if not vector_store or not new_documents:
            return False
        
        try:
            vector_store.add_documents(new_documents)
            print(f"Added {len(new_documents)} documents to existing vector store")
            return True
        except Exception as e:
            print(f"Error adding documents to vector store: {str(e)}")
            return False
    
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
            print("No vector store available for querying")
            return []
        
        try:
            results = vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Error querying vector store: {str(e)}")
            return []
    
    def is_vector_store_outdated(self, document_folders: List[str]) -> bool:
        """
        Check if vector store should be rebuilt based on file modification times
        
        Args:
            document_folders: List of folders to check for newer files
            
        Returns:
            True if vector store should be rebuilt, False otherwise
        """
        if not self._vector_store_exists():
            return True  # Need to build initial store
        
        try:
            vector_store_mtime = os.path.getmtime(self.vector_store_path)
            
            # Check if any documents are newer than the vector store
            for folder in document_folders:
                if os.path.exists(folder):
                    for root, _, files in os.walk(folder):
                        for file in files:
                            file_path = os.path.join(root, file)
                            if os.path.getmtime(file_path) > vector_store_mtime:
                                return True
            
            return False
        except Exception:
            return True  # Rebuild on any error
    
    def _cleanup_existing_store(self):
        """Clean up existing vector store directory"""
        if os.path.exists(self.vector_store_path):
            try:
                shutil.rmtree(self.vector_store_path)
                print(f"Removed existing vector store at: {self.vector_store_path}")
            except Exception as e:
                print(f"Warning: Could not remove existing vector store: {e}")
    
    def _vector_store_exists(self) -> bool:
        """Check if vector store exists and has content"""
        if not os.path.exists(self.vector_store_path):
            return False
        
        try:
            contents = os.listdir(self.vector_store_path)
            return len(contents) > 0
        except Exception:
            return False