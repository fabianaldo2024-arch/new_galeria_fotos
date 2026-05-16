# 🖼️ New Galería Foto

**FastAPI‑based photo gallery with async image processing, JWT authentication, and Docker support.**

This project is a personal portfolio to showcase digitally created artworks. It demonstrates modern Python backend development: asynchronous operations, background tasks, secure authentication, and clean architecture.

## ✨ Features

- ✅ **Async FastAPI** – high‑performance async endpoints
- ✅ **SQLAlchemy 2.0 (asyncio)** + **Alembic** for database migrations
- ✅ **JWT authentication** – register, login, protected routes
- ✅ **Image upload** – automatic thumbnail generation in the background (`BackgroundTasks`)
- ✅ **Robust file validation** – MIME type checking via `python‑magic` (magic bytes)
- ✅ **Modular structure** – models, schemas, CRUD, services, API v1
- ✅ **PostgreSQL** + **Redis** ready (Redis prepared for future task queues)
- ✅ **Docker & Docker Compose** – easy local development and deployment
- ✅ **Auto‑generated API docs** – Swagger UI at `/docs`

## 🛠️ Tech Stack

| Layer       | Technologies |
|-------------|--------------|
| Backend     | Python 3.11, FastAPI, Uvicorn |
| Database    | PostgreSQL, SQLAlchemy (async), Alembic |
| Auth        | JWT (python-jose), bcrypt (passlib) |
| Images      | Pillow, python‑magic |
| Task queue  | BackgroundTasks (FastAPI native) |
| Container   | Docker, Docker Compose |
| Cloud ready | Railway, Render, or any Docker host |

## 📁 Project Structure

new_galeria_foto/
├── app/
│ ├── api/ # API routers and endpoints
│ ├── core/ # Config, DB, security
│ ├── crud/ # Database operations
│ ├── models/ # SQLAlchemy models
│ ├── schemas/ # Pydantic schemas
│ ├── services/ # Business logic (image processing, validation)
│ └── main.py # FastAPI app entry point
├── tests/ # Unit and integration tests (soon)
├── uploads/ # Original uploaded images (gitignored)
├── thumbnails/ # Generated thumbnails (gitignored)
├── .env.example # Environment variables template
├── docker-compose.yml # Multi‑container setup
├── Dockerfile # App container definition
├── pyproject.toml # Dependencies (Poetry)
└── README.md


## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL (or Docker)
- Redis (optional, for future scaling)
- [Poetry](https://python-poetry.org/) for dependency management

### 1. Clone the repository

```bash
git clone https://github.com/https://github.com/fabianaldo2024-arch/new_galeria_fotos.git
cd new_galeria_foto