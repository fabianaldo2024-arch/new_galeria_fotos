from uuid import UUID
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.api.v1.dependencies import DBSessionDep
from app.schemas.album import AlbumCreate, AlbumUpdate, AlbumOut
from app.crud import crud_album

router = APIRouter(prefix="/albums", tags=["albums"])

@router.get("/", response_model=List[AlbumOut])
async def list_albums(db: DBSessionDep, skip: int = 0, limit: int = 100):
    return await crud_album.get_albums(db, skip=skip, limit=limit)

@router.post("/", response_model=AlbumOut, status_code=status.HTTP_201_CREATED)
async def create_album(album_in: AlbumCreate, db: DBSessionDep):
    return await crud_album.create_album(db, album_in)

@router.get("/{album_id}", response_model=AlbumOut)
async def get_album(album_id: UUID, db: DBSessionDep):
    album = await crud_album.get_album(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Álbum no encontrado")
    return album

@router.patch("/{album_id}", response_model=AlbumOut)
async def update_album(album_id: UUID, album_in: AlbumUpdate, db: DBSessionDep):
    album = await crud_album.get_album(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Álbum no encontrado")
    return await crud_album.update_album(db, album, album_in)

@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_album(album_id: UUID, db: DBSessionDep):
    album = await crud_album.get_album(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Álbum no encontrado")
    await crud_album.delete_album(db, album_id)

