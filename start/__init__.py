from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from utils.filters import FILTERS
from flask_wtf import CSRFProtect

# 实例化SQLAlchemy对象
db = SQLAlchemy()
# 实例化迁移对象
migrate = Migrate()
# 实例化WTF
csrf = CSRFProtect()

# 实例化login管理
login_manager = LoginManager()
login_manager.login_message = 'Access denied.'
login_manager.login_view = 'admin.login'


def create_app():
    app = Flask(__name__)

    # 注册配置文件
    app.config.from_pyfile('settings.py')

    # 引入blog视图(这个引入必须放在create_app里)
    from app.web import views as web
    from app.admin import views as admin
    # 注册blog蓝图
    app.register_blueprint(web.bp)
    app.register_blueprint(admin.bp)

    # 注册数据库
    db.init_app(app)
    # 注册迁移对象
    migrate.init_app(app, db)

    # 注册模型
    from app.web import models
    from app.admin import models

    # 注册过滤器
    for key, value in FILTERS.items():
        app.add_template_filter(value, key)

    # 注册首页url规则  endpoint指定端点名称  view_func指定视图函数
    app.add_url_rule(rule='/', endpoint='index', view_func=web.index)

    # 注册login管理
    login_manager.init_app(app)

    # 注册wtf
    csrf.init_app(app)

    return app
