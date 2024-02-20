"""init

Revision ID: 109129b23688
Revises: 
Create Date: 2024-02-21 00:10:41.754209

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '109129b23688'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('age', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('book',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('age', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book')
    op.drop_table('user')
    # ### end Alembic commands ###
