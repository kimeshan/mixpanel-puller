#Inserts Mixpanel data into Postgres DB and tables
import psycopg2

#Method connects to a Postgres database using the psycopg2 module db adapter
def connect_db (hostname,db,name,pw):
    print "Connecting to PostgreSQL database..."
    con = None
    try:
        #Try to connect to the database, store connection object in 'con'
        con = psycopg2.connect(host=hostname,database=db, user=name, password=pw)
        #Get the cursor object from connection, used to traverse records
        cur = con.cursor()
        #Execute statement is used to run SQL statements, here we check the Postgres version
        cur.execute('SELECT version()')
        #Fetch the record (just one record that we selected)
        ver = cur.fetchone()
        print "Successfully connected! Version information:"
        print ver
        return con,cur
    
    except psycopg2.DatabaseError, e:
        #If database error, let's rollback any changes.
        if con:
            con.rollback()
            con.close()
        print 'Error %s' % e
        sys.exit(1)

def create_db_tables (con,cur):
    try:
        #Creating tables
        cur.execute("CREATE TABLE IF NOT EXISTS event_def (event_id serial PRIMARY KEY , event_name VARCHAR(50))")
        cur.execute("CREATE TABLE IF NOT EXISTS property_def (property_id serial PRIMARY KEY, property_name VARCHAR(50), event_id integer REFERENCES event_def);")
        cur.execute("CREATE TABLE IF NOT EXISTS property_trans (trans_id bigserial PRIMARY KEY, property_value text, property_id integer REFERENCES property_def);")
        cur.execute("CREATE TABLE IF NOT EXISTS event_trans (trans_id serial PRIMARY KEY, event_id integer REFERENCES event_def, timestamp bigint);")
        cur.execute("CREATE TABLE IF NOT EXISTS funnel_trans (trans_id serial PRIMARY KEY, funnel_id integer,funnel_name VARCHAR(200),from_date date,to_date date,\
                    completion integer,starting_amount integer,steps integer,worst integer,\
                    step_1_goal VARCHAR(50),step_1_count integer,step_1_overall_conv_ratio decimal, step_1_step_conv_ratio decimal,\
                    step_2_goal VARCHAR(50),step_2_count integer,step_2_overall_conv_ratio decimal, step_2_step_conv_ratio decimal,\
                    step_3_goal VARCHAR(50),step_3_count integer,step_3_overall_conv_ratio decimal, step_3_step_conv_ratio decimal,\
                    step_4_goal VARCHAR(50),step_4_count integer,step_4_overall_conv_ratio decimal, step_4_step_conv_ratio decimal);")
        print "Done creating tables."
        con.commit()
    except psycopg2.DatabaseError, e:
        #If database error, let's rollback any changes.
        if con:
            con.rollback()
            con.close()
        print 'Error %s' % e
        sys.exit(1)

    
