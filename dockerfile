# 1. Usamos una imagen ligera de Python 3.11 basada en Debian (compatible con Mint)
FROM python:3.11-slim-bookworm

# 2. Seteamos variables de entorno para Python y Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# 3. Instalamos dependencias del sistema operativo
# libmagic1 es CRUCIAL para que python-magic funcione [1, 2]
# build-essential y libpq-dev son para compilar extensiones de DB si es necesario
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic1 \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Instalamos Poetry en el contenedor
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# 5. Creamos y seteamos el directorio de trabajo
WORKDIR /app

# 6. Copiamos solo los archivos de dependencias primero (para aprovechar el cache de Docker) [3]
COPY pyproject.toml poetry.lock* ./

# 7. Instalamos las dependencias del proyecto
RUN poetry install --no-root --only main

# 8. Copiamos el resto del código de la aplicación
COPY . .

# 9. Creamos las carpetas para uploads y thumbnails si no existen [2]
RUN mkdir -p uploads thumbnails

# 10. Exponemos el puerto que usa FastAPI
EXPOSE 8000

# 11. Comando para iniciar la app con Uvicorn [2]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]