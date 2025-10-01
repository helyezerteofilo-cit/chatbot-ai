import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file
    """
    # CI&T Flow API settings
    CIIT_FLOW_API_TOKEN: str = os.getenv("CIIT_FLOW_API_TOKEN", "")
    CIIT_FLOW_API_BASE_URL: str = os.getenv("CIIT_FLOW_API_BASE_URL", "https://api.flow.ciit.ai")
    
    # RAG settings
    RAG_DOCUMENTS_FOLDER: str = os.getenv("RAG_DOCUMENTS_FOLDER", "docs")
    
    # Vector store settings
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "vector_store")
    
    # Model settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()