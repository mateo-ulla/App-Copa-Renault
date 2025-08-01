"""Add email to User

Revision ID: 17fdf12b3801
Revises: 
Create Date: 2025-07-24 11:46:06.215553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17fdf12b3801'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sponsor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('website', sa.String(length=200), nullable=True),
    sa.Column('banner_url', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('sport', sa.String(length=20), nullable=False),
    sa.Column('category', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fixture',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('home_team_id', sa.Integer(), nullable=False),
    sa.Column('away_team_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('score_home', sa.Integer(), nullable=True),
    sa.Column('score_away', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['away_team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['home_team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('cantina_reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('menu', sa.String(length=200), nullable=False),
    sa.Column('dietary_restrictions', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cantina_reservation')
    op.drop_table('user')
    op.drop_table('fixture')
    op.drop_table('team')
    op.drop_table('sponsor')
    # ### end Alembic commands ###
