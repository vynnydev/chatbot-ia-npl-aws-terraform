"""
Configurações da aplicação
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações do ambiente"""
    
    # Application
    APP_NAME: str = "El Sabor Chatbot API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Database
    DATABASE_URL: str = "postgresql://admin:password@localhost:5432/elsabor"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # NLP
    SPACY_MODEL: str = "pt_core_news_sm"
    CONFIDENCE_THRESHOLD: float = 0.6
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Retorna singleton das configurações"""
    return Settings()