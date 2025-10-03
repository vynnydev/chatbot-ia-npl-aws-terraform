"""
FastAPI Application - El Sabor Chatbot
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import json
import random
import uuid
import redis

from .config import get_settings
from .database import get_db, engine, Base
from .models import Intent, Pattern, Response, Conversation
from .schemas import MessageRequest, MessageResponse, HealthResponse, IntentResult
from .nlp_processor import nlp_processor

# Settings
settings = get_settings()

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API do Chatbot El Sabor - Restaurante Mexicano"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis client
try:
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    redis_available = True
except Exception as e:
    print(f"Redis não disponível: {e}")
    redis_client = None
    redis_available = False


@app.on_event("startup")
async def startup_event():
    """Inicializa o chatbot ao iniciar a aplicação"""
    print("🚀 Iniciando El Sabor Chatbot API...")
    
    # Carregar intents do arquivo JSON
    try:
        with open("data/intents.json", "r", encoding="utf-8") as f:
            intents_data = json.load(f)
        
        nlp_processor.load_intents(intents_data)
        print(f"✅ {len(intents_data)} intenções carregadas com sucesso!")
        
    except FileNotFoundError:
        print("⚠️ Arquivo intents.json não encontrado!")
    except Exception as e:
        print(f"❌ Erro ao carregar intents: {e}")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "El Sabor Chatbot API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    
    # Check database
    db_status = "ok"
    try:
        db.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check Redis
    redis_status = "ok" if redis_available else "unavailable"
    if redis_available:
        try:
            redis_client.ping()
        except Exception as e:
            redis_status = f"error: {str(e)}"
    
    return HealthResponse(
        status="healthy" if db_status == "ok" else "unhealthy",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        database=db_status,
        redis=redis_status
    )


@app.post("/api/chat", response_model=MessageResponse, tags=["Chat"])
async def chat(
    request: MessageRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint principal do chat
    
    Processa mensagem do usuário e retorna resposta com intenções detectadas
    """
    
    # Gerar session_id se não fornecido
    session_id = request.session_id or str(uuid.uuid4())
    
    # Validar mensagem
    if not request.message or len(request.message.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mensagem não pode ser vazia"
        )
    
    try:
        # Dividir mensagem em múltiplas intenções se necessário
        segments = nlp_processor.split_multiple_intents(request.message)
        
        # Detectar intenções para cada segmento
        all_intents = []
        for segment in segments:
            detected = nlp_processor.detect_intent(segment, top_k=2)
            all_intents.extend(detected)
        
        # Remover duplicatas mantendo maior confiança
        unique_intents = {}
        for intent_name, confidence in all_intents:
            if intent_name not in unique_intents or confidence > unique_intents[intent_name]:
                unique_intents[intent_name] = confidence
        
        # Converter para lista de IntentResult
        intent_results = [
            IntentResult(intent=name, confidence=conf)
            for name, conf in sorted(unique_intents.items(), key=lambda x: x[1], reverse=True)
        ]
        
        # Pegar intent principal
        main_intent = intent_results[0].intent if intent_results else "unknown"
        main_confidence = intent_results[0].confidence if intent_results else 0.0
        
        # Buscar resposta
        response_text = get_response(main_intent)
        
        # Salvar no histórico
        conversation = Conversation(
            session_id=session_id,
            user_message=request.message,
            bot_response=response_text,
            detected_intent=main_intent,
            confidence=main_confidence
        )
        db.add(conversation)
        db.commit()
        
        # Salvar no Redis (cache de sessão)
        if redis_available:
            try:
                redis_client.setex(
                    f"session:{session_id}",
                    3600,  # 1 hora
                    json.dumps({
                        "last_message": request.message,
                        "last_intent": main_intent,
                        "timestamp": datetime.now().isoformat()
                    })
                )
            except Exception as e:
                print(f"Redis error: {e}")
        
        return MessageResponse(
            response=response_text,
            intents=intent_results[:3],  # Top 3 intents
            session_id=session_id,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        print(f"Error processing message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar mensagem: {str(e)}"
        )


def get_response(intent: str) -> str:
    """
    Retorna resposta para a intenção detectada
    
    Args:
        intent: Nome da intenção
        
    Returns:
        Texto da resposta
    """
    try:
        with open("data/intents.json", "r", encoding="utf-8") as f:
            intents_data = json.load(f)
        
        if intent in intents_data:
            responses = intents_data[intent].get("responses", [])
            if responses:
                return random.choice(responses)
        
        # Fallback
        return "Desculpa, não entendi. Pode reformular? 😊"
        
    except Exception as e:
        print(f"Error getting response: {e}")
        return "Ops! Tive um problema. Pode tentar novamente?"


@app.get("/api/intents", tags=["Intents"])
async def list_intents():
    """Lista todas as intenções disponíveis"""
    try:
        with open("data/intents.json", "r", encoding="utf-8") as f:
            intents_data = json.load(f)
        
        return {
            "total": len(intents_data),
            "intents": list(intents_data.keys())
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/api/history/{session_id}", tags=["History"])
async def get_history(session_id: str, db: Session = Depends(get_db)):
    """Retorna histórico de conversas de uma sessão"""
    conversations = db.query(Conversation)\
        .filter(Conversation.session_id == session_id)\
        .order_by(Conversation.created_at.desc())\
        .limit(50)\
        .all()
    
    return {
        "session_id": session_id,
        "total": len(conversations),
        "conversations": [
            {
                "user_message": c.user_message,
                "bot_response": c.bot_response,
                "intent": c.detected_intent,
                "confidence": c.confidence,
                "timestamp": c.created_at
            }
            for c in conversations
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)