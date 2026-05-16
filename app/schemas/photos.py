from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class PhotoBase(BaseModel):
    title: str
    description: Optional[str] = None
    filename: str
    file_path: str  
    width: Optional[int] = None
    height: Optional[int] = None
    file_size: Optional[int] = None
    album_id: UUID

class PhotoCreate(PhotoBase):
    pass  

class PhotoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    album_id: Optional[UUID] = None

class PhotoOut(PhotoBase):
    id: UUID
    thumbnail_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    owner_id: UUID  

    class Config:
        from_attributes = True
