from start import db
from datetime import datetime
from flask_login import UserMixin


class BaseModel(db.Model):
    """ 基类模型 """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, comment='id主键')
    add_time = db.Column(db.DateTime, default=datetime.now(), comment='创建时间')
    upd_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), comment='更新时间')


class SecurityCode(BaseModel):
    """ 防伪码表 """
    __tablename__ = 'security_db'
    goods_name = db.Column(db.String(128), comment='产品名称')
    security_code = db.Column(db.String(24), comment='防伪码')
    production_time = db.Column(db.DateTime, comment='生产时间')
    queries_num = db.Column(db.Integer, default=0, comment='查询次数')


class User(UserMixin, BaseModel):
    """ 用户模型 """
    __tablename__ = 'user_db'
    username = db.Column(db.String(64), unique=True, comment='用户名')
    password = db.Column(db.String(128), comment='密码')
    last_login = db.Column(db.DateTime, comment='上次登录时间')
    nickname = db.Column(db.String(64), comment='昵称')
    avatar_path = db.Column(db.String(256), comment='头像路径')


class BlogInfo(BaseModel):
    """ 网站信息 """
    __tablename__ = 'blog_info_db'
    after_title = db.Column(db.String(64), comment='后台标题')
    former_title = db.Column(db.Text, comment='主站标题')
    former_info = db.Column(db.Text, comment='主站介绍')
    master_background = db.Column(db.Text, comment='主站背景')
