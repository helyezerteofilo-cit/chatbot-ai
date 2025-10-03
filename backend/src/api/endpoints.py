from fastapi import APIRouter, HTTPException
from src.models.api_models import MessageRequest, MessageResponse
from src.services.chatbot_service import ChatbotService

router = APIRouter()
chatbot_service = ChatbotService()

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