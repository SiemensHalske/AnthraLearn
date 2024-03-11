from datetime import datetime
from flask import Blueprint
from flask import (
    redirect, render_template, url_for,
    flash, request, make_response,
    current_app
)
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from flask_jwt_extended import (
    create_access_token, set_access_cookies,
    unset_jwt_cookies, verify_jwt_in_request,
    get_jwt_identity, jwt_required
)

from urllib.parse import urlparse, urljoin
from time import sleep

from ..models import db, User, Course, CourseEnrollment
from ..main.routes import check_token

from app.forms.EnrollmentForm import EnrollmentForm
from app.forms.RegistrationForm import RegistrationForm
from app.forms.LoginForm import LoginForm


auth_bp = Blueprint('auth', __name__)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    is_url_safe = test_url.scheme in (
        'http', 'https') and ref_url.netloc == test_url.netloc
    return is_url_safe


def redirect_to_next(default='main.home'):
    next_page = request.args.get('next')
    # Stelle sicher, dass der Endpunkt existiert und vermeide Open Redirects
    if next_page and next_page in current_app.url_map._rules_by_endpoint:
        return redirect(url_for(next_page))
    return redirect(url_for(default))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(
                user.passwordhash,
                form.password.data
            ):

                # set is_authenticated attribute
                # for user to True
                try:
                    user.is_authenticated = True
                    db.session.commit()
                except Exception as e:
                    print(
                        f'Could not set user as authenticated in database: {e}'
                    )
                    flash('Could not set user as authenticated', 'danger')
                    sleep(3)
                    return redirect(url_for('auth.login'))

                access_token = create_access_token(identity=form.email.data)
                response = make_response(redirect(url_for('main.home')))
                set_access_cookies(response, access_token)
                next_page = request.args.get('next')
                if next_page and is_safe_url(next_page):
                    return redirect_to_next()

                return response
            else:
                flash('Bad username or password', 'warning')
    else:
        form = LoginForm()

    return render_template(
        'auth/login.html',
        title='Login',
        user=None,
        form=form
    )


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    print('Logout request received')
    response = make_response(redirect(url_for('auth.login')))
    unset_jwt_cookies(response)
    response.delete_cookie('AnthraLearn_session')
    # Setze die notwendigen Header, um Caching zu verhindern
    response.headers['Cache-Control'] = \
        'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@auth_bp.route('/register', methods=['GET', 'POST'])
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        new_user = User(
            username=form.first_name.data + form.last_name.data,
            passwordhash=password_hash,
            email=form.email.data,
            dateofbirth=form.dob.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        # Redirect to login page after successful registration
        return redirect(url_for('auth.login'))
    elif request.method == 'POST':
        flash(
            'Registration failed. Please check your inputs and try again.',
            'danger'
        )

    return render_template('auth/signup.html', title='Register', form=form)

# ======================================================
# ===================== ROUTES =========================
# ======================================================


@auth_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    # Holen Sie sich die Identität aus dem JWT-Token,
    # die die E-Mail-Adresse sein sollte
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()

    current_user_email = current_user.get('identity', None)

    user = User.query.filter_by(email=current_user_email).first()

    if user:
        return render_template('auth/settings.html', user=user)
    else:
        return render_template('auth/settings.html', user=None)


@auth_bp.route('/enroll/<int:courseid>', methods=['GET', 'POST'])
def enroll(courseid):
    def failed(courseid: int, userid: str, reason: str):
        if userid is None:
            userid = ''
        return redirect(
            url_for(
                'auth.enrollment_failed',
                courseid=courseid,
                userid=userid,
                reason=reason
            )
        )

    # Check session and request header
    print('\n'*5)
    print(f'request: {request}')
    print(f'form: {request.form}')
    print(f'args: {request.args}')
    print(f'headers: {request.headers}')
    print(f'cookies: {request.cookies}')
    print(f'Authorization: {request.headers.get("Authorization")}')
    print('\n'*5)

    verify_jwt_in_request()
    user_id = get_jwt_identity()
    user = None

    form = EnrollmentForm(courseid=courseid)
    if form.validate_on_submit():

        print(f'user: {user}')

        course = Course.query.get(courseid)
        if not course:
            return failed(courseid, user_id, 'course_not_found')

        # Check if user is alread in CourseEnrollment
        if CourseEnrollment.query.filter_by(
            courseid=courseid,
            userid=user_id
        ).count() > 0:
            return failed(courseid, user_id, 'already_enrolled')

        print('\n'*3)
        print(f'user: {user_id}')
        print(f'course: {courseid}')
        print('\n'*3)

        user = User.query.filter_by(email=user_id).first()

        print('\n'*3)
        print(f'user: {user_id}')
        print(f'course: {course}')
        print('\n'*3)

        if not user or not course:
            return failed(
                courseid=courseid,
                userid=user_id,
                reason='user_or_course_not_found'
            )

        try:
            enrollment = CourseEnrollment(
                userid=user_id,
                courseid=courseid,
                enrollmentdate=datetime.utcnow()
            )
            db.session.add(enrollment)
            db.session.commit()
        except Exception as e:
            print(f'Could not add user to course: {e}')
            return failed(courseid, user_id, 'could_not_add_user')

        return redirect(
            url_for(
                'auth.enrollment_success',
                courseid=courseid,
                userid=user_id,
                reason='enrollment_success'
            )
        )

    identity_tuple = check_token(request)
    if identity_tuple['identity']:
        user = User.query.filter_by(
            email=identity_tuple.get('identity', None)).first()
    else:
        user = None

    reason = 'You are not logged in!'

    return render_template(
        'main/enroll.html',
        form=form,
        courseid=courseid,
        user=user,
        reason=reason
    )


@auth_bp.route(
    '/enrollment_failed/<int:courseid>/<string:userid>/<string:reason>')
def enrollment_failed(courseid: int, userid: str, reason: str):
    user = User.query.filter_by(email=userid).first()
    return render_template(
        'main/enrollment_failed.html',
        course_id=courseid,
        user=user,
        reason=reason
    )


@auth_bp.route(
    '/enrollment_success/<int:courseid>/<string:userid>/<string:reason>')
def enrollment_success(courseid: int, userid: str, reason: str):
    user = User.query.filter_by(email=userid).first()
    return render_template(
        'main/enrollment_success.html',
        course_id=courseid,
        user=user,
    )
