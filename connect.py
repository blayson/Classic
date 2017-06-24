#!/usr/bin/env python3

# for install psycopg2 for Python 3 use sudo apt-get install python3-psycopg2

import psycopg2

database_name = "test_database"
user_name = "test_master"
host_name = "test-database.cvzlexvifitu.eu-central-1.rds.amazonaws.com"
port = "5432"
passwd = "testpassword"

try:
    conn = psycopg2.connect(dbname = database_name, user = user_name, host = host_name, port = port, password = passwd)
    print("All is OK")

except Exception as e:
    print(e)
    print("I am unable to connect to the database")
