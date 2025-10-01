import httpx
from typing import Dict, Any, Optional, List
from src.config.settings import settings

class CIITFlowAPIService:
    """
    Service to interact with CI&T Flow APIs
    """
    def __init__(self):
        self.base_url = settings.CIIT_FLOW_API_BASE_URL
        self.api_token = settings.CIIT_FLOW_API_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check to verify the API connection
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/health",
                    headers=self.headers
                )
                response.raise_for_status()
                return {"status": "ok", "message": "Successfully connected to CI&T Flow API"}
            except httpx.HTTPStatusError as e:
                return {"status": "error", "message": f"API error: {str(e)}"}
            except Exception as e:
                return {"status": "error", "message": f"Connection error: {str(e)}"}
    
    async def generate_response(self, 
                               message: str, 
                               context_chunks: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate a response using the CI&T Flow LLM
        
        Args:
            message: The user's message
            context_chunks: Optional list of document chunks to provide context
        
        Returns:
            Dictionary containing the LLM response
        """
        payload = {
            "message": message,
        }
        
        if context_chunks:
            payload["context"] = "\n\n".join(context_chunks)
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {"status": "error", "message": f"API error: {str(e)}"}
            except Exception as e:
                return {"status": "error", "message": f"Connection error: {str(e)}"}