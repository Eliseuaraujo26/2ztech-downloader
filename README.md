# 2ZTech Downloader

**Gerenciador profissional de downloads em massa**  
Desenvolvido por **Eliseu Araújo | 2ZTech**

Sistema robusto, modular e pronto para produção para gerenciar filas de download com interface web, workers assíncronos, autenticação, retry inteligente e armazenamento abstrato.

---

## Stack

| Camada        | Tecnologia                          |
|---------------|-------------------------------------|
| Frontend      | React 18 + TypeScript + Vite + Tailwind |
| Backend       | Python 3.12 + FastAPI + Pydantic    |
| Banco         | PostgreSQL 16 + SQLAlchemy async    |
| Fila / Cache  | Redis 7                             |
| Workers       | Processo async próprio (escalável)  |
| Container     | Docker + Docker Compose             |

---

## Arquitetura

```
Frontend → API (FastAPI) → Job Manager → Redis Queue → Workers → Adapters → Storage
```

- Cada download é um **Job** com máquina de estados formal.
- Workers podem ser escalados horizontalmente.
- Adaptadores isolados permitem adicionar novas fontes sem alterar o core.
- Storage abstrato (Local hoje; S3/GCS prontos para extensão).

---

## Requisitos

- Docker + Docker Compose
- (Opcional) Node 20+ e Python 3.12 para desenvolvimento local sem containers

---

## Início rápido (Docker)

```bash
# 1. Clone / entre na pasta
cd 2ztech-downloader

# 2. Configure o ambiente
cp .env.example .env
# Edite APP_SECRET_KEY e JWT_SECRET_KEY (mínimo 32 caracteres)

# 3. Suba tudo
docker compose up -d --build

# 4. Acesse
# Frontend: http://localhost:5173
# API Docs:  http://localhost:8000/docs
# Health:    http://localhost:8000/api/health
```

Primeiro acesso: registre um usuário em `/register`.

---

## Colocar online (produção)

### Opção recomendada: Railway.app ou Render.com

1. Crie conta em [railway.app](https://railway.app) ou [render.com](https://render.com)
2. Conecte o repositório GitHub `Eliseuaraujo26/2ztech-downloader`
3. Adicione serviços: PostgreSQL + Redis + Backend + Worker + Frontend
4. Configure as variáveis de ambiente (copie de `.env.example` e gere secrets fortes)
5. Defina o comando do backend: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Worker: `python -m app.workers.runner`

### Opção VPS (DigitalOcean, Hetzner, AWS Lightsail)

```bash
git clone https://github.com/Eliseuaraujo26/2ztech-downloader.git
cd 2ztech-downloader
cp .env.example .env
# Edite secrets e APP_URL / FRONTEND_URL para o domínio público
docker compose up -d --build
```

Use um reverse proxy (Caddy ou Nginx) com HTTPS (Let's Encrypt).

---

## Variáveis de ambiente principais

Veja `.env.example`. Destaques:

- `MAX_WORKERS` — concorrência de downloads (padrão 5)
- `MAX_RETRIES` — tentativas com backoff
- `STORAGE_LOCAL_ROOT` — pasta de downloads
- `SSRF_BLOCK_PRIVATE_IPS` — proteção SSRF (recomendado `true`)

---

## Comandos úteis

```bash
docker compose logs -f backend
docker compose logs -f worker
docker compose exec backend alembic upgrade head
docker compose exec backend pytest -v
docker compose down
```

---

## API

Documentação interativa: `/docs` (OpenAPI).

| Método | Endpoint                    | Descrição              |
|--------|-----------------------------|------------------------|
| POST   | /api/auth/register          | Cadastro               |
| POST   | /api/auth/login             | Login (JWT)            |
| POST   | /api/jobs                   | Criar job              |
| POST   | /api/jobs/bulk              | Importação em massa    |
| GET    | /api/jobs                   | Listar (filtros)       |
| POST   | /api/jobs/{id}/pause        | Pausar                 |
| POST   | /api/jobs/{id}/resume       | Retomar                |
| POST   | /api/jobs/{id}/cancel       | Cancelar               |
| POST   | /api/jobs/{id}/retry        | Retry                  |
| GET    | /api/dashboard              | Estatísticas           |
| GET    | /api/health                 | Health check           |

---

## Segurança

- Validação de URL + proteção SSRF
- JWT com access + refresh token
- Roles ADMIN / USER
- Sanitização de nomes de arquivo
- Secrets via `.env`

---

**2ZTech Downloader** — base de produto profissional  
Eliseu Araújo | 2ZTech
