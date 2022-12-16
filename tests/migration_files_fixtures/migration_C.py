"""Add table and model for diff publishing
REVISION C
Revision ID: 7474fcfa1b90
Revises: 7954fsbh1i24
Create Date: 2022-10-04 14:33:55.185029

"""
from alembic import op, context  # noqa
import sqlalchemy as sa  # noqa
from sqlalchemy.dialects import postgresql  # noqa

# revision identifiers, used by Alembic.
revision = '8448frrr2a14'
down_revision = '7954fsbh1i24'
branch_labels = None
depends_on = None


def upgrade():
    pass
    # ### end Alembic commands ###


def downgrade():
    pass
    # ### end Alembic commands ###
