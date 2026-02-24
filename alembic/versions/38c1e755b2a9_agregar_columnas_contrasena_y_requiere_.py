"""agregar columnas contrasena y requiere_cambio a usuarios

Revision ID: 38c1e755b2a9
Revises: d92e9f23846d
Create Date: 2026-02-06 12:31:48.655804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38c1e755b2a9'
down_revision: Union[str, Sequence[str], None] = 'd92e9f23846d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("usuarios", sa.Column("contrasena", sa.String(200), nullable=True))
    op.add_column("usuarios", sa.Column("requiere_cambio", sa.Boolean(), server_default=sa.text("TRUE"), nullable=False))


def downgrade():
    op.drop_column("usuarios", "contrasena")
    op.drop_column("usuarios", "requiere_cambio")