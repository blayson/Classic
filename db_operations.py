#!/usr/bin/env python3

# for install psycopg2 for Python 3 use sudo apt-get install python3-psycopg2

from classy import *
import airport_codes
import psycopg2
import json

database_name = "test_database"
user_name = "test_master"
host_name = "test-database.cvzlexvifitu.eu-central-1.rds.amazonaws.com"
port = "5432"
passwd = "testpassword"

airports = {}
with open("airports.txt") as data_file:
    airports = json.loads(data_file.read())

conn = psycopg2.connect(dbname = database_name, user = user_name, host = host_name, port = port, password = passwd)
cur = conn.cursor()


create_tables_command = (
            """
                CREATE TABLE Users (
                    user_id SERIAL PRIMARY KEY,
                    name VARCHAR (50) NOT NULL,
                    surname VARCHAR (50) NOT NULL,
                    age INTEGER NOT NULL,
                    foto BYTEA,
                    contact TEXT
                )
            """,
            """
                CREATE TABLE Airport_City (
                    city_name VARCHAR (100) NOT NULL,
                    airport_abbr VARCHAR (4) PRIMARY KEY
                )
            """,
            """
                CREATE TABLE Trips (
                    trip_id SERIAL PRIMARY KEY,
                    dest VARCHAR (4) NOT NULL,
                    date DATE NOT NULL,
                    time TIME NOT NULL,
                    time_diff BIGINT NOT NULL,
                    max_cap INTEGER NOT NULL,

                    CONSTRAINT dest_to_airport_abbr FOREIGN KEY (dest)
                    REFERENCES Airport_City (airport_abbr) MATCH SIMPLE
                    ON UPDATE NO ACTION ON DELETE NO ACTION 
                )
            """,
            """
                CREATE TABLE Flights (
                    flight_id SERIAL PRIMARY KEY,
                    from_tmsp BIGINT NOT NULL,
                    to_tmsp BIGINT NOT NULL,
                    cost INTEGER NOT NULL,
                    duration INTEGER NOT NULL,
                    from_location VARCHAR (4) NOT NULL,
                    book_url TEXT,

                    CONSTRAINT from_loc_to_airport_abbr FOREIGN KEY (from_location)
                    REFERENCES Airport_City (airport_abbr) MATCH SIMPLE
                    ON UPDATE NO ACTION ON DELETE NO ACTION
                )
            """,
            """
                CREATE TABLE User_Trip (
                    user_id INTEGER NOT NULL,
                    trip_id INTEGER NOT NULL,

                    CONSTRAINT users_ids FOREIGN KEY (user_id)
                    REFERENCES Users (user_id) MATCH SIMPLE
                    ON UPDATE NO ACTION ON DELETE CASCADE,

                    CONSTRAINT trips_ids FOREIGN KEY (trip_id)
                    REFERENCES Trips (trip_id) MATCH SIMPLE
                    ON UPDATE NO ACTION ON DELETE CASCADE
              )
            """
    )

drop_tables = (
            """
            DROP TABLE User_Trip
            """,
            """
            DROP TABLE Users
            """,
            """
            DROP TABLE Trips
            """,
            """
            DROP TABLE Flights
            """,
            """
            DROP TABLE Airport_City
            """
    )
        
def create_user(user):
    add_user = (
            """
            INSERT INTO Users (name, surname, age, foto, contact)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING user_id
            """
        )
    user_info = (user.name, user.surname, user.age, user.foto_path, user.kontakt_path)
    cur.execute(add_user, user_info)
    user_id = cur.fetchone()[0]

    conn.commit()

    return user_id

def add_user(user, trip):
    add_usr = (
            """
            INSERT INTO User_Trip (user_id, trip_id)
            VALUES (%s, %s)
            """
        )
    cur.execute(add_usr, (user.id, trip.id))
    conn.commit()

def remove_user(user):
    rem_user = (
            """
            DELETE FROM User_Trip
            WHERE user_id = %s
            """
        )
    cur.execute(rem_user, (user.id,))
    conn.commit()


def create_trip(trip):
    add_trip = (
            """
            INSERT INTO Trips (dest, date, time, time_diff, max_cap)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING trip_id
            """
        )
    trip_info = (trip.dest, trip.date, trip.time, trip.time_diff, trip.max_cap)
    cur.execute(add_trip, trip_info)
    trip_id = cur.fetchone()[0]
    conn.commit()

    return trip_id

def create_flight(flight):
    add_flight = (
            """
            INSERT INTO Flights (from_tmsp, to_tmsp, cost, duration)
            VALUES (%s, %s, %s, %s)
            """
        )
    flight_info = (flight.from_tmsp, flight.to_tmsp, flight.cost, flight.duration)
    cur.execute(add_flight, flight_info)
    conn.commit()


def get_trips(city, date, time = None):
    trips = []
    try:
        airp_list = airports[city]
        for airport in airp_list:
            if time:
                select_trips = """ SELECT * FROM Trips WHERE dest = %s AND date = %s AND time = %s """
                trip_info = (airport, date, time)
            else:   
                select_trips = """ SELECT * FROM Trips WHERE dest = %s AND date = %s """
                trip_info = (airport, date)

            cur.execute(select_trips, trip_info)
            trip_list = cur.fetchall()

            for trip in trips_list:
                new_trip = Trip(trip[1], trip[2], trip[3], trip[4], trip[5])
                new_trip.id = trip[0]
                trips.append(new_trip)

    except (ValueError, FileNotFoundError):
        print("Trips are not found!")

    return trips


def get_trip_by_id(trip_id):
    select = (
            """
            SELECT * FROM Trips
            WHERE trip_id = %s
            """
        )
    cur.execute(select, (trip_id,))
    trip = cur.fetchone()[0]
    conn.commit()

    return Trip(trip[0], trip[1], trip[2], trip[3], trip[4], trip[5])

def get_partic(trip):
    users = []
    select_users = (
            """
            SELECT * FROM User_Trip NATURAL JOIN Users 
            WHERE User_Trip.trip_id = %s
            """
        )
    cur.execute(select_users, (trip.id,))
    user_list = cur.fetchall()
    for user in user_list:
        new_user = User(user[2], user[3], user[4], user[5], user[6])
        new_user.id = user[1]
        users.append(new_user)

    conn.commit()

    return users

def fill_test_data():
    create_user(User("Vova"), cur)
    create_user(User("Andrii"), cur)
    create_user(User("Lecha"), cur)
    create_user(User("Andrei"), cur)
    create_user(User("Pavel"), cur)
    create_user(User("Roma"), cur)
    create_user(User("Jakub"), cur)



def create_tables():
    try:

        
        print("Connected!")
        print("Tables creating...")

        for command in create_tables_command:
            cur.execute(command)
        
        print("Tables are created!")
        print("Fill airport list...")

        cur.execute(airport_codes.fill_airport_list)

        print("Filled!")
        print("Fill data...")

        # TEST
        fill_test_data(cur)

        print("Filled!")
        print("Drop tables...")

        for command in drop_tables:
            cur.execute(command)

        print("Dropped!")
        print("Close connection...")

        cur.close()
        conn.commit()


    except Exception as e:
        print(e)
        print("Something wrong!")

    finally:
        if conn is not None:
            conn.close()