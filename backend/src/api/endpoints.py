from fastapi import APIRouter, Depends, HTTPException
from src.models.api_models import MessageRequest, MessageResponse, HealthResponse
from src.services.chatbot_service import ChatbotService

router = APIRouter()
chatbot_service = ChatbotService()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the API and services are working
    """
    setup_status = await chatbot_service.setup()
    
    return HealthResponse(
        status="ok",
        message="API is running",
        rag_status=setup_status.get("rag_status"),
        api_status=setup_status.get("api_status")
    )

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