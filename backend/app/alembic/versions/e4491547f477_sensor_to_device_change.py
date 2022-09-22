"""Sensor to device change

Revision ID: e4491547f477
Revises: 6c6cf9493da5
Create Date: 2022-09-04 17:35:30.409949

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = 'e4491547f477'
down_revision = '6c6cf9493da5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('name', sa.TEXT(), nullable=True),
    sa.Column('uuid', UUID(), nullable=False),
    sa.Column('type', sa.SMALLINT(), nullable=True),
    sa.Column('location', sa.SMALLINT(), nullable=True),
    sa.Column('first_occurrence', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('date_registered', postgresql.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_device_id'), 'device', ['id'], unique=False)
    op.create_table('device_location',
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('location_id')
    )
    op.create_index(op.f('ix_device_location_location_id'), 'device_location', ['location_id'], unique=False)
    op.create_table('device_type',
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('type_id')
    )
    op.create_index(op.f('ix_device_type_type_id'), 'device_type', ['type_id'], unique=False)
    op.drop_index('ix_sensor_id', table_name='sensor')
    op.drop_table('sensor')
    op.drop_index('ix_sensor_type_type_id', table_name='sensor_type')
    op.drop_table('sensor_type')
    op.drop_index('ix_sensor_location_location_id', table_name='sensor_location')
    op.drop_table('sensor_location')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sensor_location',
    sa.Column('location_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('location_id', name='sensor_location_pkey')
    )
    op.create_index('ix_sensor_location_location_id', 'sensor_location', ['location_id'], unique=False)
    op.create_table('sensor_type',
    sa.Column('type_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('type_id', name='sensor_type_pkey')
    )
    op.create_index('ix_sensor_type_type_id', 'sensor_type', ['type_id'], unique=False)
    op.create_table('sensor',
    sa.Column('id', sa.BIGINT(), server_default=sa.text("nextval('sensor_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('type', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('location', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('first_occurrence', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('date_registered', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='sensor_pkey')
    )
    op.create_index('ix_sensor_id', 'sensor', ['id'], unique=False)
    op.drop_index(op.f('ix_device_type_type_id'), table_name='device_type')
    op.drop_table('device_type')
    op.drop_index(op.f('ix_device_location_location_id'), table_name='device_location')
    op.drop_table('device_location')
    op.drop_index(op.f('ix_device_id'), table_name='device')
    op.drop_table('device')
    # ### end Alembic commands ###