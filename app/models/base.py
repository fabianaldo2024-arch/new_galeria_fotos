# app/models/base.py
from sqlalchemy.orm import DeclarativeBase
import uuid
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass

# Mixin para añadir id UUID y timestamps automáticos a todos los modelos
class TimestampMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)