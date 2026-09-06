# Autonomous Research Lab

Milestone 1 foundation for a modular scientific research platform. It includes a FastAPI backend with Clean Architecture boundaries, async PostgreSQL persistence, Redis, Alembic, and a React dashboard.

## Docker quick start

Copy the example environment file before starting the stack:

```bash
cp .env.example .env
docker compose up --build
```

On Windows PowerShell, use `Copy-Item .env.example .env` instead. The Compose file also supplies safe development defaults when `.env` is absent.

Open http://localhost:5173. API docs are at http://localhost:8000/docs. PostgreSQL data is persisted in the named `postgres_data` volume, and migrations run automatically when the backend starts after PostgreSQL is healthy.

Stop the services with `docker compose down`. To remove the persisted database as well, run `docker compose down -v`.

## Architecture

HTTP concerns live in `app/api`, orchestration in `app/services`, persistence in `app/repositories`, and SQLAlchemy models in `app/models`. Configuration, errors, middleware, and authentication seams are isolated. Research agents are intentionally not implemented in this milestone.
