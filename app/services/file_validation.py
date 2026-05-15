# app/services/file_validation.py
import magic
from fastapi import HTTPException

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
}

def validate_image_file(content: bytes, filename: str) -> None:
    """
    Valida que el contenido del archivo sea realmente una imagen permitida.
    Lanza HTTPException 400 si no es válido.
    """
    # Detectar MIME real por magic bytes
    mime = magic.from_buffer(content, mime=True)
    if mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Formato de imagen no soportado: {mime}. Solo se permiten: {', '.join(ALLOWED_MIME_TYPES)}"
        )
    
    # Validación opcional de extensión (capa extra)
    ext = filename.split(".")[-1].lower()
    allowed_exts = ["jpg", "jpeg", "png", "gif", "webp"]
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Extensión de archivo no válida: {ext}. Permitted: {', '.join(allowed_exts)}"
        )