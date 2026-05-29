FROM python:3.11-slim

WORKDIR /app

# Instalar Poetry
RUN pip install --no-cache-dir poetry

# Copiar archivos de configuración
COPY pyproject.toml poetry.lock* ./

# Configurar Poetry
RUN poetry config virtualenvs.create false

# Instalar dependencias (sin el proyecto actual)
RUN poetry install --no-interaction --no-ansi --no-root

# Copiar el resto del código
COPY . .

# Asegurar que la carpeta app sea un paquete Python
RUN touch app/__init__.py

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
