from typing import Dict, Any, Optional, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.config.settings import settings
from src.utils.token_manager import TokenManager

class FlowAPIService:
    """
    Service to interact with CI&T Flow APIs using LangChain's ChatOpenAI
    """
    def __init__(self):
        self.token_manager = TokenManager()
        self.chat_model = None
    
    async def _get_chat_model(self):
        """
        Gets a ChatOpenAI instance with a valid token
        
        Returns:
            ChatOpenAI instance configured with a valid token
        """
        token = await self.token_manager.get_valid_token()
        
        return ChatOpenAI(
            base_url=settings.FLOW_API_BASE_URL,
            api_key=token,
            model=settings.FLOW_MODEL,
            default_headers={
                "FlowAgent": settings.FLOW_AGENT,
                "FlowTenant": settings.FLOW_TENANT,
            }
        )
    
    async def generate_response(self, 
                               message: str, 
                               context_chunks: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate a response using the CI&T Flow LLM via LangChain's ChatOpenAI
        
        Args:
            message: The user's message
            context_chunks: Optional list of document chunks to provide context
        
        Returns:
            Dictionary containing the LLM response
        """
        try:
            chat_model = await self._get_chat_model()
            
            system_content = "You are a helpful assistant."
            if context_chunks and len(context_chunks) > 0:
                context_text = "\n\n".join(context_chunks)
                system_content = f"You are a helpful assistant. Use the following information to answer the user's question:\n\n{context_text}"
            
            messages = [
                SystemMessage(content=system_content),
                HumanMessage(content=message)
            ]
            
            response = chat_model.invoke(messages)
            
            return {
                "status": "success",
                "response": response.content,
            }
        except Exception as e:
            return {"status": "error", "message": f"Error generating response: {str(e)}"}