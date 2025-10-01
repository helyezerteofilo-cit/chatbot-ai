from typing import Dict, Any, List
from src.services.ciit_flow_api import CIITFlowAPIService
from src.services.document_service import DocumentService

class ChatbotService:
    """
    Service to handle chatbot interactions using RAG and CI&T Flow API
    """
    def __init__(self):
        self.ciit_flow_api = CIITFlowAPIService()
        self.document_service = DocumentService()
    
    async def setup(self) -> Dict[str, Any]:
        """
        Set up the chatbot service
        
        Returns:
            Status dictionary
        """
        # Set up RAG system
        rag_status = self.document_service.setup_rag_system()
        
        # Check CI&T Flow API connection
        api_status = await self.ciit_flow_api.health_check()
        
        return {
            "rag_status": rag_status,
            "api_status": api_status
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
            # Retrieve relevant document chunks
            relevant_docs = self.document_service.query_vector_store(message)
            
            # Extract text from documents
            context_chunks = [doc.page_content for doc in relevant_docs]
            
            # Generate response using CI&T Flow API
            response = await self.ciit_flow_api.generate_response(message, context_chunks)
            
            # Add metadata about the retrieved documents
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