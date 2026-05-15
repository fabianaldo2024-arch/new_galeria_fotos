from app.models.base import Base
from app.models.user import User
from app.models.album import Album
from app.models.photo import Photo

# Así todos los modelos quedan registrados y Alembic puede detectarlos
__all__ = ["Base", "User", "Album", "Photo"]