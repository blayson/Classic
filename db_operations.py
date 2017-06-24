#!/usr/bin/env python3

# for install psycopg2 for Python 3 use sudo apt-get install python3-psycopg2

from classy import *
import airport_codes
import psycopg2

database_name = "test_database"
user_name = "test_master"
host_name = "test-database.cvzlexvifitu.eu-central-1.rds.amazonaws.com"
port = "5432"
passwd = "testpassword"

create_tables_command = (
			"""
				CREATE TABLE Users (
					user_id SERIAL PRIMARY KEY,
					name VARCHAR (50) NOT NULL,
					surname VARCHAR (50) NOT NULL,
					age INTEGER NOT NULL,
					foto BYTEA,
					contact VARCHAR (100)
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
		
def create_user(user, cur):
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
	return user_id

def create_trip(trip, cur):
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
	return trip_id

def create_flight(flight, cur):
	add_flight = (
			"""
			INSERT INTO Flights (from_tmsp, to_tmsp, cost, duration)
			VALUES (%s, %s, %s, %s)
			"""
		)
	flight_info = (flight.from_tmsp, flight.to_tmsp, flight.cost, flight.duration)
	cur.execute(add_flight, flight_info)


def get_trips(cur, dest, date, time = None):
	trips = []

	if time:
		select_trips = """ SELECT * FROM Trips WHERE dest = %s AND date = %s AND time = %s """
		trip_info = (dest, date, time)
	else:
		select_trips = """ SELECT * FROM Trips WHERE dest = %s AND date = %s """
		trip_info = (dest, date)

	cur.execute(select_trips)
	trip_list = cur.fetchall()
	for trip in trips_list:
		new_trip = Trip(trip[1], trip[2], trip[3], trip[4], trip[5])
		new_trip.id = trip[0]
		trips.append(new_trip)

	return trips

def get_partic(cur, trip):
	users = []
	select_trip = """ SELECT * FROM Trips WHERE dest = %s AND date = %s AND time BETWEEN %s AND %s """
	trip_info = (trip.dest, trip.date, trip.time-trip.time_diff, trip.time + trip.time_diff)

	cur.execute(select_trip, trip_info)
	trips = cur.fetchall()

	select_users = """ SELECT 
						User.name,
						User.surname,
						User.age,
						User.foto,
						User.contact
						FROM User
						INNER JOIN User_Trip ON User_Trip.user_id = User.user_id
						INNER JOIN Trip ON User_Trip.trip_id = %s """
	for trip in trips:
		cur.execute(select_users, (trip[0],))
		users = cur.fetchall()
		for user in users:
			new_user = User(user[0], user[1], user[2], user[3], user[4])
			users.append(new_user)

	return users

def fill_test_data(cur):
	create_user(User("Vova"), cur)
	create_user(User("Andrii"), cur)
	create_user(User("Lecha"), cur)
	create_user(User("Andrei"), cur)
	create_user(User("Pavel"), cur)
	create_user(User("Roma"), cur)
	create_user(User("Jakub"), cur)

def create_tables():
	try:
	    conn = psycopg2.connect(dbname = database_name, user = user_name, host = host_name, port = port, password = passwd)
	    cur = conn.cursor()

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

if __name__ == '__main__':
	create_tables()
