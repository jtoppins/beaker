# This program is free software; you can redistribute it and/or modify
## i under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

"""add firmware columns to system table
add firmware columns to device table

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
    op.add_column('system', Column('sysfw_version', String(32), nullable=True))
    op.add_column('system', Column('sysfw_date', DateTime, nullable=True))
    op.add_column('device', Column('fw_version', String(32), nullable=True))
    op.add_column('device', Column('fw_date', DateTime, nullable=True))
    # TODO: I think we also need to play with the table constraints for the
    # device table as well but I am not sure specifically what is needed
    # right now

def downgrade():
    op.drop_column('system', 'sysfw_version')
    op.drop_column('system', 'sysfw_date')
    op.drop_column('device', 'fw_version')
    op.drop_column('device', 'fw_date')

