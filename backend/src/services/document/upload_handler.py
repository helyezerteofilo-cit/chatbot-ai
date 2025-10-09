import os
import uuid
from typing import Dict, Any
from langchain_community.document_loaders import TextLoader, PyPDFLoader

from .document_processor import DocumentProcessor


class UploadHandler:
    """
    Handles document upload operations
    """
    
    def __init__(self, uploads_folder: str, processor: DocumentProcessor):
        """
        Initialize the upload handler
        
        Args:
            uploads_folder: Path to the uploads folder
            processor: Document processor instance
        """
        self.uploads_folder = uploads_folder
        self.processor = processor
        
        os.makedirs(uploads_folder, exist_ok=True)
    
    def save_uploaded_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Save an uploaded file to the uploads folder
        
        Args:
            file_content: The binary content of the uploaded file
            filename: The name of the uploaded file
            
        Returns:
            Status dictionary with file information
        """
        try:
            validation_result = self._validate_file(filename)
            if validation_result["status"] == "error":
                return validation_result
            
            doc_id = str(uuid.uuid4())
            _, file_extension = os.path.splitext(filename)
            unique_filename = f"{doc_id}{file_extension}"
            file_path = os.path.join(self.uploads_folder, unique_filename)
            
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            print(f"Document saved: {file_path}")
            
            return {
                "status": "success",
                "document_id": doc_id,
                "document_name": filename,
                "file_path": file_path
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error saving document: {str(e)}"
            }
    
    def load_and_process_uploaded_file(self, file_path: str):
        """
        Load and process a single uploaded file
        
        Args:
            file_path: Path to the uploaded file
            
        Returns:
            Processed document chunks
        """
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.txt':
                loader = TextLoader(file_path)
            elif file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
            
            documents = loader.load()
            
            processed_docs = self.processor.process_documents(documents)
            
            return processed_docs
            
        except Exception as e:
            print(f"Error processing uploaded file {file_path}: {str(e)}")
            raise e
    
    def _validate_file(self, filename: str) -> Dict[str, Any]:
        """
        Validate uploaded file
        
        Args:
            filename: Name of the file to validate
            
        Returns:
            Validation result
        """
        _, file_extension = os.path.splitext(filename)
        
        if file_extension.lower() not in ['.txt', '.pdf']:
            return {
                "status": "error",
                "message": f"Unsupported file type: {file_extension}. Only .txt and .pdf files are supported."
            }
        
        return {
            "status": "success",
            "message": "File validation passed"
        }