# app/api/v1/endpoints/photos.py
import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, BackgroundTasks
from sqlalchemy import select
from PIL import Image

from app.api.v1.dependencies import DBSessionDep, get_current_user
from app.models.user import User
from app.models.album import Album
from app.models.photo import Photo
from app.schemas.photos import PhotoOut
from app.services.image_processing import generate_thumbnail_sync
from app.services.file_validation import validate_image_file

router = APIRouter()

UPLOAD_DIR = Path("uploads")
THUMB_DIR = Path("thumbnails")
UPLOAD_DIR.mkdir(exist_ok=True)
THUMB_DIR.mkdir(exist_ok=True)

@router.post("/", response_model=PhotoOut)
async def create_photo(
    background_tasks: BackgroundTasks,
    db: DBSessionDep,
    current_user: User = Depends(get_current_user),
    title: str = Form(...),
    description: str = Form(None),
    album_id: str = Form(...),
    file: UploadFile = File(...),
):
    # 1. Validar que el álbum existe
    result = await db.execute(select(Album).where(Album.id == uuid.UUID(album_id)))
    album = result.scalar_one_or_none()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # 2. Validación de tipo MIME básica (rápida)
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image MIME type")
    
    # 3. Leer los primeros bytes para validación mágica (sin consumir el archivo)
    contents = await file.read(1024)   # Leemos 1KB, suficiente para magic bytes
    await file.seek(0)                 # Reiniciamos el puntero para poder guardar después
    
    # 4. Validación robusta con python-magic
    validate_image_file(contents, file.filename)
    
    # 5. Guardar archivo original
    ext = file.filename.split(".")[-1].lower()
    safe_name = f"{uuid.uuid4().hex}.{ext}"
    file_path = UPLOAD_DIR / safe_name
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 6. Obtener dimensiones y tamaño
    with Image.open(file_path) as img:
        width, height = img.size
    file_size = file_path.stat().st_size
    
    # 7. Crear registro en BD (thumbnail_path inicialmente None)
    photo = Photo(
        title=title,
        description=description,
        filename=file.filename,
        file_path=str(file_path),
        thumbnail_path=None,
        width=width,
        height=height,
        file_size=file_size,
        album_id=album.id,
        owner_id=current_user.id,
    )
    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    
    # 8. Tarea en segundo plano para generar thumbnail
    thumb_filename = f"thumb_{photo.id}.jpg"
    thumb_path = THUMB_DIR / thumb_filename
    background_tasks.add_task(
        generate_thumbnail_sync,
        original_path=file_path,
        thumb_path=thumb_path,
    )
    
    return photo