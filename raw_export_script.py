#This is the main class
from datetime import date,timedelta, datetime
import mixpanel_puller, to_postgres
import json
import sys,ast
import psycopg2

#OneAfricaMedia Mixpanel key
api_key = "INSERT YOUR MIXPANEL KEY HERE"
api_secret = "INSERT YOUR MIXPANEL SECRET HERE"

#To log time taken to export all raw event data for the day
timing_file = open('timing.txt', 'w')

#More logs
#mixpanel_data_file = open('mixpanel_sample.txt','r')

#Export raw event data from Mixpanel
print "Exporting raw event data from Mixpanel..."
export_start_date = date.today()-timedelta(days=1) #Yesterday
export_end_date = date.today()-timedelta(days=1) #Yesterday
timing_file.write("Started exporting raw data:"+str(datetime.now())+"\n")
event_dicts = mixpanel_puller.pull_raw_export(export_start_date, export_end_date,api_key,api_secret)
#event_dicts = ast.literal_eval(mixpanel_data_file.read())
number_of_events = len(event_dicts)
timing_file.write("Completed exporting "+str(number_of_events)+" events at:"+str(datetime.now())+"\n")
print "Raw data export completed successfully!"
print str(len(event_dicts))+" event(s) exported."

#Database operations
#1. Connect to Postgres database
hostname = "localhost"
db= "postgres"
name = "postgres"
pw = "test"
con,cur = to_postgres.connect_db(hostname,db,name,pw)

#2. Create required tables if they do not yet exist
to_postgres.create_raw_export_tables(con,cur)

#3. Update tables
try:   
    #Update event definition and event transaction table    
    print "Updating events tables..."
    for each_event in event_dicts:
        event_name = each_event["event"]
        #Update event def table
        cur.execute("SELECT exists(SELECT * FROM event_def where event_name=%s);",(event_name,))
        if not(cur.fetchone()[0]): #If not found in table, add the event.
            cur.execute("INSERT INTO event_def(event_name) VALUES(%s);",(event_name,))
        #Update event transaction table
        cur.execute("SELECT event_id FROM event_def WHERE event_name=%s;",(event_name,)) #Select event id
        event_id = cur.fetchone()[0] #Store event_id
        timestamp = each_event["properties"]["time"] #Store timestamp
        cur.execute("INSERT INTO event_trans(event_id,timestamp) VALUES(%s,%s);",(event_id,timestamp))
    timing_file.write("Completed event table writing and started properties at: "+str(datetime.now())+"\n")
    con.commit()    
        
    event_count = 0
    current_progress_percent = 0
    print "Updating property tables..."
    #Update property definition and property transaction table
    print "Percentage completed..."
    for each_event in event_dicts:
        event_count+=1
        cur.execute("SELECT event_id FROM event_def WHERE event_name=%s",(each_event["event"],))
        event_id = cur.fetchone()[0]  
        properties = each_event["properties"] #Properties is a dictionary of various key-values (properties)
        property_trans_list = []
        #Loop through each property            
        for key in properties:
            key_formatted = key.lstrip('$').replace(' ','_').lower() #Remove spaces and $ sign from beginning of keys
            #Update property def table
            cur.execute("SELECT exists(SELECT * FROM property_def where property_name=%s AND event_id=%s);",(key_formatted,event_id))
            if not(cur.fetchone()[0]): #If not found in table, add the property name and event id
                cur.execute("INSERT INTO property_def(property_name, event_id) VALUES(%s,%s);",(key_formatted,event_id))
            #Update property transaction table
            #Let's try multi row insertion here              
            cur.execute("SELECT property_id FROM property_def WHERE property_name=%s AND event_id=%s;",(key_formatted,event_id)) #Get property id
            property_id = cur.fetchone()[0]
            #Let's batch them by properties per event, so insert all the property rows for each event using one "INSERT"
            property_trans_list.append([unicode(properties[key]),property_id])
        property_trans_tuple = tuple(property_trans_list)
        #Execute the insertion of all properties for this event
        cur.executemany("INSERT INTO property_trans(property_value,property_id) VALUES(%s,%s);", property_trans_tuple)
        if ((event_count/1.00)/number_of_events)*100  > 5+current_progress_percent:
            current_progress_percent = ((event_count/1.00)/number_of_events)*100
            timing_file.write("Progress bar: "+str(current_progress_percent)+"%\n")
            print str(int(current_progress_percent))+"%..."
    timing_file.write("Completed property table writing at: "+str(datetime.now())+"\n")       
    con.commit()
    timing_file.write("Commited to database at: "+str(datetime.now())+"\n") 

    print "Update complete and changes committed to database."
    
except psycopg2.DatabaseError, e:
    #If database error, let's rollback any changes.
    if con:
        con.rollback()
    print 'Error %s' % e
    timing_file.write("Error encountered at: "+str(datetime.now())+"\n")
    timing_file.close()
    sys.exit(1)

finally:
    if con:
        con.close
        print "Connection to database closed."
        timing_file.write("Connection to database closed at: "+str(datetime.now())+"\n")
        timing_file.close()              
