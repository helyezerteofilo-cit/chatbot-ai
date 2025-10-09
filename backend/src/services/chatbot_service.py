from typing import Dict, Any, List
from src.services.flow_api import FlowAPIService
from src.services.document import DocumentService

class ChatbotService:
    """
    Service to handle chatbot interactions using RAG and CI&T Flow API
    """
    def __init__(self):
        self.flow_api = FlowAPIService()
        self.document_service = DocumentService()
    
    async def setup(self) -> Dict[str, Any]:
        """
        Set up the chatbot service
        
        Returns:
            Status dictionary
        """
        rag_status = self.document_service.setup_rag_system()
        
        return {
            "rag_status": rag_status,
        }
    
    async def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process a user message using RAG and CI&T Flow API
        
        Args:
            message: The user's message
            
        Returns:
            Response dictionary
        """
        try:
            relevant_docs = self.document_service.query_vector_store(message)
            
            context_chunks = [doc.page_content for doc in relevant_docs]
            
            response = await self.flow_api.generate_response(message, context_chunks)
            
            if response.get("status") == "success":
                response["context"] = {
                    "num_docs_retrieved": len(relevant_docs),
                    "sources": [
                        {"source": doc.metadata.get("source", "Unknown"), 
                         "page": doc.metadata.get("page", 0) if "page" in doc.metadata else None}
                        for doc in relevant_docs
                    ]
                }
            
            return response
        except Exception as e:
            return {"status": "error", "message": f"Error processing message: {str(e)}"}