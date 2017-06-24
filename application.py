from flask import render_template
from flask import Flask, session, redirect, url_for
from flask import request
from flask.ext.session import Session
import json
from dateutil.parser import parse
from db_operations import (
    get_trip_by_id, create_trip, 
    create_user, create_tables,
    fill_test_data, get_trips,
    create_flight, add_user
)

from classy import Trip


app = Flask(__name__)
app.config.from_object(__name__)
sess = Session()

users = []
trips = []

with open('cities.json') as cities:
    cities = json.loads(cities.read())


@app.route('/load_cities', methods=['GET',])
def load_cities():
    name = request.args.get('name')
    filtered_cities = filter(lambda c: name in c['name'].lower(), cities)
    return json.dumps(list(map(lambda c: '{}, {}'.format(c['name'], c['country']), filtered_cities)))


@app.route('/', methods=['GET', 'POST'])
def index():
    register_template = 'index.html'
    if request.method == 'POST':
        data = request.form
        if data.get('register'):
            username = data.get('username')
            name = data.get('name')
            password = data.get('password')
            users.append({
                'username':username,
                'name':name,
                'password':password    
            })
            session['username'] = username
            session['name'] = name
            return render_template(
                    register_template, 
                    username=username, 
                    name=name
                )
        elif data.get('login'):
            username = data.get('username')
            password = data.get('password')
            if check_login(username, password):
                session['username'] = username
                session['name'] = name
                return render_template(
                    register_template, 
                    username=username, 
                    name=name
                )
        else:
            return render_template(register_template)
    elif session.get('username'):
        trip = {}
        return render_template(
            register_template, 
            username=session['username'], 
            name=session['name'],  trip=trip
        )
    return render_template(register_template)


@app.route('/logout', methods=['GET',])
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('index'))


@app.route('/trip-list', methods=['GET'])
def trip_list():
    data = request.args
    if len(data) == 0:
        return render_template('trip_list.html', trips=trips)
    results = filter(lambda tr: tr.dest == data.get('to') and tr.date == parse(data.get('date')).date(), trips)
    return render_template('trip_list.html', trips=results)

@app.route('/trip-detail', method=['GET',])
def trip_detail(trip_id):

    return render_template('trip_detail.html', )


@app.route('/about-us', methods=['GET'])
def about_us():
    return render_template('about_us.html')


@app.route('/new-trip', methods=['GET', 'POST'])
def new_trip():
    if request.method == 'POST':
        data = request.form
        trip = Trip(data.get('to'), parse(data.get('date')).date(), '14:00')
        trips.append(trip)
        return redirect(url_for('trip_list'))
    return render_template('new_trip.html')


def check_login(username, password):
    return True


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.debug = True
    app.run()
