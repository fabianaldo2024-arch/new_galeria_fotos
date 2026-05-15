"""Initial migration

Revision ID: 6e0de07ba9b1
Revises: 
Create Date: 2026-05-13 23:24:11.352990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e0de07ba9b1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade():
    # 1. Crear tabla users
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # 2. Crear tabla photos (SIN la FK hacia albums aún)
    op.create_table('photos',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('filename', sa.String(500), nullable=False),
        sa.Column('file_path', sa.String(1000), nullable=False),
        sa.Column('thumbnail_path', sa.String(1000), nullable=True),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('album_id', sa.UUID(), nullable=False),  # FK que se agregará después
        sa.Column('owner_id', sa.UUID(), nullable=False),   # FK hacia users
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 3. Crear tabla albums (SIN la FK hacia photos aún)
    op.create_table('albums',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cover_photo_id', sa.UUID(), nullable=True),  # FK que se agregará después
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    def downgrade():
    # Aquí pones el código que me diste:
        op.drop_constraint('fk_photos_album_id', 'photos', type_='foreignkey')
        op.drop_constraint('fk_albums_cover_photo_id', 'albums', type_='foreignkey')
        op.drop_constraint('fk_photos_owner_id', 'photos', type_='foreignkey')
        op.drop_table('albums')
        op.drop_table('photos')
        op.drop_table('users')





    # 4. Ahora agregar las claves foráneas
    op.create_foreign_key('fk_photos_owner_id', 'photos', 'users', ['owner_id'], ['id'])
    op.create_foreign_key('fk_photos_album_id', 'photos', 'albums', ['album_id'], ['id'])
    op.create_foreign_key('fk_albums_cover_photo_id', 'albums', 'photos', ['cover_photo_id'], ['id'])

    # 5. Crear índices (si los hay)
    op.create_index('ix_users_username', 'users', ['username'])


