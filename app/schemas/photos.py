from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class PhotoBase(BaseModel):
    title: str
    description: Optional[str] = None
    filename: str
    file_path: str  # Podríamos ocultarlo en respuestas, pero de momento lo mostramos
    width: Optional[int] = None
    height: Optional[int] = None
    file_size: Optional[int] = None
    album_id: UUID

class PhotoCreate(PhotoBase):
    pass  # En creación se requiere todo excepto los auto-generados

class PhotoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    album_id: Optional[UUID] = None

class PhotoOut(PhotoBase):
    id: UUID
    thumbnail_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    owner_id: UUID  # Para saber quién la subió

    model_config = dict(from_attributes=True)