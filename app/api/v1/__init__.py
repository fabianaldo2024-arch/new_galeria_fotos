from fastapi import APIRouter
from app.api.v1.endpoints import albums, photos, auth

api_router = APIRouter()
api_router.include_router(albums.router, prefix="/albums", tags=["albums"])
api_router.include_router(photos.router, prefix="/photos", tags=["photos"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])