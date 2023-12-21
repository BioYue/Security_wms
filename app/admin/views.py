import json
import secrets
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, url_for
from flask_login import login_user, login_required, logout_user
from sqlalchemy import or_
from werkzeug.security import check_password_hash

from start import db, login_manager
from start.settings import BASE_DIR
from .models import SecurityCode, User

bp = Blueprint('admin', __name__, url_prefix='/zs_admin', template_folder='templates', static_folder='static')


# 加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/login', methods=['get', 'post'])
def login():
    """
    后台管理-登录页+校验API
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'status': 'success', 'message': 'login_successful'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'login_fail'}), 200


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return 'logout_success'


@bp.route('/master_settings')
@login_required
def master_settings():
    """
    主站设置
    :return:
    """
    return render_template('master_settings.html')


@bp.route('/main_img_upload', methods=['post'])
@login_required
def main_img_upload():
    """
    主站图片上传
    :return:
    """
    location = request.form['location']
    file = request.files['file']
    location = 'top' if location == 'top' else 'center'
    file_path = f'app/web/static/imgs/{location}.jpg'
    file.save(BASE_DIR / file_path)
    return {'url': url_for('web.static', filename=f'imgs/{location}.jpg')}


# @bp.route('/register')
# def register():
#     """
#     用户注册临时API
#     :return:
#     """
#     username = 'fanjuying'
#     password = 'fanjuyingzisha'
#     password_hash = generate_password_hash(password, method='pbkdf2:sha256:600000')
#     user = User(username=username, password=password_hash)
#     db.session.add(user)
#     db.session.commit()
#     return '注册成功'


@bp.route('/security')
@login_required
def security():
    return render_template('security.html')


@bp.route('/security_add', methods=['post'])
@login_required
def security_add():
    try:
        production_time = request.form['date']
        goods_name = request.form['name']
        creat_num = int(request.form['num'])

        # 数据验证，确保 production_time, goods_name, creat_num 是合法的
        security_codes = [
            {
                'goods_name': goods_name,
                'production_time': production_time,
                'security_code': secrets.token_hex(6)
            }
            for _ in range(creat_num)
        ]
        # start = time.time()
        # 批量插入，使用事务
        # with db.session.begin():
        db.session.bulk_insert_mappings(SecurityCode, security_codes)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Records deleted successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/security_query')
@login_required
def security_query():
    page = request.args.get('page', type=int, default=1)
    limit = request.args.get('limit', type=int, default=15)
    word = request.args.get('word')
    if word:
        security_code_pg = SecurityCode.query.filter(
            or_(SecurityCode.goods_name.like(f"%{word}%"), SecurityCode.security_code.like(f"%{word}%"))) \
            .order_by(SecurityCode.id.desc()).paginate(page=page, per_page=limit)
    else:
        security_code_pg = SecurityCode.query.order_by(SecurityCode.id.desc()).paginate(page=page, per_page=limit)

    security_code_list = []
    for item in security_code_pg.items:
        row = {
            'id': item.id,
            'goods_name': item.goods_name,
            'security_code': item.security_code,
            'production_time': item.production_time.strftime("%Y-%m-%d"),
            'queries_num': item.queries_num,
            'add_time': item.add_time.strftime("%Y-%m-%d %H:%M"),
            'upd_time': item.upd_time.strftime("%Y-%m-%d %H:%M")
        }
        security_code_list.append(row)
    data = {
        'code': 0,
        'data': security_code_list,
        'count': security_code_pg.total,
        'msg': ''
    }
    return jsonify(data)


@bp.route('/security_delete', methods=['post'])
@login_required
def security_delete():
    try:
        ids = json.loads(request.form['data'])['ids']
        SecurityCode.query.filter(SecurityCode.id.in_(ids)).delete()
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Records deleted successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/security_batch_delete', methods=['post'])
@login_required
def security_batch_delete():
    try:
        production_time = request.form['date']
        goods_name = request.form['name']

        if production_time != '' and goods_name != '':
            SecurityCode.query.filter_by(production_time=production_time, goods_name=goods_name).delete()
        elif production_time != '':
            SecurityCode.query.filter_by(production_time=datetime.strptime(production_time, "%Y-%m-%d")).delete()
        elif goods_name != '':
            SecurityCode.query.filter_by(goods_name=goods_name).delete()
        else:
            return jsonify({'status': 'error', 'message': 'Both date and name are missing'}), 400

        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Records deleted successfully'})
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500
