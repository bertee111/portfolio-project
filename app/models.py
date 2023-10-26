from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #event_id = db.Column(db.Integer, db.ForeignKey('event.id', name='fk_user_event'), nullable=False)
    #enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.id', name='fk_user_enrollment'), nullable=False)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_event_user'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # def __init__(self, user_id, title, date):
    #     self.user_id = user_id
    #     self.title = title
    #     self.date = date
    
    def __repr__(self):
        return '<Event {}>'.format(self.title)
    

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_enrollment_user'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', name='fk_enrollment_event'), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Enrollment {}>'.format(self.title)
    #    return '<Enrollment: User {} in Event {}>'.format(self.user_id, self.event_id)
