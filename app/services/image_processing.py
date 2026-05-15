# app/services/image_processing.py
import logging
from pathlib import Path
from PIL import Image

logger = logging.getLogger(__name__)

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