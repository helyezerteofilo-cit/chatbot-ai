from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class MessageRequest(BaseModel):
    """
    Request model for chat messages
    """
    message: str

class MessageResponse(BaseModel):
    """
    Response model for chat messages
    """
    response: str
    status: str
    context: Optional[Dict[str, Any]] = None

class DocumentUploadResponse(BaseModel):
    """
    Response model for document uploads
    """
    status: str
    message: str
    document_id: Optional[str] = None
    document_name: Optional[str] = None