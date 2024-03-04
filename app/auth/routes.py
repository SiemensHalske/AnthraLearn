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
    make_response
)
from wtforms.validators import ValidationError
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from flask_jwt_extended import (
    create_access_token, set_access_cookies,
    verify_jwt_in_request, unset_jwt_cookies,
    get_jwt_identity
)
from functools import wraps

from ..models import db, User


auth_bp = Blueprint('auth', __name__)


def custom_jwt_required(optional=False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if optional:
                try:
                    verify_jwt_in_request(optional=True)
                    current_user = get_jwt_identity()
                except Exception as e:
                    # Falls JWT fehlt oder ungültig ist,
                    # einfach die Funktion ohne Weiterleitung aufrufen
                    print('Optional check failed:', e)
            else:
                try:
                    verify_jwt_in_request()
                    current_user = get_jwt_identity()
                    print(f'Current user: {current_user}')
                except Exception as e:
                    # Wenn JWT fehlt oder ungültig ist,
                    # leite zur Login-Seite weiter
                    print('Exception:', e)
                    return redirect(url_for('auth.login'))
            return fn(*args, **kwargs)
        return wrapper
    return decorator


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


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()

            if user and check_password_hash(
                    user.passwordhash,
                    form.password.data):
                access_token = create_access_token(identity=form.email.data)

                # Erstellen Sie eine Antwort und
                # setzen Sie das access_token-Cookie
                response = make_response(redirect(url_for('main.home')))
                set_access_cookies(response, access_token)

                # Redirect to main index upon successful login
                return response
            else:
                flash('Bad username or password', 'warning')
    else:
        form = LoginForm()

    return render_template('auth/login.html', title='Login', form=form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    response = jsonify({"logout": True})
    unset_jwt_cookies(response)
    return response


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
