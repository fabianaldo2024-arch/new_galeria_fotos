# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema para Pillow y python-magic
RUN apt-get update && apt-get install -y \
    libmagic1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install poetry

# Copiar archivos de dependencias
COPY pyproject.toml poetry.lock ./

# Instalar dependencias sin crear entorno virtual (para que estén en el sistema)
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copiar el resto del código
COPY . .

# Crear directorios para uploads y thumbnails
RUN mkdir -p uploads thumbnails

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]