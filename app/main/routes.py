from flask import Blueprint, jsonify, render_template
from flask_jwt_extended import get_jwt_identity
from ..auth.routes import custom_jwt_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/index')
@main_bp.route('/')
@custom_jwt_required()
def home():
    return render_template('main/index.html', title='Home')


@main_bp.route('/contacts')
@custom_jwt_required(optional=True)
def contacts():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(
            {
                'message': f"Hello, {current_user}! These are your contacts."
            }
        )
    else:
        return "Hello, anonymous user! These are some public contacts."
