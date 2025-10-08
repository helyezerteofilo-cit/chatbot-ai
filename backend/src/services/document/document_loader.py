import os
from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader


class DocumentLoader:
    """
    Handles loading documents from files and folders
    """
    
    @staticmethod
    def load_from_folder(folder_path: str) -> List[Document]:
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
                    loaded_docs = DocumentLoader._load_single_file(file_path, file_extension)
                    documents.extend(loaded_docs)
                except Exception as e:
                    print(f"Error loading document {file_path}: {str(e)}")
        
        print(f"Loaded {len(documents)} documents from {folder_path}")
        return documents
    
    @staticmethod
    def _load_single_file(file_path: str, file_extension: str) -> List[Document]:
        """
        Load a single file based on its extension
        
        Args:
            file_path: Path to the file
            file_extension: File extension
            
        Returns:
            List of loaded documents
        """
        if file_extension == '.txt':
            print(f"Loading text file: {file_path}")
            loader = TextLoader(file_path)
            return loader.load()
        
        elif file_extension == '.pdf':
            print(f"Loading PDF file: {file_path}")
            loader = PyPDFLoader(file_path)
            return loader.load()
        
        else:
            print(f"Unsupported file type: {file_extension}")
            return []
    
    @staticmethod
    def load_multiple_folders(folder_paths: List[str]) -> List[Document]:
        """
        Load documents from multiple folders
        
        Args:
            folder_paths: List of folder paths
            
        Returns:
            List of all loaded documents
        """
        all_documents = []
        
        for folder_path in folder_paths:
            documents = DocumentLoader.load_from_folder(folder_path)
            all_documents.extend(documents)
        
        print(f"Loaded {len(all_documents)} documents in total from {len(folder_paths)} folders")
        return all_documents