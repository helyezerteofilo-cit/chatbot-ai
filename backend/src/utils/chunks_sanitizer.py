"""
Utility functions for cleaning and normalizing text
"""
import re
from typing import List
from langchain.schema import Document


def chunks_sanitizer(chunks: List[Document]) -> List[Document]:
    """
    Clean and normalize text in Document objects by removing excessive whitespace,
    HTML tags, and other formatting issues.
    
    Args:
        chunks: List of Document objects to clean
        
    Returns:
        List of Document objects with cleaned text
    """
    if not chunks:
        return []
    
    cleaned_chunks = []
    for doc in chunks:
        if not doc or not doc.page_content:
            continue
        
        text = doc.page_content
        
        # Remove HTML tags
        cleaned = re.sub(r'<.*?>', '', text)
        # Replace all newlines with spaces (remove completely)
        cleaned = re.sub(r'\n', ' ', cleaned)
        # Remove excessive spaces between words
        cleaned = re.sub(r'\s{2,}', ' ', cleaned)
        # Trim leading/trailing whitespace
        cleaned = cleaned.strip()
        
        # Create a new Document with cleaned text but keep the original metadata
        cleaned_doc = Document(
            page_content=cleaned,
            metadata=doc.metadata,
            type=doc.type
        )
        cleaned_chunks.append(cleaned_doc)
    
    return cleaned_chunks