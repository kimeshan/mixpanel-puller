#This is the main class
from datetime import date,timedelta, datetime
import pull_funnels, raw_export,mixpanel_to_postgres
import json
import sys,ast
import psycopg2

#OneAfricaMedia Mixpanel key
api_key = "215044064e1ec9964ed91c25bf628e73"
api_secret = "0067413ce68849370bac6b47d34c9f65"

#To log time taken to export all raw event data for the day
timing_file = open('timing.txt', 'w')

#More logs
raw_export_data_file = open('data.txt','w')
#mixpanel_data_file = open('mixpanel_sample.txt','r')

"""
#Export raw event data from Mixpanel
print "Exporting raw event data from Mixpanel..."
export_start_date = "2015-01-30"
export_end_date = "2015-01-30"
timing_file.write("Started exporting raw data:"+str(datetime.now())+"\n")
event_dicts = raw_export.pull(export_start_date, export_end_date,api_key,api_secret)
#event_dicts = ast.literal_eval(mixpanel_data_file.read())
number_of_events = len(event_dicts)
timing_file.write("Completed exporting "+str(number_of_events)+" events at:"+str(datetime.now())+"\n")
raw_export_data_file.write(unicode(event_dicts))
raw_export_data_file.close()
print "Raw data export completed successfully!"
print str(len(event_dicts))+" event(s) exported."
"""

#Pull funnel list
print "Pulling funnel list, request sent to Mixpanel.com:"
funnel_list = pull_funnels.listFunnels(api_key,api_secret)

#Set parameters to pull funnel data
length  = 60
interval = 1
seven_days_ago = date.today()-timedelta(days=7)
yesterday = date.today()-timedelta(days=1)

#Database operations
#1. Connect to Postgres database
hostname = "localhost"
db= "postgres"
name = "postgres"
pw = "test"

con,cur = mixpanel_to_postgres.connect_db(hostname,db,name,pw)

#2. Create required tables if they do not yet exist
mixpanel_to_postgres.create_db_tables(con,cur)

#3. Update tables

#timing_file.write("Number of events writing to postgres: "+str(max_events)+"\n")

try:   
    #Update funnel tables
    for each in funnel_list:
        funnel_id,funnel_name = each["funnel_id"],each["name"]        
        funnel_data = pull_funnels.pullFunnels(funnel_id,length,interval,seven_days_ago,yesterday,api_key,api_secret);
        #print json.dumps(funnel_data)
        for date in funnel_data["meta"]["dates"]:
            print "Current date is:" + date
            date_data = funnel_data["data"][date]
            completion = funnel_data["data"][date]["analysis"]["completion"]
            starting_amount = funnel_data["data"][date]["analysis"]["starting_amount"]
            steps = funnel_data["data"][date]["analysis"]["steps"]
            worst = funnel_data["data"][date]["analysis"]["worst"]
            print "Comp:"+str(completion)+"\nStarting amt: "+str(starting_amount)+"\nSteps:"+str(steps)+"W:"+str(worst)
            #Loop through steps, cater for max of 4 steps (to match database schema)
            step_data = [["",0,0.0,0.0],["",0,0.0,0.0],["",0,0.0,0.0],["",0,0.0,0.0]] #Cater for a maximum of 4 steps
            steps_dicts = date_data["steps"]
            for step in range(steps):
                step_data[step] = [steps_dicts[step]["goal"],steps_dicts[step]["count"],
                                   steps_dicts[step]["overall_conv_ratio"],steps_dicts[step]["step_conv_ratio"]]
            print "Array of data for each step:"
            print step_data
            #Insert row for this date and funnel into table
            cur.execute("INSERT INTO funnel_trans(funnel_id, funnel_name,from_date,to_date, completion,starting_amount,steps,\
                        worst, step_1_goal, step_1_count, step_1_overall_conv_ratio, step_1_step_conv_ratio,\
                        step_2_goal, step_2_count, step_2_overall_conv_ratio, step_2_step_conv_ratio,\
                        step_3_goal, step_3_count, step_3_overall_conv_ratio, step_3_step_conv_ratio,\
                        step_4_goal, step_4_count, step_4_overall_conv_ratio, step_4_step_conv_ratio) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                        (funnel_id,funnel_name,date,date,completion,starting_amount,steps,worst,step_data[0][0],step_data[0][1],
                        step_data[0][2],step_data[0][3],step_data[1][0],step_data[1][1],step_data[1][2],step_data[1][3],
                        step_data[2][0],step_data[2][1],step_data[2][2],step_data[2][3],
                        step_data[3][0],step_data[3][1],step_data[3][2],step_data[3][3]))
    con.commit()   
    #Update event definition and event transaction table
    """
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
            print current_progress_percent
    timing_file.write("Completed property table writing at: "+str(datetime.now())+"\n")       
    con.commit()
    timing_file.write("Commited to database at: "+str(datetime.now())+"\n")
    """

    

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
