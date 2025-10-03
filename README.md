# 🌮 Chatbot IA para Restaurante Mexicano

<div align="center">

![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![React Native](https://img.shields.io/badge/React_Native-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)

**Chatbot inteligente com NLP para automatizar pedidos em restaurante mexicano**

[📚 Documentação](#-documentação) - [🚀 Deploy Rápido](#-deploy-rápido) - [🏗️ Arquitetura](#️-arquitetura) - [📸 Screenshots](#-screenshots)

</div>

---

## 📋 Sobre o Projeto

Sistema completo de chatbot com **Processamento de Linguagem Natural (NLP)** desenvolvido para atender pedidos em um restaurante mexicano moderno chamado **"El Sabor"**.

O projeto demonstra uma arquitetura **cloud-native serverless** completa utilizando AWS ECS Fargate, RDS PostgreSQL, ElastiCache Redis e **Infrastructure as Code (IaC)** com Terraform.

### ✨ Funcionalidades Principais

- 🤖 **NLP Avançado**: Processamento de linguagem natural com spaCy/NLTK
- 🎯 **Múltiplas Intenções**: Detecta várias intenções em uma única mensagem
- 📊 **Confiabilidade**: Exibe probabilidade de acerto para cada intent detectada
- 🌐 **Interface Web**: Frontend responsivo desenvolvido em Next.js
- 📱 **App Mobile**: Aplicativo nativo com React Native + Expo
- ☁️ **Deploy Automatizado**: Infraestrutura provisionada com Terraform
- 📈 **Observabilidade**: Monitoramento completo com CloudWatch
- 🔄 **Auto Scaling**: Escala automática baseada em CPU/memória
- 🔒 **Segurança**: VPC isolada, encryption at rest, security groups

### 🎯 Intenções Suportadas

O chatbot reconhece as seguintes intenções:

| Intenção | Exemplos | Respostas |
|----------|----------|-----------|
| **Compra** | "Quero um burrito", "Me vê dois tacos" | Confirmação de pedido |
| **Cardápio** | "Quais pratos vocês têm?", "Me mostra o menu" | Lista de itens disponíveis |
| **Preço** | "Quanto custa?", "Qual o valor?" | Informações de preço |
| **Entrega** | "Quanto tempo demora?", "Quando chega?" | Tempo estimado |
| **Agradecimento** | "Obrigado!", "Valeu!" | Mensagem de cortesia |
| **Reclamação** | "Pedido atrasado", "Veio errado" | Tratamento de problema |
| **Cumprimento** | "Oi", "Bom dia" | Saudação |
| **Despedida** | "Tchau", "Até logo" | Finalização |

Cada intenção possui **15+ frases de treinamento** e **4+ respostas variadas**.

---

## 🏗️ Arquitetura

### Stack Tecnológico

#### **Backend**
- **FastAPI**: Framework web assíncrono e performático
- **Python 3.11**: Linguagem principal
- **spaCy / NLTK**: Bibliotecas de NLP
- **scikit-learn**: Machine learning para classificação
- **SQLAlchemy**: ORM para PostgreSQL
- **Redis**: Cache de sessões

#### **Frontend Web**
- **Next.js 14**: Framework React com SSR
- **TypeScript**: Tipagem estática
- **Tailwind CSS**: Estilização
- **Axios**: Requisições HTTP

#### **Frontend Mobile**
- **React Native**: Framework mobile
- **Expo**: Toolchain e APIs nativas
- **React Navigation**: Navegação

#### **Infraestrutura AWS**
- **ECS Fargate**: Containers serverless
- **RDS PostgreSQL 15.4**: Banco de dados relacional
- **ElastiCache Redis 7.0**: Cache em memória
- **Application Load Balancer**: Balanceamento de carga
- **Amazon ECR**: Registro de containers
- **VPC**: Rede privada virtual
- **CloudWatch**: Logs e métricas
- **Terraform 1.5+**: Infrastructure as Code

### Diagrama de Arquitetura
```

┌─────────────────────────────────────────────────────────────┐ │ Internet Gateway │ └──────────────────────┬──────────────────────────────────────┘ │ ┌──────────────────────▼──────────────────────────────────────┐ │ Application Load Balancer (ALB) │ │ ┌──────────────┐ ┌──────────────┐ │ │ │ Frontend │ │ Backend │ │ │ │ (Next.js) │ │ (FastAPI) │ │ │ └──────────────┘ └──────────────┘ │ └─────────────────────────────────────────────────────────────┘ │ ┌──────────────┼──────────────┐ │ │ │ ┌───────▼──────┐ ┌────▼──────┐ ┌────▼──────────┐ │ ECS Fargate │ │ ECS Fargate│ │ ElastiCache │ │ Frontend │ │ Backend │ │ (Redis) │ │ Tasks │ │ Tasks │ └──────────────┘ └──────────────┘ └────┬───────┘ │ ┌─────▼──────┐ │ RDS │ │ PostgreSQL │ └────────────┘

```

📐 **[Diagrama completo em Draw.io](./docs/architecture-diagram.drawio.xml)**

### Componentes

- **VPC**: 10.0.0.0/16 com subnets públicas e privadas em 2 AZs
- **ALB**: Roteamento inteligente para frontend (/) e backend (/api/*)
- **ECS**: 2 clusters (frontend + backend) com auto-scaling
- **RDS**: PostgreSQL t3.micro com backups automáticos
- **Redis**: ElastiCache t3.micro para sessões
- **ECR**: 2 repositórios para imagens Docker

---

## 🚀 Deploy Rápido

### Pré-requisitos

- [AWS CLI](https://aws.amazon.com/cli/) configurado
- [Terraform](https://www.terraform.io/downloads) >= 1.5
- [Docker](https://www.docker.com/get-started)
- [Make](https://www.gnu.org/software/make/) (opcional)

### Passo 1: Clone o Repositório
```bash
git clone https://github.com/seu-usuario/chatbot-ia-npl-aws-terraform.git
cd chatbot-ia-npl-aws-terraform
```

### Passo 2: Configure AWS

bash

```
aws configure
# AWS Access Key ID: [sua-key]
# AWS Secret Access Key: [seu-secret]
# Default region: us-east-1
# Default output format: json
```

### Passo 3: Configure Variáveis

bash

```
cd terraform
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars
```

**IMPORTANTE**: Altere a senha do banco de dados em `db_password`!

### Passo 4: Valide a Configuração

bash

```
chmod +x scripts/validate.sh
./scripts/validate.sh
```

### Passo 5: Deploy da Infraestrutura

bash

```
# Criar backend do Terraform (primeira vez apenas)
make setup-backend

# Descomente o bloco backend "s3" em terraform/backend.tf

# Inicializar e aplicar
make init
make plan
make apply
```

⏱️ **Tempo estimado**: 10-15 minutos

### Passo 6: Deploy das Aplicações

bash

```
# Build e push das imagens Docker
make deploy

# Aguarde 3-5 minutos para os containers iniciarem
```

### Passo 7: Acesse a Aplicação

bash

```
# Obter URL do Load Balancer
make output | grep alb_url

# URL exemplo: http://el-sabor-prod-alb-123456789.us-east-1.elb.amazonaws.com
```

**Pronto!** 🎉 Sua aplicação está no ar!

* * * * *

📚 Documentação
---------------

### Estrutura do Projeto

```
chatbot-ia-npl-aws-terraform/
├── terraform/                    # Infraestrutura como código
│   ├── main.tf                  # Configuração principal
│   ├── variables.tf             # Variáveis
│   ├── outputs.tf               # Outputs
│   ├── backend.tf               # Remote state
│   └── modules/                 # Módulos Terraform
│       ├── networking/          # VPC, subnets, NAT
│       ├── ecr/                 # Container registry
│       ├── rds/                 # PostgreSQL database
│       ├── elasticache/         # Redis cache
│       ├── alb/                 # Load balancer
│       └── ecs/                 # ECS Fargate
├── backend/                     # API Backend (FastAPI)
│   ├── src/
│   │   ├── main.py             # Entrypoint
│   │   ├── nlp_processor.py    # NLP engine
│   │   └── models.py           # Database models
│   ├── data/
│   │   └── intents.json        # Intenções e respostas
│   ├── requirements.txt
│   └── Dockerfile
├── frontend-web/                # Frontend Web (Next.js)
│   ├── src/
│   │   ├── app/
│   │   └── components/
│   ├── package.json
│   └── Dockerfile
├── frontend-mobile/             # App Mobile (React Native)
│   ├── src/
│   ├── app.json
│   └── package.json
├── scripts/                     # Scripts auxiliares
│   ├── deploy.sh               # Deploy automatizado
│   ├── destroy.sh              # Destruir infraestrutura
│   └── validate.sh             # Validar configuração
├── docs/                        # Documentação adicional
│   ├── ARCHITECTURE.md         # Arquitetura detalhada
│   └── architecture-diagram.drawio.xml
├── Makefile                     # Comandos make
├── .gitignore
├── QUICKSTART.md               # Guia rápido
└── README.md                   # Este arquivo
```

### Documentos Importantes

-   📖 [Guia de Início Rápido](./QUICKSTART.md)
-   🏗️ [Arquitetura Detalhada](./docs/ARCHITECTURE.md)
-   🔧 [Troubleshooting](#-troubleshooting)

* * * * *

🛠️ Comandos Úteis
------------------

### Terraform

bash

```
make init          # Inicializar Terraform
make plan          # Ver mudanças planejadas
make apply         # Aplicar mudanças
make destroy       # Destruir infraestrutura
make output        # Ver outputs
make format        # Formatar código Terraform
make validate      # Validar configuração
```

### Docker

bash

```
make docker-login           # Login no ECR
make docker-build-backend   # Build imagem backend
make docker-build-frontend  # Build imagem frontend
make docker-push-backend    # Push backend para ECR
make docker-push-frontend   # Push frontend para ECR
make deploy                 # Build + Push + Update ECS
```

### Logs

bash

```
make logs-backend    # Ver logs do backend
make logs-frontend   # Ver logs do frontend
```

* * * * *

🐛 Troubleshooting
------------------

### Problema: "No healthy targets"

bash

```
# Verificar logs do backend
make logs-backend

# Testar health check
curl http://seu-alb-url/api/health

# Verificar tasks rodando
aws ecs list-tasks --cluster el-sabor-prod-backend-cluster
```

### Problema: "Cannot connect to database"

bash

```
# Verificar endpoint do RDS
cd terraform && terraform output rds_endpoint

# Verificar security groups
aws ec2 describe-security-groups --filters "Name=tag:Name,Values=el-sabor-prod-rds-sg"
```

### Problema: "Out of memory"

Edite `terraform/variables.tf` e aumente `backend_memory`:

hcl

```
variable "backend_memory" {
  default = 2048  # Era 1024
}
```

Depois execute `make apply`.

* * * * *

💰 Custos Estimados
-------------------

### Infraestrutura (mensalmente)

-   **NAT Gateway**: ~$32/mês (2 NAT em 2 AZs)
-   **ALB**: ~$22/mês
-   **ECS Fargate**: ~$40/mês (4 tasks rodando 24/7)
-   **RDS t3.micro**: ~$15/mês
-   **ElastiCache t3.micro**: ~$12/mês
-   **ECR**: ~$1/mês
-   **CloudWatch**: ~$5/mês
-   **Data Transfer**: ~$5-10/mês

**Total estimado**: ~$130-140/mês

### Para Reduzir Custos

1.  Use apenas 1 NAT Gateway (-$16/mês)
2.  Reduza `desired_count` para 1 (-$20/mês)
3.  Pare a infraestrutura quando não estiver usando:

bash

```
make destroy  # Destruir tudo
make apply    # Recriar quando precisar
```

* * * * *

📸 Screenshots
--------------

> [Adicione aqui screenshots da interface web e mobile]

* * * * *

🔒 Segurança
------------

-   ✅ VPC isolada com subnets privadas
-   ✅ Security Groups com princípio de menor privilégio
-   ✅ Encryption at rest (RDS + S3)
-   ✅ HTTPS com certificado ACM (opcional)
-   ✅ IAM Roles com permissões mínimas
-   ✅ Secrets via variáveis de ambiente
-   ✅ VPC Flow Logs habilitados
-   ✅ Scan de vulnerabilidades em imagens Docker

* * * * *

🎯 Roadmap
----------

-   [ ]  Implementar AWS WAF no ALB
-   [ ]  Configurar domínio customizado com Route53
-   [ ]  Adicionar AWS Secrets Manager
-   [ ]  Implementar CI/CD com GitHub Actions
-   [ ]  Adicionar testes automatizados
-   [ ]  Implementar Blue/Green deployments
-   [ ]  Adicionar AWS X-Ray para tracing
-   [ ]  Criar CloudWatch Dashboards customizados

* * * * *

👥 Autor
--------

**Seu Nome**

-   🎓 Trabalho Acadêmico - [Nome da Universidade]
-   💼 LinkedIn: [seu-linkedin]
-   📧 Email: [seu-email]
-   🌐 Portfolio: [seu-portfolio]

* * * * *

🙏 Agradecimentos
-----------------

-   [Anthropic Claude](https://www.anthropic.com) - Assistência no desenvolvimento
-   [AWS Documentation](https://docs.aws.amazon.com)
-   [Terraform Registry](https://registry.terraform.io)
-   [FastAPI](https://fastapi.tiangolo.com)
-   [Next.js](https://nextjs.org)

* * * * *

📄 Licença
----------

Este projeto foi desenvolvido para fins **educacionais** como parte de um trabalho acadêmico.