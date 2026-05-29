from app.core.config import settings  # ← esta línea debe estar
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


# El motor asíncrono se crea una vez (puede ser singleton a nivel módulo)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,           # Imprime las consultas SQL en modo debug
    pool_pre_ping=True,            # Verifica la conexión antes de usarla
    pool_size=10,                  # Número de conexiones en el pool
    max_overflow=20,               # Conexiones extra si el pool está lleno
    future=True,                   # Habilita el modo 2.0 (ya es default)
)

# La fábrica de sesiones: llamarla produce una AsyncSession
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,        # No expira objetos tras commit (útil en async)
    autocommit=False,
    autoflush=False,
)

# Dependencia para FastAPI: obtención de sesión de DB
async def get_db() -> AsyncSession:
    """Proporciona una sesión de base de datos por petición."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # Opcional: commit automático al final de la petición
            # await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

