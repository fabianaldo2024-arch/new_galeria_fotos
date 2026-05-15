
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Album(Base, TimestampMixin):
    __tablename__ = "albums"

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    cover_photo_id = Column(UUID(as_uuid=True), ForeignKey("photos.id"), nullable=True)

    # Relación con fotos - usando primaryjoin para desambiguar
    photos = relationship(
        "Photo", 
        back_populates="album", 
        primaryjoin="Album.id == Photo.album_id"
    )
    
    cover_photo = relationship(
    "Photo", 
    foreign_keys=[cover_photo_id], 
    post_update=True, 
)