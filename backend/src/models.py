"""
Modelos do banco de dados
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Intent(Base):
    """Modelo de Intenção"""
    __tablename__ = "intents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    patterns = relationship("Pattern", back_populates="intent", cascade="all, delete-orphan")
    responses = relationship("Response", back_populates="intent", cascade="all, delete-orphan")


class Pattern(Base):
    """Padrões de texto para cada intenção"""
    __tablename__ = "patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    intent_id = Column(Integer, ForeignKey("intents.id"), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    intent = relationship("Intent", back_populates="patterns")


class Response(Base):
    """Respostas para cada intenção"""
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True)
    intent_id = Column(Integer, ForeignKey("intents.id"), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    intent = relationship("Intent", back_populates="responses")


class Conversation(Base):
    """Histórico de conversas"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), nullable=False, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    detected_intent = Column(String(100))
    confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())