# Postgres database methods to connect to DB and create various tables
import psycopg2
import sys


# Method connects to a Postgres database using the psycopg2 module db adapter
def connect_db(hostname, db, name, pw):
    print("Connecting to database at "+str(hostname)+"...")
    con = None
    try:
        # Try to connect to the database, store connection object in 'con'
        con = psycopg2.connect(host=hostname,database=db, user=name, password=pw)
        # Get the cursor object from connection, used to traverse records
        cur = con.cursor()
        print("Successfully connected to database!\n")
        return con, cur
    
    except psycopg2.DatabaseError as e:
        # If database error, let's rollback any changes.
        if con:
            con.rollback()
            con.close()
        print('Error %s' % e)
        sys.exit(1)


def create_raw_export_tables(con, cur):
    try:
        # Creating tables
        print("Creating tables that do not exist already...")
        cur.execute("CREATE TABLE IF NOT EXISTS event_def (event_id serial PRIMARY KEY , event_name VARCHAR(50))")
        cur.execute("CREATE TABLE IF NOT EXISTS property_def (property_id serial PRIMARY KEY, property_name VARCHAR(50), event_id integer REFERENCES event_def);")
        cur.execute("CREATE TABLE IF NOT EXISTS property_trans (trans_id bigserial PRIMARY KEY, property_value text, property_id integer REFERENCES property_def);")
        cur.execute("CREATE TABLE IF NOT EXISTS event_trans (trans_id serial PRIMARY KEY, event_id integer REFERENCES event_def, timestamp bigint);")
        con.commit()
        print("Done.")

    except psycopg2.DatabaseError as e:
        # If database error, let's rollback any changes.
        if con:
            con.rollback()
            con.close()
        print('Error %s' % e)
        sys.exit(1)


def create_funnel_table(con, cur):
    try:
        # Creating funnel_trans (funnel transaction) table: 25 columns
        print("Creating funnel_trans if it doesn't already exist...")
        cur.execute("CREATE TABLE IF NOT EXISTS funnel_trans (trans_id SERIAL PRIMARY KEY, funnel_id INTEGER, \
                    funnel_name VARCHAR(200), from_date DATE, to_date DATE, completion INTEGER, \
                    starting_amount INTEGER, steps INTEGER, worst INTEGER, \
                    step_1_goal VARCHAR(50), step_1_count INTEGER, step_1_overall_conv_ratio DECIMAL, \
                    step_1_step_conv_ratio DECIMAL, step_2_goal VARCHAR(50), step_2_count INTEGER, \
                    step_2_overall_conv_ratio DECIMAL, step_2_step_conv_ratio DECIMAL, step_3_goal VARCHAR(50), \
                    step_3_count INTEGER, step_3_overall_conv_ratio DECIMAL, step_3_step_conv_ratio DECIMAL,\
                    step_4_goal VARCHAR(50), step_4_count INTEGER, step_4_overall_conv_ratio DECIMAL, \
                    step_4_step_conv_ratio DECIMAL);")
        con.commit()
        print("Done.")

    except psycopg2.DatabaseError as e:
        # If database error, let's rollback any changes.
        if con:
            con.rollback()
            con.close()
        print('Error %s' % e)
        sys.exit(1)

