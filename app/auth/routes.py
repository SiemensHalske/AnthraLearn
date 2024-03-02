from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    EmailField, TelField, DateField
)
from wtforms.validators import DataRequired, Email, Length
from flask import redirect, render_template, url_for, flash
from wtforms.validators import ValidationError


class ComplexPasswordValidator:
    def __call__(self, form, field):
        password = field.data
        # Beispielbedingung: Das Passwort muss mindestens eine Ziffer enthalten
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                'Das Passwort muss mindestens eine Ziffer enthalten.')


class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    contact = TelField('Contact Number (Optional)')
    dob = DateField('Date of Birth', validators=[DataRequired()])
    submit = SubmitField('Register')


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    return "This is the login page."


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process the form data, create the user, etc.
        flash('Account created successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('signup.html', title='Signup', form=form)
