# ⚙️ Setup

## Requisitos

- Docker
- Docker Compose

## Instalación

1. Clona el repositorio
\```bash
git clone <url>
cd backend
\```

2. Crea tu `.env` basado en `.env.example`
\```bash
cp .env.example .env
\```

3. Completa las variables en tu `.env`
\```bash
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DB=tienda_db
DATABASE_URL=postgresql://admin:admin123@db:5432/tienda_db
\```

4. Levanta el proyecto
\```bash
docker compose up --build
\```

5. Abre la documentación
\```
http://localhost:8000/docs
\```

## Comandos útiles

\```bash
# Levantar en background
docker compose up -d

# Ver logs
docker compose logs -f

# Detener contenedores
docker compose down

# Reconstruir imagen
docker compose up --build
\```