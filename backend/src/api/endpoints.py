from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
from src.models.api_models import MessageRequest, MessageResponse, DocumentUploadResponse
from src.services.chatbot_service import ChatbotService
from src.services.document import DocumentService
from src.config.settings import settings
import os

router = APIRouter()
chatbot_service = ChatbotService()
document_service = DocumentService()

@router.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    """
    Chat endpoint to process user messages and return responses
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    response = await chatbot_service.process_message(request.message)
    
    if response.get("status") == "error":
        raise HTTPException(status_code=500, detail=response.get("message", "Unknown error"))
    
    return MessageResponse(
        response=response.get("response", ""),
        status="success",
        context=response.get("context")
    )

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
):
    """
    Upload a document to be used for RAG
    """
    try:
        file_size = 0
        file_content = await file.read()
        file_size = len(file_content)
        
        if file_size > settings.MAX_UPLOAD_SIZE:
            return JSONResponse(
                status_code=413,
                content={
                    "status": "error",
                    "message": f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
                }
            )
        
        filename = file.filename
        _, file_extension = os.path.splitext(filename)
        
        if file_extension.lower() not in ['.txt', '.pdf']:
            return JSONResponse(
                status_code=415,
                content={
                    "status": "error",
                    "message": f"Unsupported file type: {file_extension}. Only .txt and .pdf files are supported."
                }
            )
        
        result = document_service.save_uploaded_document(file_content, filename)
        
        if result["status"] == "error":
            return JSONResponse(
                status_code=500,
                content=result
            )
        
        return DocumentUploadResponse(**result)
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Error uploading document: {str(e)}"
            }
        )