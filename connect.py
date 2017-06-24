#!/usr/bin/env python3

# for install psycopg2 for Python 3 use sudo apt-get install python3-psycopg2

import psycopg2

database_name = "test_database"
user_name = "test_master"
host_name = "test-database.cvzlexvifitu.eu-central-1.rds.amazonaws.com"
port = "5432"
passwd = "testpassword"

create_table = """ 
			CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """

drop_table = """
			DROP TABLE vendors
			"""

show_tables = """ 
			SELECT table_name FROM information_schema.tables
       		WHERE table_schema = 'public' 
       	"""

try:
    conn = psycopg2.connect(dbname = database_name, user = user_name, host = host_name, port = port, password = passwd)
    cur = conn.cursor()

    cur.execute(create_table)

    cur.execute(show_tables)
    for table in cur.fetchall():
    	print(table)

    cur.execute(drop_table)

    cur.execute(show_tables)
    for table in cur.fetchall():
    	print(table)
    else:
    	print("OOOps")

    cur.close()
    conn.commit()

    print("All is OK")

except Exception as e:
    print(e)
    print("I am unable to connect to the database")

finally:
    if conn is not None:
        conn.close()
