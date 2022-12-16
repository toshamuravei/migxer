"""Add table and model for diff publishing
REVISION A
Revision ID: 7474fcfa1b90
Revises: 2d9f80797b0d
Create Date: 2022-10-02 14:33:55.185029

"""
from alembic import op, context  # noqa
import sqlalchemy as sa  # noqa
from sqlalchemy.dialects import postgresql  # noqa

# revision identifiers, used by Alembic.
revision = '7474fcfa1b90'
down_revision = '2d9f80797b0d'
branch_labels = None
depends_on = None


def upgrade():
    pass
    # ### end Alembic commands ###


def downgrade():
    pass
    # ### end Alembic commands ###
