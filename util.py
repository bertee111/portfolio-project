from app import app, db
from app.models import User, Event
from datetime import datetime
app.app_context().push()
#a = Event(title='bike', date=datetime.utcnow(), user_id=1)
a = Event(title='tennis', date=datetime.utcnow(), user_id=48)
#a = Event(title='karaté', date=datetime.utcnow(), user_id=2)
db.session.add(a)
db.session.commit()
exit()