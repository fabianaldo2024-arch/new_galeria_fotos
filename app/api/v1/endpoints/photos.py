from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID, uuid4
from typing import Optional

from app.core.database import AsyncSessionLocal
from app.models.photo import Photo 
from app.models.user import User    
from app.schemas.photos import PhotoOut
from app.services.image_processing import process_and_save_photo

try:
    from app.models.album import Album
except ImportError:
    Album = None

router = APIRouter()

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
    # 1. Validar formato de la imagen
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo enviado no es una imagen válida.")
    
    # 2. RESOLUCIÓN DE DUEÑO: Buscar cualquier usuario administrador real en PostgreSQL
    result_user = await db.execute(select(User).limit(1))
    owner_user = result_user.scalars().first()
    
    if not owner_user:
        owner_user = User(
            id=uuid4(),
            username="rocker_admin",
            email="admin@example.com",
            hashed_password="placeholder_hash"
        )
        db.add(owner_user)
        await db.flush()

      # 3. RESOLUCIÓN DE ÁLBUM: Validar de forma segura si el álbum de prueba ya existe
    final_album_id = album_id
    if Album is not None:
        result_album = await db.execute(select(Album).where(Album.id == album_id))
        existing_album = result_album.scalars().first()
        
        # Si NO existe el álbum de ceros, recién ahí lo creamos por única vez
        if not existing_album:
            new_album = Album(
                id=album_id,
                title="Default Album"
            )
            db.add(new_album)
            await db.flush()  # Registra el nuevo álbum de forma segura
        # Si ya existe, Python ignora el bloque de creación y continúa limpio

    # 4. Procesamiento físico de archivos en las carpetas locales
    disk_data = await process_and_save_photo(file)
    
    # 5. Persistencia del registro final mapeado con llaves primarias existentes
    db_photo = Photo(
        title=title,
        description=description,
        album_id=final_album_id,
        filename=disk_data["filename"],
        file_path=disk_data["file_path"],
        thumbnail_path=disk_data["thumbnail_path"],
        width=disk_data["width"],
        height=disk_data["height"],
        file_size=disk_data["file_size"],
        owner_id=owner_user.id  
    )
    
    try:
        db.add(db_photo)
        await db.commit()
        await db.refresh(db_photo)
    except Exception as db_err:
        await db.rollback()
        print(f"❌ Fallo crítico en inserción: {db_err}")
        raise HTTPException(status_code=500, detail=f"Excepción de Base de Datos: {db_err}")
    
    return db_photo




