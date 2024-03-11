from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms.validators import DataRequired


class EnrollmentForm(FlaskForm):
    courseid = HiddenField('Course ID', validators=[DataRequired()])

    def __init__(self, courseid, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        if courseid is not None:
            self.courseid.data = courseid
