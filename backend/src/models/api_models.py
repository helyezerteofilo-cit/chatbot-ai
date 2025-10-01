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

class HealthResponse(BaseModel):
    """
    Response model for health check
    """
    status: str
    message: str
    rag_status: Optional[Dict[str, Any]] = None
    api_status: Optional[Dict[str, Any]] = None