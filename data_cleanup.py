from app import app, db
from app.models import Event, Enrollment, User
from sqlalchemy import delete, insert
from datetime import datetime
from werkzeug.security import generate_password_hash

try:
    with app.app_context():
        # DELETING ALL ENROLLMENTS, EVENTS, USERS
        db.session.execute(delete(Enrollment))
        db.session.execute(delete(Event))
        db.session.execute(delete(User))
        db.session.commit()

        # ADDING USER
        psw = generate_password_hash('123')
        db.session.execute(
            insert(User),
            [
                {"username": "paul", "email": "paul@beatles.com", "password_hash": psw},
                {"username": "john", "email": "john@beatles.com", "password_hash": psw},
                {"username": "george", "email": "george@beatles.com", "password_hash": psw},
                {"username": "ringo", "email": "ringo@beatles.com", "password_hash": psw},
            ]
        )
        db.session.commit()
        
        # ADDING EVENT
        db.session.execute(
            insert(Event),
            [
                {"user_id": 2, "title": "Boxe", "date": datetime.today()},
                {"user_id": 2, "title": "Karate", "date": datetime.today()},
                {"user_id": 2, "title": "Judo", "date": datetime.today()},
                {"user_id": 2, "title": "Kendo", "date": datetime.today()},
                {"user_id": 3, "title": "Rock", "date": datetime.today()},
                {"user_id": 3, "title": "Disco", "date": datetime.today()},
                {"user_id": 3, "title": "Techno", "date": datetime.today()},
                {"user_id": 3, "title": "Classical", "date": datetime.today()}
            ]
        )
        db.session.commit()

        # ADDING ENROLLMENT
        db.session.execute(
            insert(Enrollment),
            [
                {"user_id": 1, "event_id": 6, "date": datetime.today()},
                {"user_id": 2, "event_id": 6, "date": datetime.today()},
                {"user_id": 3, "event_id": 6, "date": datetime.today()},
                {"user_id": 1, "event_id": 2, "date": datetime.today()},
                {"user_id": 2, "event_id": 4, "date": datetime.today()},
                {"user_id": 1, "event_id": 3, "date": datetime.today()}                   
            ]
        )
        db.session.commit()

        # ADDING USER

    # id = db.Column(db.Integer, primary_key=True)
    # #event_id = db.Column(db.Integer, db.ForeignKey('event.id', name='fk_user_event'), nullable=False)
    # #enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.id', name='fk_user_enrollment'), nullable=False)
    # username = db.Column(db.String(64), index=True, unique=True)
    # email = db.Column(db.String(120), index=True, unique=True)
    # password_hash = db.Column(db.String(128))

except Exception as error:
    # handle the exception
    print("An exception occurred:", error)  