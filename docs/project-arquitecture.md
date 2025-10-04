```
chatbot-ia-npl-aws-terraform/
│
├── 📁 infraestruture/                           # INFRAESTRUTURA COMO CÓDIGO
│   │
│   ├── backend.tf                          # Configuração do backend remoto S3 + DynamoDB
│   ├── main.tf                             # Orquestração dos módulos (chama todos os módulos)
│   ├── variables.tf                        # Declaração de todas as variáveis do projeto
│   ├── outputs.tf                          # Outputs importantes (URLs, endpoints)
│   ├── terraform.tfvars.example            # Exemplo de configuração (copiar para .tfvars)
│   ├── terraform.tfvars                    # Valores reais das variáveis (GIT IGNORE!)
│   │
│   └── 📁 modules/                         # MÓDULOS TERRAFORM REUTILIZÁVEIS
│       │
│       ├── 📁 networking/                  # VPC, Subnets, NAT, IGW
│       │   ├── main.tf                     # Recursos de rede (VPC, subnets, route tables)
│       │   ├── variables.tf                # Variáveis do módulo networking
│       │   └── outputs.tf                  # Outputs (VPC ID, subnet IDs)
│       │
│       ├── 📁 ecr/                         # Container Registry
│       │   ├── main.tf                     # Repositórios ECR para backend/frontend
│       │   ├── variables.tf                # Variáveis do ECR
│       │   └── outputs.tf                  # URLs dos repositórios
│       │
│       ├── 📁 rds/                         # Banco de Dados PostgreSQL
│       │   ├── main.tf                     # RDS instance, subnet group, security group
│       │   ├── variables.tf                # Variáveis (instance type, credenciais)
│       │   └── outputs.tf                  # Endpoint do banco
│       │
│       ├── 📁 elasticache/                 # Cache Redis
│       │   ├── main.tf                     # ElastiCache cluster, subnet group
│       │   ├── variables.tf                # Variáveis do Redis
│       │   └── outputs.tf                  # Endpoint do Redis
│       │
│       ├── 📁 alb/                         # Application Load Balancer
│       │   ├── main.tf                     # ALB, target groups, listeners, rules
│       │   ├── variables.tf                # Variáveis do ALB
│       │   └── outputs.tf                  # DNS do ALB, ARNs dos target groups
│       │
│       └── 📁 ecs/                         # ECS Fargate (Módulo Genérico)
│           ├── main.tf                     # Cluster, task definition, service, auto-scaling
│           ├── variables.tf                # Variáveis (CPU, memória, porta, image)
│           └── outputs.tf                  # Cluster name, service name, security group
│
├── 📁 backend/                             # API BACKEND (FASTAPI + PYTHON)
│   │
│   ├── 📁 src/                             # Código-fonte da aplicação
│   │   ├── main.py                         # Entrypoint da API FastAPI
│   │   ├── nlp_processor.py                # Engine de processamento NLP (spaCy/NLTK)
│   │   ├── intent_classifier.py            # Classificador de intenções (ML)
│   │   ├── models.py                       # Modelos SQLAlchemy (ORM)
│   │   ├── database.py                     # Configuração do banco de dados
│   │   ├── schemas.py                      # Schemas Pydantic (validação)
│   │   ├── routes.py                       # Rotas da API (/chat, /health)
│   │   └── config.py                       # Configurações e variáveis de ambiente
│   │
│   ├── 📁 data/                            # Dados de treinamento
│   │   └── intents.json                    # Intenções, patterns e respostas (15+ por intent)
│   │
│   ├── 📁 tests/                           # Testes unitários
│   │   ├── test_nlp.py                     # Testes do NLP
│   │   └── test_api.py                     # Testes da API
│   │
│   ├── requirements.txt                    # Dependências Python (FastAPI, spaCy, etc)
│   ├── Dockerfile                          # Imagem Docker do backend
│   ├── .dockerignore                       # Arquivos ignorados no build
│   └── README.md                           # Documentação do backend
│
├── 📁 frontend-web/                        # FRONTEND WEB (NEXT.JS)
│   │
│   ├── 📁 src/                             # Código-fonte
│   │   ├── 📁 app/                         # App Router do Next.js 14
│   │   │   ├── page.tsx                    # Página principal (/)
│   │   │   ├── layout.tsx                  # Layout global
│   │   │   └── globals.css                 # Estilos globais
│   │   │
│   │   └── 📁 components/                  # Componentes React
│   │       ├── ChatInterface.tsx           # Interface principal do chat
│   │       ├── MessageBubble.tsx           # Bolha de mensagem
│   │       ├── IntentDisplay.tsx           # Mostra intent + probabilidade
│   │       └── Header.tsx                  # Cabeçalho
│   │
│   ├── 📁 public/                          # Arquivos estáticos
│   │   ├── logo.svg                        # Logo do El Sabor
│   │   └── favicon.ico                     # Favicon
│   │
│   ├── package.json                        # Dependências Node.js
│   ├── tsconfig.json                       # Configuração TypeScript
│   ├── next.config.js                      # Configuração do Next.js
│   ├── tailwind.config.js                  # Configuração do Tailwind CSS
│   ├── Dockerfile                          # Imagem Docker do frontend
│   ├── .dockerignore                       # Arquivos ignorados
│   └── README.md                           # Documentação do frontend web
│
├── 📁 frontend-mobile/                     # APP MOBILE (REACT NATIVE)
│   │
│   ├── 📁 src/                             # Código-fonte
│   │   ├── 📁 screens/                     # Telas do app
│   │   │   ├── ChatScreen.tsx              # Tela principal do chat
│   │   │   └── HomeScreen.tsx              # Tela inicial
│   │   │
│   │   ├── 📁 components/                  # Componentes
│   │   │   ├── ChatMessage.tsx             # Componente de mensagem
│   │   │   └── InputBar.tsx                # Barra de input
│   │   │
│   │   ├── 📁 services/                    # Serviços
│   │   │   └── api.ts                      # Cliente HTTP (axios)
│   │   │
│   │   └── 📁 navigation/                  # Navegação
│   │       └── AppNavigator.tsx            # Navegação do app
│   │
│   ├── App.tsx                             # Componente raiz
│   ├── app.json                            # Configuração do Expo
│   ├── package.json                        # Dependências
│   ├── tsconfig.json                       # TypeScript config
│   └── README.md                           # Documentação do app mobile
│
├── 📁 scripts/                             # SCRIPTS AUXILIARES
│   ├── deploy.sh                           # Script completo de deploy (build + push + update ECS)
│   ├── destroy.sh                          # Script seguro para destruir infraestrutura
│   └── validate.sh                         # Valida pré-requisitos antes do deploy
│
├── 📁 docs/                                # DOCUMENTAÇÃO ADICIONAL
│   ├── ARCHITECTURE.md                     # Arquitetura detalhada com diagramas
│   ├── architecture-diagram.drawio.xml     # Diagrama editável no Draw.io
│   └── API.md                              # Documentação da API (endpoints)
│
├── 📁 .github/                             # CI/CD (OPCIONAL)
│   └── 📁 workflows/
│       ├── deploy.yml                      # GitHub Actions para deploy automático
│       └── terraform.yml                   # Validação do Terraform no PR
│
├── Makefile                                # Comandos make (init, apply, deploy, logs)
├── .gitignore                              # Arquivos ignorados pelo Git
├── README.md                               # Documentação principal do projeto
├── QUICKSTART.md                           # Guia de início rápido (5 min deploy)
└── LICENSE                                 # Licença do projeto (MIT, GPL, etc)
```