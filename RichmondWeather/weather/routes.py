from weather import app
from flask import render_template, redirect, url_for, flash, request
from weather.models import Weather, User
from weather.forms import RegisterForm, LoginForm
from weather import db
from flask_login import login_user, logout_user, login_required
from weather.weather_bot import get_weather

#home page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

#weather page
@app.route('/weather')
@login_required #requires login to view page, can be deleted.
def weather_page():
    get_weather() #causes webscraper to run when page is refreshed

#retrieve weather channel temp and conditions from database
    for weather_channel_temp in Weather.query.filter_by(source='Weather Channel').all():
        weather_channel_temp = weather_channel_temp
    for weather_channel_conditions in Weather.query.filter_by(source='Weather Channel').all():
        weather_channel_conditions = weather_channel_conditions

#retrieve wunderground temp and conditions from database
    for wunderground_temp in Weather.query.filter_by(source='Wunderground').all():
        wunderground_temp = wunderground_temp
    for wunderground_conditions in Weather.query.filter_by(source='Wunderground').all():
        wunderground_conditions = wunderground_conditions

#retrieve noaa temp and conditions from database
    for noaa_temp in Weather.query.filter_by(source='NOAA').all():
        noaa_temp = noaa_temp
    for noaa_conditions in Weather.query.filter_by(source='NOAA').all():
        noaa_conditions = noaa_conditions

#retrieve local conditions temp and conditions from database
    for local_conditions_temp in Weather.query.filter_by(source='Local Conditions').all():
        local_conditions_temp = local_conditions_temp
    for conditions_local_conditions in Weather.query.filter_by(source='Local Conditions').all():
        conditions_local_conditions = conditions_local_conditions

#retrieve average temp from database
    for average_temp in Weather.query.filter_by(source='Average').all():
        average_temp = average_temp

    return render_template('weather.html',
                           weatherchanneltemp=weather_channel_temp.temperature,
                           weatherchannelconditions=weather_channel_conditions.conditions,
                           wundergroundtemp=wunderground_temp.temperature,
                           wundergroundconditions=wunderground_conditions.conditions,
                           noaatemp=noaa_temp.temperature,
                           noaaconditions=noaa_conditions.conditions,
                           localconditionstemp=local_conditions_temp.temperature,
                           conditionslocalconditions=conditions_local_conditions.conditions,
                           averagetemp=average_temp.temperature)

#login page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    #checks login against SQL database
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('weather_page'))
        else:
            flash('Username and password do not match! Please try again', category='danger')

    return render_template('login.html', form=form)

#contact page
@app.route('/contact')
def contact_page():
    return render_template('contact.html')

#register page
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    #form enters new user into SQL database
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('weather_page'))
    if form.errors != {}:  # If there are errors in the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

#logout
@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

#test page for trying out new things
@app.route('/test')
def test_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('weather_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('test.html', form=form)


