"""message

Revision ID: 99355bf70412
Revises: e4efc7674b7e
Create Date: 2024-12-02 23:31:10.636088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99355bf70412'
down_revision: Union[str, None] = 'e4efc7674b7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
