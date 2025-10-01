import asyncio
from src.services.document_service import DocumentService
from src.services.ciit_flow_api import CIITFlowAPIService

async def initialize_system():
    """
    Initialize the RAG system and test the CI&T Flow API connection
    """
    print("Initializing RAG system...")
    
    # Initialize document service and process documents
    doc_service = DocumentService()
    rag_status = doc_service.setup_rag_system()
    print(f"RAG system initialization: {rag_status['status']}")
    print(f"Message: {rag_status['message']}")
    
    # Test CI&T Flow API connection
    print("\nTesting CI&T Flow API connection...")
    api_service = CIITFlowAPIService()
    api_status = await api_service.health_check()
    print(f"API connection: {api_status['status']}")
    print(f"Message: {api_status['message']}")
    
    print("\nInitialization complete!")

if __name__ == "__main__":
    asyncio.run(initialize_system())