from datetime import datetime

from sqlalchemy import orm
from werkzeug.security import check_password_hash, generate_password_hash

from api.server import db


class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    _password = db.Column('password', db.String(255))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
            self._password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = orm.synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        if self.password is None:
            return False
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, email, password):
        email = email.strip().lower()
        user = query(cls).filter(cls.email == email).first()
        if user is None:
            return None, False
        if not user.active:
            return user, False
        return user, user.check_password(password)


class InterviewCandidate(db.Model):
    __tablename__ = "interview_candidate"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    resume_link = db.Column(db.String(255))


class Interviewer(db.Model):
    __tablename__ = "interviewer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    reviews = db.Column(db.String(255))


class InterviewDetails(db.Model):
    __tablename__ = "interview_details"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    interviewer_id = db.Column(db.Integer, db.ForeignKey('interviewer.id', ondelete='SET NULL'))
    interviewee_id = db.Column(db.Integer, db.ForeignKey('interview_candidate.id', ondelete='SET NULL'))
    start_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    is_cancelled = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id', ondelete='SET NULL'))