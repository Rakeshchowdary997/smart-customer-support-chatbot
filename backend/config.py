import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/chatbot_db')
    SQLALCHEMY_ECHO: bool = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    
    # Redis
    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # NLP Models
    SPACY_MODEL: str = os.getenv('SPACY_MODEL', 'en_core_web_sm')
    TRANSFORMER_MODEL: str = os.getenv('TRANSFORMER_MODEL', 'bert-base-uncased')
    SENTENCE_TRANSFORMER_MODEL: str = os.getenv('SENTENCE_TRANSFORMER_MODEL', 'all-MiniLM-L6-v2')
    
    # Vector Database
    FAISS_INDEX_PATH: str = os.getenv('FAISS_INDEX_PATH', './models/faiss_index')
    USE_PINECONE: bool = os.getenv('USE_PINECONE', 'False').lower() == 'true'
    PINECONE_API_KEY: str = os.getenv('PINECONE_API_KEY', '')
    PINECONE_ENVIRONMENT: str = os.getenv('PINECONE_ENVIRONMENT', 'gcp-starter')
    PINECONE_INDEX_NAME: str = os.getenv('PINECONE_INDEX_NAME', 'chatbot-kb')
    
    # LLM Integration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    LLM_MODEL: str = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
    LLM_TEMPERATURE: float = float(os.getenv('LLM_TEMPERATURE', '0.7'))
    LLM_MAX_TOKENS: int = int(os.getenv('LLM_MAX_TOKENS', '500'))
    
    # Server Configuration
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8000'))
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'info')
    
    # CORS
    ALLOWED_ORIGINS: list = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:8000').split(',')
    
    # JWT/Auth
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key-here')
    ALGORITHM: str = os.getenv('ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    
    # Agent Configuration
    ESCALATION_CONFIDENCE_THRESHOLD: float = float(os.getenv('ESCALATION_CONFIDENCE_THRESHOLD', '0.5'))
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    TIMEOUT_SECONDS: int = int(os.getenv('TIMEOUT_SECONDS', '30'))
    
    # Knowledge Base
    KB_SIMILARITY_THRESHOLD: float = float(os.getenv('KB_SIMILARITY_THRESHOLD', '0.7'))
    KB_TOP_K_RESULTS: int = int(os.getenv('KB_TOP_K_RESULTS', '5'))
    
    class Config:
        case_sensitive = True

settings = Settings()
