# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine, AsyncSessionLocal  # Añadimos AsyncSessionLocal
from app.crud.crud_user import get_user_by_email, create_user  # Nuevo
from app.schemas.user import UserCreate                       # Nuevo

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando aplicación...")
    
    # Crear usuario administrador si no existe
    async with AsyncSessionLocal() as db:
        admin = await get_user_by_email(db, "admin@example.com")
        if not admin:
            await create_user(
                db,
                UserCreate(
                    username="admin",
                    email="admin@example.com",
                    password="admin123"
                )
            )
            print("✅ Usuario administrador creado")
    
    yield  # La aplicación se ejecuta aquí
    
    print("🛑 Apagando aplicación...")
    await engine.dispose()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Bienvenido a New Galería Foto"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Incluir el router de la API v1
from app.api.v1 import api_router
app.include_router(api_router, prefix="/api/v1")