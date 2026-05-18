from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

# Directorios base del proyecto (ajusta si tu app no está en la raíz)
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # sube desde app/core/ hasta la raíz

UPLOAD_DIR = BASE_DIR / "uploads"
THUMBNAIL_DIR = BASE_DIR / "thumbnails"

# Asegurar que los directorios existen (opcional pero recomendado)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):
    # Configuración general de la aplicación
    APP_NAME: str = "New Galería Foto"
    DEBUG: bool = Field(default=False, description="Modo debug")

    # Configuración de base de datos
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://user:pass@localhost:5432/dbname",
        description="URL de conexión asíncrona a PostgreSQL con asyncpg"
    )
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "pass"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "new_galeria_foto"

    # Redis (para ARQ)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Almacenamiento de fotos
    UPLOAD_DIR: str = "./uploads"

    # Seguridad JWT
    SECRET_KEY: str = Field(
        default="tu-super-secret-key-cambia-esto-en-produccion",
        description="Clave secreta para firmar JWT"
    )
    ALGORITHM: str = Field(default="HS256", description="Algoritmo para JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Minutos de expiración del token")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()