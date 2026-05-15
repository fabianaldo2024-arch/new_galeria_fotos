from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.album import Album
from app.schemas.album import AlbumCreate, AlbumUpdate

async def get_album(db: AsyncSession, album_id: UUID) -> Album | None:
    result = await db.execute(select(Album).where(Album.id == album_id))
    return result.scalar_one_or_none()

async def get_albums(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Album]:
    result = await db.execute(select(Album).offset(skip).limit(limit).order_by(Album.created_at.desc()))
    return result.scalars().all()

async def create_album(db: AsyncSession, album_in: AlbumCreate) -> Album:
    db_album = Album(**album_in.model_dump())
    db.add(db_album)
    await db.commit()
    await db.refresh(db_album)
    return db_album

async def update_album(db: AsyncSession, db_album: Album, album_in: AlbumUpdate) -> Album:
    update_data = album_in.model_dump(exclude_unset=True)  # solo campos enviados
    for field, value in update_data.items():
        setattr(db_album, field, value)
    db.add(db_album)
    await db.commit()
    await db.refresh(db_album)
    return db_album

async def delete_album(db: AsyncSession, album_id: UUID) -> None:
    await db.execute(delete(Album).where(Album.id == album_id))
    await db.commit()