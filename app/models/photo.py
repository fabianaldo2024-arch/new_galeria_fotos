from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class Photo(Base, TimestampMixin):
    __tablename__ = "photos"

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    filename = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=False)
    thumbnail_path = Column(String(1000), nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)

    album_id = Column(UUID(as_uuid=True), ForeignKey("albums.id"), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="photos")
    album = relationship(
        "Album", 
        back_populates="photos", 
        foreign_keys=[album_id],
        primaryjoin="Photo.album_id == Album.id"
    )