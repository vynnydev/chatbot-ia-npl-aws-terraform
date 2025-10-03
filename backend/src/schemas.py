"""
Schemas Pydantic para validação
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MessageRequest(BaseModel):
    """Request de mensagem do usuário"""
    message: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = None


class IntentResult(BaseModel):
    """Resultado de detecção de intenção"""
    intent: str
    confidence: float
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Response do chatbot"""
    response: str
    intents: List[IntentResult]
    session_id: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    environment: str
    database: str
    redis: str


class IntentCreate(BaseModel):
    """Schema para criar intenção"""
    name: str
    description: Optional[str] = None
    patterns: List[str]
    responses: List[str]


class IntentResponse(BaseModel):
    """Schema de resposta de intenção"""
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True