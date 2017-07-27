# This program is free software; you can redistribute it and/or modify
## i under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

"""add firmware columns to system table

Revision ID: 2a56e56fbe26
Revises: f18df089261
Create Date: 2017-07-25 18:48:06.192722

"""

# revision identifiers, used by Alembic.
revision = '2a56e56fbe26'
down_revision = 'f18df089261'

from alembic import op
from sqlalchemy import Column, String, DateTime

def upgrade():
    op.add_column('system', Column('fw_version', String(32), nullable=True))
    op.add_column('system', Column('fw_date', DateTime, nullable=True))

def downgrade():
    op.drop_column('system', 'fw_version')
    op.drop_column('system', 'fw_date')

