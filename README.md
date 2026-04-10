# 🛒 Tienda API

Backend REST API construida progresivamente como proyecto de aprendizaje hacia un stack production-ready.

El objetivo es construir un backend completo desde cero, agregando capas de complejidad de forma incremental: desde un CRUD básico hasta un sistema con auth, cache, tests, CI/CD y monitoreo.

## 🚀 Tech Stack actual

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Containerization:** Docker + Docker Compose
- **Validation:** Pydantic

## 🗺️ Roadmap

### ✅ Fase 1 — Base
- [x] FastAPI + Docker + PostgreSQL
- [x] CRUD Productos

### 🔄 Fase 2 — Entidades
- [x] CRUD Clientes
- [ ] CRUD Vendedores
- [ ] Relaciones entre entidades
- [ ] Migraciones con Alembic

### 🔄 Fase 3 — Auth & Seguridad
- [ ] JWT Authentication
- [ ] Register / Login
- [ ] Refresh tokens
- [ ] Roles y permisos (RBAC)
- [ ] Hash de contraseñas con bcrypt
- [ ] Protección de endpoints por rol
- [ ] CORS configurado correctamente
- [ ] Variables de entorno seguras
- [ ] HTTPS / SSL

### 🔄 Fase 4 — Rate Limiting & Protección
- [ ] Rate limiting por IP
- [ ] Rate limiting por usuario
- [ ] Protección contra fuerza bruta en login
- [ ] Blacklist de tokens JWT
- [ ] Sanitización de inputs
- [ ] Protección contra SQL Injection
- [ ] Headers de seguridad (Helmet equivalent)
- [ ] CSRF Protection

### 🔄 Fase 5 — Performance & Cache
- [ ] Redis Cache
- [ ] Cache de queries frecuentes
- [ ] Paginación
- [ ] Filtros y búsqueda
- [ ] Ordenamiento
- [ ] Query optimization
- [ ] Connection pooling

### 🔄 Fase 6 — Testing
- [ ] Unit tests con Pytest
- [ ] Integration tests
- [ ] Test de endpoints
- [ ] Mocking de base de datos
- [ ] Coverage reports
- [ ] Test en CI/CD pipeline

### 🔄 Fase 7 — DevOps & CI/CD
- [ ] GitHub Actions pipeline
- [ ] Lint automático (flake8, black)
- [ ] Tests automáticos en cada PR
- [ ] Environments separados (dev, staging, prod)
- [ ] Docker multi-stage builds
- [ ] Secrets management
- [ ] Automated deployments

### 🔄 Fase 8 — Infraestructura
- [ ] Nginx como reverse proxy
- [ ] Gunicorn + Uvicorn en producción
- [ ] SSL con Certbot
- [ ] Deploy en VPS
- [ ] Docker Compose para producción
- [ ] Backups automáticos de base de datos
- [ ] Health checks

### 🔄 Fase 9 — Observabilidad
- [ ] Logging estructurado
- [ ] Prometheus + Grafana
- [ ] ELK Stack (Elasticsearch, Logstash, Kibana)
- [ ] Alertas automáticas
- [ ] Tracing de requests
- [ ] Métricas de performance

### 🔄 Fase 10 — Buenas Prácticas
- [ ] Conventional Commits
- [ ] Branching strategy (Gitflow)
- [ ] Pull Request templates
- [ ] Code review process
- [ ] Documentación de API con ejemplos
- [ ] Versionado de API (v1, v2)
- [ ] Manejo global de errores
- [ ] Respuestas estandarizadas