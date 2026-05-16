import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine, AsyncSessionLocal
from app.crud.crud_user import get_user_by_email, create_user
from app.schemas.user import UserCreate
from app.api.v1 import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando aplicación...")
    
    # Asegurar que existan las carpetas de almacenamiento local
    os.makedirs("./uploads", exist_ok=True)
    os.makedirs("./thumbnails", exist_ok=True)
    
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

# Incluir el router centralizado de la API v1
app.include_router(api_router, prefix="/api/v1")
