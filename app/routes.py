from flask import render_template, flash, redirect, url_for, request, Flask, redirect
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EventForm
from app.models import User, Event, Enrollment
from sqlalchemy import func
import sqlite3

#appName = 'My global appName TVINING'
#appTitle = 'My global appTitle : ' + appName
#appSlogan = 'My global appSlogan...to be or not to be'

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

#@user.route('/<user_id>', defaults={'username': default_value})
#@user.route('/<user_id>/<username>')
#def show(user_id, username):

#@app.route("/<parameter>/<optional_parameter>")
#@app.route("/<parameter>")
#def route(parameter, optional_parameter="Default Value"):
#    return parameter + " " + optional_parameter



@app.route('/event', methods=['POST', 'GET'])
@app.route('/event/<event_id>', methods=['GET'])
@login_required
def event(event_id=0):
    global appName, appSlogan, appTitle, db
    if request.method == 'GET':
        form = EventForm()
        if form.validate_on_submit():
            new_event = Event(title=form.title.data,date=form.date.data,user_id=current_user.id
            )
            db.session.add(new_event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('event.htlm'))

        return render_template('event.html',appName=appName, appTitle=appTitle, appSlogan=appSlogan, form=form)
        # return render_template('event.html', appName=appName, appTitle=appTitle, appSlogan=appSlogan)

    elif request.method == 'POST':
        form_data = request.form
        if form_data['eventMethod'] == 'delete':
            event_to_delete = Event.query.filter(Event.id == form_data['theEventId']).first()
            db.session.delete(event_to_delete)
            db.session.commit()
    return redirect('/user-events')

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
        Enrollment.user_id == user_id
    ).group_by(
        Event.user_id,
        Event.id,
        User.username,
        Event.date,
        Event.title
    ).order_by(
        func.count(Enrollment.user_id).desc(),
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
    userEnrollments = db.session.query(
        Event.title,
        Event.date,
        User.username.label('owner'),
        func.count(Enrollment.user_id).label('participants')
    ).outerjoin(Enrollment, Event.id == Enrollment.event_id
    ).outerjoin(User, User.id == Event.user_id
    ).group_by(Event.user_id, Event.date
    ).order_by(
         func.count(Enrollment.user_id).label('participants').desc(),
         Event.title
    ).all()
    return render_template(
        'user-enrollments.html',
        appName=appName,
        appTitle=appTitle,
        appSlogan=appSlogan,
        userEnrollments=userEnrollments)

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