from datetime import datetime
from flask import request, current_app
from flask_sqlalchemy import SQLAlchemy

import jwt
from jwt.exceptions import InvalidTokenError

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    passwordhash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    profilepicture = db.Column(db.String(255))
    registrationdate = db.Column(
        db.Date, nullable=False, default=datetime.utcnow)
    dateofbirth = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def get_roles(self):
        return UserRole.query.filter_by(UserID=self.UserID).all()

    def get_progress(self):
        return UserProgress.query.filter_by(UserID=self.UserID).all()

    def get_submissions(self):
        return Submission.query.filter_by(UserID=self.UserID).all()

    def get_feedbacks(self):
        return Feedback.query.filter_by(UserID=self.UserID).all()

    @staticmethod
    def verify_jwt(jwt_token):
        try:
            payload = jwt.decode(
                jwt_token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            return True, payload
        except InvalidTokenError:
            return False, {}

    @staticmethod
    def get_jwt_from_cookie():
        jwt_cookie = request.cookies.get(
            current_app.config['JWT_ACCESS_COOKIE_NAME']
        )
        return jwt_cookie

    def is_user_authenticated(self):
        print('Is user authenticated?')
        jwt_cookie = self.get_jwt_from_cookie()
        if jwt_cookie:
            valid, payload = self.verify_jwt(jwt_cookie)
            return valid, payload
        else:
            return False, 'default'


class Role(db.Model):
    __tablename__ = 'roles'

    roleid = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"Role('{self.RoleName}')"


class UserRole(db.Model):
    __tablename__ = 'user_roles'

    userid = db.Column(db.Integer, db.ForeignKey(
        'users.UserID'), primary_key=True)
    roleid = db.Column(db.Integer, db.ForeignKey(
        'roles.RoleID'), primary_key=True)

    def __repr__(self):
        return f"UserRole('{self.UserID}', '{self.RoleID}')"


class Course(db.Model):
    __tablename__ = 'courses'

    courseid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    creatorid = db.Column(db.Integer, db.ForeignKey(
        'users.UserID'), nullable=False)
    publicationdate = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f"Course('{self.title}', '{self.status}')"

    def get_modules(self):
        return Module.query.filter_by(CourseID=self.courseid).all()

    def get_progress(self):
        return UserProgress.query.filter_by(CourseID=self.courseid).all()

    def get_feedbacks(self):
        return Feedback.query.filter_by(CourseID=self.courseid).all()


class CourseEnrollment(db.Model):
    __tablename__ = 'courseenrollments'

    enrollmentid = db.Column(db.Integer, primary_key=True)
    courseid = db.Column(db.Integer, db.ForeignKey(
        'courses.courseid'), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey(
        'users.userid'), nullable=False)
    enrollmentdate = db.Column(db.Date)

    # Die UNIQUE-Constraint könnte auch über SQLAlchemy definiert werden,
    # aber da der SQL Befehl bereits ein Teil davon ist,
    # ist es hier nicht unbedingt nötig.

    def __init__(self, courseid, userid, enrollmentdate):
        self.courseid = courseid
        self.userid = userid
        self.enrollmentdate = enrollmentdate


class Module(db.Model):
    __tablename__ = 'modules'

    moduleid = db.Column(db.Integer, primary_key=True)
    courseid = db.Column(db.Integer, db.ForeignKey(
        'courses.CourseID'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    sequence = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Module('{self.Title}', '{self.Sequence}')"

    def get_lessons(self):
        return Lesson.query.filter_by(ModuleID=self.ModuleID).all()


class Lesson(db.Model):
    __tablename__ = 'lessons'

    LessonID = db.Column(db.Integer, primary_key=True)
    ModuleID = db.Column(db.Integer, db.ForeignKey(
        'modules.ModuleID'), nullable=False)
    Title = db.Column(db.String(255), nullable=False)
    ContentType = db.Column(db.String(50), nullable=False)
    Content = db.Column(db.Text, nullable=False)
    Sequence = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        title = self.Title
        ctype = self.ContentType
        sequence = self.Sequence
        return f"Lesson('{title}', '{ctype}', '{sequence}')"


class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    ProgressID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey(
        'users.UserID'), nullable=False)
    CourseID = db.Column(db.Integer, db.ForeignKey(
        'courses.CourseID'), nullable=False)
    Status = db.Column(db.String(50), nullable=False)
    CompletionDate = db.Column(db.Date)

    def __repr__(self):
        uid = self.UserID
        cid = self.CourseID
        status = self.Status
        return f"UserProgress('{uid}', '{cid}', '{status}')"


class Assignment(db.Model):
    __tablename__ = 'assignments'

    AssignmentID = db.Column(db.Integer, primary_key=True)
    LessonID = db.Column(db.Integer, db.ForeignKey(
        'lessons.LessonID'), nullable=False)
    Title = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    DueDate = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"Assignment('{self.Title}', '{self.DueDate}')"


class Submission(db.Model):
    __tablename__ = 'submissions'

    SubmissionID = db.Column(db.Integer, primary_key=True)
    AssignmentID = db.Column(db.Integer, db.ForeignKey(
        'assignments.AssignmentID'), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey(
        'users.UserID'), nullable=False)
    SubmissionDate = db.Column(db.Date, nullable=False)
    File = db.Column(db.String(255))
    Grade = db.Column(db.Integer)
    Feedback = db.Column(db.Text)

    def __repr__(self):
        return f"Submission('{self.SubmissionDate}', '{self.Grade}')"


class DiscussionForum(db.Model):
    __tablename__ = 'discussion_forums'

    PostID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, db.ForeignKey(
        'courses.CourseID'), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey(
        'users.UserID'), nullable=False)
    Title = db.Column(db.String(255), nullable=False)
    Content = db.Column(db.Text, nullable=False)
    CreationDate = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"DiscussionForum('{self.Title}', '{self.CreationDate}')"


class AdminUser(db.Model):
    __tablename__ = 'admin_users'

    AdminUserID = db.Column(db.Integer, db.ForeignKey(
        'users.UserID'), primary_key=True)
    AdminRole = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"AdminUser('{self.AdminRole}')"


class CourseAccessRight(db.Model):
    __tablename__ = 'course_access_rights'

    AccessID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, db.ForeignKey(
        'courses.CourseID'), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey(
        'users.UserID'), nullable=False)

    def __repr__(self):
        return f"CourseAccessRight('{self.CourseID}', '{self.UserID}')"


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    LogID = db.Column(db.Integer, primary_key=True)
    ActivityType = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey(
        'users.UserID'), nullable=False)
    DateTime = db.Column(db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return f"AuditLog('{self.ActivityType}', '{self.DateTime}')"


class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    FeedbackID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, db.ForeignKey(
        'courses.CourseID'), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey(
        'users.UserID'), nullable=False)
    Rating = db.Column(db.Integer, nullable=False)
    Comment = db.Column(db.Text)
    DateTime = db.Column(db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return f"Feedback('{self.Rating}', '{self.DateTime}')"


class CourseMaterial(db.Model):
    __tablename__ = 'coursematerials'

    materialid = db.Column(db.Integer, primary_key=True)
    courseid = db.Column(db.Integer, db.ForeignKey(
        'courses.courseid'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    filepath = db.Column(db.String(255), nullable=True)
    uploadedat = db.Column(db.DateTime, default=datetime.utcnow)
    access_rivileges = db.Column(db.String(50), nullable=True)

    # course = db.relationship('Course', back_populates='coursematerials')

    # Include any additional methods and representation
    # of the model if necessary
    def __repr__(self):
        m_id = self.material_id
        title = self.title
        course = self.course_id
        return f"<CourseMaterial(material_id={m_id}, title={title}, course_id={course})>"
