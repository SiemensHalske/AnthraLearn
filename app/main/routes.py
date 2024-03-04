from flask import Blueprint, render_template
from flask_jwt_extended import get_jwt_identity
from ..auth.routes import custom_jwt_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/index')
@main_bp.route('/')
@custom_jwt_required()
def home():
    return render_template('main/index.html', title='Home')


@main_bp.route('/about')
@custom_jwt_required(optional=True)
def about():
    current_user = get_jwt_identity()
    return render_template(
        'main/about.html',
        title='About',
        user=current_user
    )


@main_bp.route('/courses')
@custom_jwt_required()
def courses():
    current_user = get_jwt_identity()
    return render_template(
        'main/courses.html',
        title='Courses',
        user=current_user
    )


@main_bp.route('/contact')
@main_bp.route('/contact-us')
@custom_jwt_required(optional=True)
def contact():
    current_user = get_jwt_identity()
    return render_template(
        'main/contact.html',
        title='Contact', user=current_user
    )
