# 🐍 Backend - El Sabor Chatbot API

API FastAPI com NLP para processamento de linguagem natural.

## 🚀 Desenvolvimento Local

### Instalar Dependências
```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
```

### Rodar Localmente

bash

```
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse: <http://localhost:8000/docs>

🐳 Docker
---------

bash

```
docker build -t el-sabor-backend .
docker run -p 8000:8000 el-sabor-backend
```

📡 Endpoints
------------

-   `GET /` - Informações da API
-   `GET /health` - Health check
-   `POST /api/chat` - Enviar mensagem para o chatbot
-   `GET /api/intents` - Listar intenções
-   `GET /api/history/{session_id}` - Histórico de conversas

🧪 Testar API
-------------

bash

```
curl -X POST "http://localhost:8000/api/chat"\
  -H "Content-Type: application/json"\
  -d '{"message": "Olá, quero um burrito"}'
```