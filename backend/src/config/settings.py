import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file
    """
    # CI&T Flow API settings
    FLOW_API_TOKEN: str = os.getenv("FLOW_API_TOKEN", "")
    FLOW_API_BASE_URL: str = os.getenv("FLOW_API_BASE_URL", "https://flow.ciandt.com/ai-orchestration-api/v1/openai")
    FLOW_AGENT: str = os.getenv("FLOW_AGENT", "Flow Api")
    FLOW_TENANT: str = os.getenv("FLOW_TENANT", "")
    FLOW_MODEL: str = os.getenv("FLOW_MODEL", "gpt-4o-mini")
    
    # Flow Auth settings
    FLOW_CLIENT_ID: str = os.getenv("FLOW_CLIENT_ID", "")
    FLOW_CLIENT_SECRET: str = os.getenv("FLOW_CLIENT_SECRET", "")
    
    # RAG settings
    RAG_DOCUMENTS_FOLDER: str = os.getenv("RAG_DOCUMENTS_FOLDER", "docs")
    
    # Vector store settings
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "vector_store")
    
    # Model settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Use ConfigDict instead of class Config
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

# Create settings instance
settings = Settings()