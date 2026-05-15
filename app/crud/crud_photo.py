from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.photo import Photo
from app.schemas.photos import PhotoCreate, PhotoUpdate

async def get_photo(db: AsyncSession, photo_id: UUID) -> Photo | None:
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    return result.scalar_one_or_none()

async def get_photos_by_album(db: AsyncSession, album_id: UUID, skip: int = 0, limit: int = 100) -> List[Photo]:
    result = await db.execute(
        select(Photo).where(Photo.album_id == album_id).offset(skip).limit(limit).order_by(Photo.created_at.desc())
    )
    return result.scalars().all()

async def create_photo(db: AsyncSession, photo_in: PhotoCreate, owner_id: UUID) -> Photo:
    db_photo = Photo(**photo_in.model_dump(), owner_id=owner_id)
    db.add(db_photo)
    await db.commit()
    await db.refresh(db_photo)
    return db_photo

async def update_photo(db: AsyncSession, db_photo: Photo, photo_in: PhotoUpdate) -> Photo:
    update_data = photo_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_photo, field, value)
    db.add(db_photo)
    await db.commit()
    await db.refresh(db_photo)
    return db_photo

async def delete_photo(db: AsyncSession, photo_id: UUID) -> None:
    await db.execute(delete(Photo).where(Photo.id == photo_id))
    await db.commit()