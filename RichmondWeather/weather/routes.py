from weather import app
from flask import render_template, redirect, url_for, flash, request
from weather.models import Weather


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/weather')
def weather_page():
    for weather_channel_temp in Weather.query.filter_by(source='Weather Channel').all():
            print(weather_channel_temp)

    for wunderground_temp in Weather.query.filter_by(source='Wunderground').all():
            print(wunderground_temp)

    for noaa_temp in Weather.query.filter_by(source='NOAA').all():
            print(noaa_temp)

    for local_conditions_temp in Weather.query.filter_by(source='Local Conditions').all():
            print(local_conditions_temp)

    for average_temp in Weather.query.filter_by(source='Average').all():
            print(average_temp)

    return render_template('weather.html',
                           weatherchanneltemp=weather_channel_temp.temperature,
                           wundergroundtemp=wunderground_temp.temperature,
                           noaatemp=noaa_temp.temperature,
                           localconditionstemp=local_conditions_temp.temperature,
                           averagetemp=average_temp.temperature)


@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/test')
def test_page():
    if request.method == 'GET':
        for weather_channel_temp in Weather.query.filter_by(source='Weather Channel').all():
            print(weather_channel_temp)

        for wunderground_temp in Weather.query.filter_by(source='Wunderground').all():
            print(wunderground_temp)

        for noaa_temp in Weather.query.filter_by(source='NOAA').all():
            print(noaa_temp)

        for local_conditions_temp in Weather.query.filter_by(source='Local Conditions').all():
            print(local_conditions_temp)

        for average_temp in Weather.query.filter_by(source='Average').all():
            print(average_temp)

    return render_template('weather.html',
                           weatherchanneltemp=weather_channel_temp.temperature,
                           wundergroundtemp=wunderground_temp.temperature,
                           noaatemp=noaa_temp.temperature,
                           localconditionstemp=local_conditions_temp.temperature,
                           averagetemp=average_temp.temperature)


