from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocumentProcessor:
    """
    Handles document processing and text splitting
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor
        
        Args:
            chunk_size: Size of each text chunk
            chunk_overlap: Overlap between chunks
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
    
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
    
    def update_chunk_settings(self, chunk_size: int, chunk_overlap: int):
        """
        Update chunk size and overlap settings
        
        Args:
            chunk_size: New chunk size
            chunk_overlap: New chunk overlap
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        print(f"Updated chunk settings: size={chunk_size}, overlap={chunk_overlap}")