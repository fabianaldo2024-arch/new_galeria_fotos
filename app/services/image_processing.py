import os
import uuid
import logging
import aiofiles
from pathlib import Path
from fastapi import UploadFile
from PIL import Image

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("./uploads")
THUMB_DIR = Path("./thumbnails")

def generate_thumbnail_sync(original_path: Path, thumb_path: Path, size: tuple = (256, 256)) -> bool:
    """
    Genera un thumbnail de la imagen original.
    Retorna True si éxito, False si error.
    """
    try:
        with Image.open(original_path) as img:
            # Convertir a RGB si es necesario (para PNG con transparencia)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.thumbnail(size)
            img.save(thumb_path, "JPEG", quality=85, optimize=True)
        logger.info(f"Thumbnail generado: {thumb_path}")
        return True
    except Exception as e:
        logger.error(f"Error generando thumbnail {original_path}: {e}")
        return False

async def process_and_save_photo(file: UploadFile):
    """
    Guarda la foto original de forma asíncrona, extrae sus metadatos
    y genera automáticamente su respectiva miniatura (thumbnail).
    """
    # 1. Generar nombre único manteniendo la extensión original
    _, ext = os.path.splitext(file.filename or "")
    unique_name = f"{uuid.uuid4()}{ext}"
    
    original_path = UPLOAD_DIR / unique_name
    thumb_name = f"thumb_{uuid.uuid4()}.jpg"  # Siempre guardamos en JPG según tu función
    thumb_path = THUMB_DIR / thumb_name

    # 2. Guardar el archivo original en el disco asíncronamente
    file_size = 0
    async with aiofiles.open(original_path, "wb") as buffer:
        while content := await file.read(1024 * 1024):
            file_size += len(content)
            await buffer.write(content)

    # 3. Abrir la imagen para extraer las dimensiones del original
    with Image.open(original_path) as img:
        width, height = img.size

    # 4. Generar la miniatura usando tu función sincrónica
    thumb_success = generate_thumbnail_sync(original_path, thumb_path)
    final_thumb_path = str(thumb_path) if thumb_success else None

    return {
        "filename": unique_name,
        "file_path": str(original_path),
        "thumbnail_path": final_thumb_path,
        "file_size": file_size,
        "width": width,
        "height": height
    }
