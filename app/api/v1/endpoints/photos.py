from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional

from app.core.database import AsyncSessionLocal
# Importamos la clase genérica 'Photo' que es el estándar de SQLAlchemy
from app.models.photo import Photo 
from app.schemas.photos import PhotoOut
from app.services.image_processing import process_and_save_photo

router = APIRouter()

# Dependencia para la sesión de la base de datos
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/upload", response_model=PhotoOut)
async def upload_photo(
    title: str = Form(...),
    album_id: UUID = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db)
):
    # 1. Validar que el archivo sea una imagen
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo enviado no es una imagen válida.")
    
    # 2. Procesar y guardar en disco (Original + Thumbnail)
    disk_data = await process_and_save_photo(file)
    
    # 3. Guardar el registro en la Base de Datos
    db_photo = Photo(
        title=title,
        description=description,
        album_id=album_id,
        filename=disk_data["filename"],
        file_path=disk_data["file_path"],
        thumbnail_path=disk_data["thumbnail_path"],
        width=disk_data["width"],
        height=disk_data["height"],
        file_size=disk_data["file_size"],
        owner_id=UUID("00000000-0000-0000-0000-000000000000") # Temporal para pruebas
    )
    
    db.add(db_photo)
    await db.commit()
    await db.refresh(db_photo)
    
    return db_photo


