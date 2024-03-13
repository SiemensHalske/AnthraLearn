from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms.validators import DataRequired


class EnrollmentForm(FlaskForm):
    courseid = HiddenField('Course ID', validators=[DataRequired()])
    userid = HiddenField('User ID', validators=[DataRequired()])

    def __init__(self, courseid, user, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        if user is not None:
            userid = user.username
            self.userid.data = userid
        if courseid is not None:
            self.courseid.data = courseid
