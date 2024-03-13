from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    DateField, TelField, EmailField
)
from wtforms.validators import DataRequired, Email, Length


class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    contact = TelField('Contact Number (Optional)')
    dob = DateField('Date of Birth', validators=[DataRequired()])
    submit = SubmitField('Register')
