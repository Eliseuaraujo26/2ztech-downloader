# Deploy 2ZTech Downloader no Railway

Guia passo a passo para subir a **versao completa** (API + Worker + PostgreSQL + Redis).

## Pre-requisitos

1. Conta em https://railway.app (login com GitHub)
2. Repositorio: https://github.com/Eliseuaraujo26/2ztech-downloader

---

## Passo 1 - Novo projeto

1. Acesse https://railway.app/new
2. Escolha **Deploy from GitHub repo**
3. Autorize o Railway e selecione `Eliseuaraujo26/2ztech-downloader`

---

## Passo 2 - PostgreSQL

1. No projeto: **+ New** -> **Database** -> **PostgreSQL**
2. Aguarde provisionar

---

## Passo 3 - Redis

1. **+ New** -> **Database** -> **Redis**

---

## Passo 4 - Backend (API)

1. **+ New** -> **GitHub Repo** -> mesmo repositorio
2. Settings:
   - **Root Directory:** `backend`
3. **Start Command:**
   ```
   alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. **Variables:**

```
APP_NAME=2ZTech Downloader
APP_ENV=production
APP_DEBUG=false
APP_SECRET_KEY=<string-aleatoria-32+-chars>
JWT_SECRET_KEY=<outra-string-aleatoria-32+-chars>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
MAX_WORKERS=5
MAX_RETRIES=3
STORAGE_BACKEND=local
STORAGE_LOCAL_ROOT=/app/downloads
SSRF_BLOCK_PRIVATE_IPS=true
ALLOWED_URL_SCHEMES=http,https
LOG_LEVEL=INFO
LOG_FORMAT=json
```

5. DATABASE_URL: copie a URL do Postgres e troque `postgresql://` por `postgresql+asyncpg://`
6. REDIS_URL: referencie o Redis
7. **Networking** -> **Generate Domain**

---

## Passo 5 - Worker

1. **+ New** -> **GitHub Repo** -> mesmo repo
2. Root Directory: `backend`
3. Start Command: `python -m app.workers.runner`
4. Copie as mesmas variaveis do backend

---

## Passo 6 - Frontend

Use Vercel apontando VITE_API_URL para a URL da API no Railway, ou outro servico no Railway com root `frontend`.

No backend defina:
```
ALLOWED_ORIGINS=https://seu-frontend.vercel.app
APP_URL=https://sua-api.up.railway.app
FRONTEND_URL=https://seu-frontend.vercel.app
```

---

## Passo 7 - Volume

No backend e worker: monte volume em `/app/downloads` para persistir arquivos.

---

## Testar

- Health: `https://sua-api.up.railway.app/api/health`
- Docs: `https://sua-api.up.railway.app/docs`

## Servicos

| Servico    | Root    | Start |
|------------|---------|-------|
| PostgreSQL | -       | plugin |
| Redis      | -       | plugin |
| backend    | backend | alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT |
| worker     | backend | python -m app.workers.runner |

**2ZTech Downloader** - Eliseu Araujo | 2ZTech
