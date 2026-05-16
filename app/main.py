import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.database import engine, AsyncSessionLocal
from app.crud.crud_user import get_user_by_email, create_user
from app.schemas.user import UserCreate
from app.api.v1 import api_router
from app.models.photo import Photo  # Importamos el modelo para traer las fotos en Python

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando aplicación...")
    os.makedirs("./uploads", exist_ok=True)
    os.makedirs("./thumbnails", exist_ok=True)
    os.makedirs("./frontend/static/css", exist_ok=True)
    os.makedirs("./frontend/static/js", exist_ok=True)
    
    async with AsyncSessionLocal() as db:
        admin = await get_user_by_email(db, "admin@example.com")
        if not admin:
            await create_user(
                db,
                UserCreate(username="admin", email="admin@example.com", password="admin123")
            )
            print("✅ Usuario administrador creado")
    
    yield
    print("🛑 Apagando aplicación...")
    await engine.dispose()

app = FastAPI(title=settings.APP_NAME, version="0.1.0", lifespan=lifespan)

# Montar archivos estáticos
app.mount("/static/uploads", StaticFiles(directory="./uploads"), name="uploads")
app.mount("/static/thumbnails", StaticFiles(directory="./thumbnails"), name="thumbnails")
app.mount("/ui", StaticFiles(directory="./frontend/static"), name="frontend_static")

# Configurar Jinja2 apuntando a tu carpeta frontend
templates = Jinja2Templates(directory="./frontend")

# Dependencia para la base de datos
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/", response_class=HTMLResponse)
async def root(db: AsyncSession = Depends(get_db)):
    """
    Ruta raíz que consulta la base de datos con Python asíncrono 
    y renderiza la plantilla Jinja2 inyectando las fotos directamente.
    """
    result = await db.execute(select(Photo).order_by(Photo.created_at.desc()))
    photos_list = result.scalars().all()
    
    # Python genera el HTML dinámicamente pasando la lista "photos" a la plantilla
    return templates.TemplateResponse("index.html", {"request": {}, "photos": photos_list})

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(api_router, prefix="/api/v1")


