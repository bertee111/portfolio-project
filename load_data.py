from app import app, db
from app.models import Event, User
from datetime import datetime

# Testing insert event with invalid user_id
try:
    with app.app_context():
        newEvent = Event(50, 'abc', datetime.utcnow())    
        db.session.add(newEvent)
        db.session.commit()        
except Exception as error:
    # handle the exception
    print("An exception occurred:", error) # An exception occurred

# try:
#     with app.app_context():
#         # myDate = datetime.utcnow() working 
#         # myDate = '2023-10-23' not working 
#         myDate = datetime.strptime('2023-10-23','%Y-%m-%d') #working
#         newEvent = Event(3, 'rat', myDate)    
#         db.session.add(newEvent)
#         db.session.commit()        
# except Exception as error:
#     # handle the exception
#     print("An exception occurred:", error) # An exception occurred  