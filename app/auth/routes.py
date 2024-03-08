from datetime import datetime
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    EmailField, TelField, DateField
)
from wtforms.validators import DataRequired, Email, Length
from flask import (
    redirect, render_template, url_for,
    flash, request, jsonify,
    make_response, current_app
)
from wtforms.validators import ValidationError
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from flask_jwt_extended import (
    create_access_token, set_access_cookies,
    unset_jwt_cookies, jwt_required, get_jwt_identity
)

from urllib.parse import urlparse, urljoin

from ..models import db, User


auth_bp = Blueprint('auth', __name__)


class ComplexPasswordValidator:
    def __call__(self, form, field):
        password = field.data
        # Beispielbedingung: Das Passwort muss mindestens eine Ziffer enthalten
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                'Das Passwort muss mindestens eine Ziffer enthalten.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    contact = TelField('Contact Number (Optional)')
    dob = DateField('Date of Birth', validators=[DataRequired()])
    submit = SubmitField('Register')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


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
            if user and check_password_hash(user.passwordhash, form.password.data):
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

    return render_template('auth/login.html', title='Login', form=form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    print('Logout request received')
    response = make_response(redirect(url_for('auth.login')))
    unset_jwt_cookies(response)
    response.delete_cookie('AnthraLearn_session')
    # Setze die notwendigen Header, um Caching zu verhindern
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
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
@jwt_required()
def settings():
    # Holen Sie sich die Identität aus dem JWT-Token, die die E-Mail-Adresse sein sollte
    current_user_email = get_jwt_identity()

    # Suchen Sie nach dem Benutzer in der Datenbank mit der E-Mail-Adresse
    user = User.query.filter_by(email=current_user_email).first()
    if user:
        # Machen Sie etwas mit dem Benutzerobjekt ...
        return render_template('auth/settings.html', user=user)
    else:
        return render_template('auth/settings.html')
