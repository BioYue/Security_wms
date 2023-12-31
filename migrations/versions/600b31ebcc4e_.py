"""empty message

Revision ID: 600b31ebcc4e
Revises: b90dd33f99cd
Create Date: 2023-12-19 00:58:57.351285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '600b31ebcc4e'
down_revision = 'b90dd33f99cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_info_db',
    sa.Column('after_title', sa.String(length=64), nullable=True, comment='后台标题'),
    sa.Column('former_title', sa.Text(), nullable=True, comment='主站标题'),
    sa.Column('former_info', sa.Text(), nullable=True, comment='主站介绍'),
    sa.Column('master_background', sa.Text(), nullable=True, comment='主站背景'),
    sa.Column('id', sa.Integer(), nullable=False, comment='id主键'),
    sa.Column('add_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('upd_time', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_db',
    sa.Column('username', sa.String(length=64), nullable=True, comment='用户名'),
    sa.Column('password', sa.String(length=128), nullable=True, comment='密码'),
    sa.Column('last_login', sa.DateTime(), nullable=True, comment='上次登录时间'),
    sa.Column('nickname', sa.String(length=64), nullable=True, comment='昵称'),
    sa.Column('avatar_path', sa.String(length=256), nullable=True, comment='头像路径'),
    sa.Column('id', sa.Integer(), nullable=False, comment='id主键'),
    sa.Column('add_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('upd_time', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_db')
    op.drop_table('blog_info_db')
    # ### end Alembic commands ###
