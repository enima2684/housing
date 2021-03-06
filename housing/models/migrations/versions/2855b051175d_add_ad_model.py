"""add Ad model

Revision ID: 2855b051175d
Revises: b89bcb3c0fd0
Create Date: 2018-12-16 19:07:29.565060

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2855b051175d'
down_revision = 'b89bcb3c0fd0'
branch_labels = None
depends_on = None


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ads')
    # ### end Alembic commands ###


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ads',
    sa.Column('id', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('source_file', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('web_site', postgresql.ENUM('PAP', 'SeLoger', name='websites'), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('area', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('postal_code', sa.VARCHAR(length=16), autoincrement=False, nullable=False),
    sa.Column('url', sa.VARCHAR(length=512), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='ads_pkey')
    )
    # ### end Alembic commands ###
