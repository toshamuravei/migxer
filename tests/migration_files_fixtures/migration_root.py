"""Add table and model for diff publishing
REVISION ROOT
Revision ID: 2d9f80797b0d
Revises: None
Create Date: 2022-10-01 10:33:55.185029

"""
from alembic import op, context  # noqa
import sqlalchemy as sa  # noqa
from sqlalchemy.dialects import postgresql  # noqa

# revision identifiers, used by Alembic.
revision = '2d9f80797b0d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass
    # ### end Alembic commands ###


def downgrade():
    pass
    # ### end Alembic commands ###
