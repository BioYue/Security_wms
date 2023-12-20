from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.admin.models import SecurityCode
from start import db
import json

bp = Blueprint('web', __name__, url_prefix='/purple_sands', template_folder='templates', static_folder='static')


def index():
    return render_template('index.html', **locals())


@bp.route('/identify')
def identify():
    code = request.args.get('code')
    products = SecurityCode.query.filter_by(security_code=code).first()
    if products:
        products_json = {
            'goods_name': products.goods_name,
            'security_code': products.security_code,
            'queries_num': products.queries_num
        }
        products.queries_num += 1
        db.session.commit()
    else:
        products_json = None
    return render_template('identify.html', **locals())



