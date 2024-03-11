from flask import (
    Blueprint, render_template, request
)
from flask_jwt_extended import (
    get_jwt_identity, verify_jwt_in_request
)
from flask import redirect, url_for

from app.models import User, Course
from app.extensions import jwt_required_optional

from ..forms.EnrollmentForm import EnrollmentForm

main_bp = Blueprint('main', __name__)

# ================================================================
# ================== Helper methods ==============================
# ================================================================


def check_token(optional=False):
    identity_dict = {
        'message': 'invalid',
        'identity': None
    }

    try:
        verify_jwt_in_request(optional=optional)
        identity = get_jwt_identity()

        identity_dict['message'] = 'valid'
        identity_dict['identity'] = identity

    except Exception as e:
        print('JWT not found or invalid')
        print(e)

    return identity_dict


# ================================================================
# ======================== NavBar ================================
# ================================================================


@main_bp.route('/index')
@main_bp.route('/')
def home():
    def show_index_page(current_user):
        return render_template(
            'main/index_2.html',
            title='Home',
            user=current_user
        )
    # Versucht, den JWT in der Anfrage zu verifizieren
    current_user = check_token()
    username = current_user['identity'] or None
    print(f'Current User: {username}')

    user = User.query.filter_by(email=username).first()

    if user:
        return show_index_page(current_user=user)
    else:
        print('No current user')
        return show_index_page(current_user=None)


@main_bp.route('/courses')
def courses():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()

    user = User.query.filter_by(email=current_user).first()

    courses = Course.query.all()
    form = EnrollmentForm(courseid=None)
    return render_template(
        'main/courses.html',
        title='Courses',
        user=user if user else None,
        courses=courses,
        form=form
    )


@main_bp.route('/about')
def about():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()

    user = User.query.filter_by(email=current_user).first()

    return render_template(
        'main/about.html',
        title='About',
        user=user
    )


@main_bp.route('/contact')
@main_bp.route('/contact-us')
def contact():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()

    user = User.query.filter_by(email=current_user).first()

    return render_template(
        'main/contact.html',
        title='Contact',
        user=user
    )


@main_bp.route('/gettoknowus')
def gettoknowus():
    return redirect(url_for('main.about'))

# ================================================================
# ======================== Footer ================================
# ================================================================


@main_bp.route('/sitemap')
def sitemap():
    return render_template(
        'main/sitemap.html',
        title='Sitemap',
    )


@main_bp.route('/terms')
def terms():
    return render_template(
        'main/terms.html',
        title='Terms',
    )


@main_bp.route('/privacy')
def privacy():
    return render_template(
        'main/privacy.html',
        title='Privacy',
    )


@main_bp.route('/disclaimer')
def disclaimer():
    return render_template(
        'main/disclaimer.html',
        title='Disclaimer',
    )


# ================================================================
# ======================== Routes ================================
# ================================================================

@main_bp.route('/user_profile', methods=['GET', 'POST'])
@jwt_required_optional()
def user_profile():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()

    if user:
        return render_template('main/user_profile.html', user=user)
    else:
        return redirect(url_for('main.home'))


@main_bp.route('/course/<course_id>')
def course(course_id):
    form = EnrollmentForm(course_id=course_id)
    return render_template('course.html', form=form, course_id=course_id)
