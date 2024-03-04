from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    EmailField, TelField, DateField
)
from wtforms.validators import DataRequired, Email, Length
from flask import (
    redirect, render_template, url_for,
    flash, request, jsonify
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


def custom_jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            print(f'Current user: {current_user}')
        except Exception as e:
            # If JWT is missing or invalid, redirect to the login page
            print('Exception:', e)
            return redirect(url_for('auth.login'))
        return fn(*args, **kwargs)
    return wrapper


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
            # Example user lookup
            user = User.query.filter_by(email=form.email.data).first()

            # Verify password (make sure to hash passwords in your database!)
            if user and check_password_hash(
                    user.passwordhash,
                    form.password.data):
                # Create JWT token
                access_token = create_access_token(identity=form.email.data)

                # Create response object
                response = jsonify({'login': True})
                # Set the JWT cookie in the response
                set_access_cookies(response, access_token)

                # Redirect to main index upon successful login
                return redirect(url_for('main.home'))
            else:
                flash('Bad username or password', 'warning')
    else:
        form = LoginForm()

    # GET request, failed form validation, or failed login attempt
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
