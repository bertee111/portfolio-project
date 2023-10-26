from flask import render_template, flash, redirect, url_for, request, Flask, redirect
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EventForm
from app.models import User, Event, Enrollment
from sqlalchemy import func
from sqlalchemy.sql import alias
import sqlite3
from wtforms.fields import DateField
from datetime import timedelta, date, time, datetime


appName = 'TVINING'
appTitle = 'Welcome to ' + appName
appSlogan = 'A simple way to join with activities'


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', appName=appName, appTitle=appTitle, appSlogan=appSlogan, title='Home', posts=posts)

def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/event', methods=['POST', 'GET'])
@app.route('/event/<event_id>', methods=['POST', 'GET'])
@login_required
def event(event_id=0):
    global appName, appSlogan, appTitle, db
    form = EventForm()
    form_data = request.form
    print(request)  

    if request.method == 'POST':
        if event_id == 0 and form_data['eventMethod'] != 'delete':
            # date_object = datetime.strptime((request.form['date']), '%Y-%m-%d')

            print('je insert')
            new_event = Event(title=form.title.data, date=datetime.strptime((request.form['date']), '%Y-%m-%d'), user_id=current_user.id)
            db.session.add(new_event)
            db.session.commit()
            flash('Event created successfully!', 'success')

            return redirect('/user-events')
        
        elif form_data['eventMethod'] == 'delete':
            print('je delete')
            event_id_to_delete = form_data['theEventId']
            event_to_delete = Event.query.filter(Event.id == event_id_to_delete).first()
            db.session.delete(event_to_delete)
            db.session.commit()
            enrollments_to_delete = Enrollment.query.filter(Enrollment.event_id == event_id_to_delete ).all()
            for enrollment in enrollments_to_delete:
                db.session.delete(enrollment)
                db.session.delete(event_to_delete)
                db.session.commit()
            return redirect('/user-events')
        elif event_id != 0: 
            print('je update')
            form = Event.query.get(event_id)
            # myDate = datetime.utcnow() working 
            # myDate = '2023-10-23' not working 

            print(request.form)
            form.title = (request.form['title'])
            form.date = datetime.strptime((request.form['date']), '%Y-%m-%d')
            print(request.form['title'])

            db.session.commit()




            return redirect('/user-events')

    elif request.method == 'GET':
        if event_id == 0:
            print('je get ajout')
        else:
            print('je get update' + str(event_id))
            currentEvent = db.session.query(
            Event.user_id,
            Event.id,
            Event.date,
            Event.title,        
            ).filter(
            Event.id == event_id
            ).first()
            form.title.data = currentEvent.title
            print(currentEvent)
            print(currentEvent.date)

            form.date.data = currentEvent.date
            # form.date.data = datetime.strftime('2011-03-07','%Y-%m-%d')
            # form.date.data = datetime.date(2011, 3, 7) not working!
            # form.date.data = datetime.strptime(datetime.date(2011, 3, 7)) NOT WORKING
            # formatted_date = currentEvent.date.strftime('%Y-%m-%d')
            # print(formatted_date)
            # form.date.data = formatted_date


            # form.date.data = '2023-10-01' not working!
            # form.date.data = datetime.strptime((currentEvent.date), '%Y-%m-%d') not working!
            # TODO fix date

        return render_template('event.html',appName=appName, appTitle=appTitle, appSlogan=appSlogan, form=form)


        

        # print(currentEvent)
        # print(str(currentEvent.date))



        # event_start_time = datetime(2023, 3, 1, 18, 15)
        # formatted_date = event_start_time.strftime('%Y-%m-%d')
        # parsed_date = datetime.strptime(formatted_date, '%Y-%m-%d')

        # form.date.data = parsed_date
        # print(parsed_date)
        # print(currentEvent.id)
   




@app.route('/user-events', methods=['GET', 'POST', 'UPDATE'])
@login_required
def userEvents():
    global appName, appSlogan, appTitle, db
    user_id = current_user.id
    

    userEvents = db.session.query(
        Event.user_id,
        Event.id,
        User.username.label("owner"),
        Event.date,
        Event.title,        
        func.count(Enrollment.user_id).label('participants')
    ).outerjoin(User, Event.user_id == User.id
    ).outerjoin(Enrollment, Event.id == Enrollment.event_id
    ).filter(
        Event.user_id == user_id
    ).group_by(
        Event.user_id,
        Event.date,
        Event.title
    ).order_by(
         func.count(Enrollment.user_id).label('participants').desc(),
         Event.title
    ).all()

    return render_template(
        'user-events.html', 
        appName=appName, 
        appTitle=appTitle, 
        appSlogan=appSlogan, 
        userEvents=userEvents 
    ) 

    

@app.route('/user-enrollments', methods=['GET', 'POST', 'UPDATE'])
def userEnrollments():
    global appName, appSlogan, appTitle, db
    user_id = current_user.id
    userEnrollmentsAlias = alias(Enrollment)
    userEnrollments = db.session.query(
        Enrollment.id, 
        Event.title,
        Event.date,
        Event.id.label('eventId'),
        User.username.label('owner'),
        func.count(userEnrollmentsAlias.c.user_id).label('participants')
    ).outerjoin(User, User.id == Enrollment.user_id
    ).outerjoin(Event, Enrollment.event_id == Event.id
    ).outerjoin(userEnrollmentsAlias, Enrollment.event_id == userEnrollmentsAlias.c.event_id
    ).group_by(Enrollment.id, Event.title, Event.date, Event.id, User.username
    ).filter(Enrollment.user_id == user_id               
    ).all()

    return render_template(
        'user-enrollments.html',
        appName=appName,
        appTitle=appTitle,
        appSlogan=appSlogan,
        userEnrollments=userEnrollments)


@app.route('/event-enrollment', methods=['GET'])
@app.route('/event-enrollment/<event_id>', methods=['GET'])
@login_required
def eventEnrollments(event_id=0):
    global appName, appSlogan, appTitle, db
    eventEnrollments = db.session.query(
        Enrollment.id, 
        Event.title,
        Event.date,
        User.username.label('enroller'),
    ).outerjoin(User, User.id == Enrollment.user_id
    ).outerjoin(Event, Enrollment.event_id == Event.id
    ).filter(Event.id == event_id           
    ).all()
    eventTitle = eventEnrollments[0].title

    return render_template(
        'event-enrollments.html',
        appName=appName,
        appTitle=appTitle,
        appSlogan=appSlogan,
        eventTitle=eventTitle,
        eventEnrollments=eventEnrollments,
        )




@app.route('/login', methods=['GET', 'POST'])
def login():
    global appName, appSlogan, appTitle 

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', appName=appName, appSlogan=appSlogan, appTitle=appTitle, form=form)
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', appName=appName, appTitle=appTitle, appSlogan=appSlogan, form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)



@app.route('/enrollment', methods=['POST', 'GET'])
@app.route('/enrollment/<enrollment_id>', methods=['POST', 'GET'])
@login_required
def enrollment(enrolment_id=0):
    return('123')