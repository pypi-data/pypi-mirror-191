# -*- coding: utf-8 -*-
"""empty message

Revision ID: roc_dingo_0027_modify_view_rpw_events_per_day
Revises: roc_dingo_0026_add_table_events
Create Date: 2023-02-14 17:04:01.249362

"""
from alembic import op
from pathlib import Path

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0027_modify_view_rpw_events_per_day'
down_revision = 'roc_dingo_0026_add_table_events'
branch_labels = None
depends_on = None


def upgrade():

    filename = 'SQL/roc_dingo_0027_modifiy_view_rpw_events_per_day.sql'
    sql_file = Path(__file__).parent / filename
    with open(sql_file, 'r') as sql_content:
        sql_cmd = sql_content.read()
        op.execute(sql_cmd)


def downgrade():

    filename = 'SQL/roc_dingo_0026_create_view_anomalies_per_day.sql'
    sql_file = Path(__file__).parent / filename
    with open(sql_file, 'r') as sql_content:
        sql_cmd = sql_content.read()
        op.execute(sql_cmd)
