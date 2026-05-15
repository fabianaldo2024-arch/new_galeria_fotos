from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class AlbumBase(BaseModel):
    title: str
    description: Optional[str] = None

class AlbumCreate(AlbumBase):
    pass  # Los mismos campos que la base

class AlbumUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    cover_photo_id: Optional[UUID] = None

class AlbumOut(AlbumBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    cover_photo_id: Optional[UUID] = None

    model_config = dict(from_attributes=True)