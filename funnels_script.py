#Script to pull funnel data and write to funnel_trans (funnel transacations)
#table on Postgres DB
from datetime import date,timedelta, datetime
import mixpanel_puller,to_postgres
import json
import psycopg2

print "Starting script to pull funnel data from Mixpanel and write to database..."

#OneAfricaMedia Mixpanel key
api_key = "INSERT YOUR MIXPANEL KEY HERE"
api_secret = "INSERT YOUR MIXPANEL SECRET HERE"

#Pull funnel list
print "Pulling funnel list, request sent to Mixpanel.com:"
funnel_list = mixpanel_puller.list_funnels(api_key,api_secret)

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
con,cur = to_postgres.connect_db(hostname,db,name,pw)

#2.Create funnel_trans table if it does not already exist
to_postgres.create_funnel_table(con,cur)

#3.Insert funnel data into funnel_trans table
try:   
    #Update funnel_trans table
    print "Writing funnel data to funnel_trans table.."
    for each in funnel_list:
        funnel_id,funnel_name = each["funnel_id"],each["name"]        
        funnel_data = mixpanel_puller.pull_funnels(funnel_id,length,interval,seven_days_ago,yesterday,api_key,api_secret);
        print "Funnel data received.\n"
        for date in funnel_data["meta"]["dates"]:
            date_data = funnel_data["data"][date]
            completion = funnel_data["data"][date]["analysis"]["completion"]
            starting_amount = funnel_data["data"][date]["analysis"]["starting_amount"]
            steps = funnel_data["data"][date]["analysis"]["steps"]
            worst = funnel_data["data"][date]["analysis"]["worst"]
            #Loop through steps, cater for max of 4 steps (to match database schema)
            step_data = [["",0,0.0,0.0],["",0,0.0,0.0],["",0,0.0,0.0],["",0,0.0,0.0]] #Cater for a maximum of 4 steps
            steps_dicts = date_data["steps"]
            for step in range(steps):
                step_data[step] = [steps_dicts[step]["goal"],steps_dicts[step]["count"],
                                   steps_dicts[step]["overall_conv_ratio"],steps_dicts[step]["step_conv_ratio"]]
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
    print "funnel_trans table updated successfully."

except psycopg2.DatabaseError, e:
    #If database error, let's rollback any changes.
    if con:
        con.rollback()
    print 'Error %s' % e
    sys.exit(1)

finally:
    if con:
        con.close
        print "Connection to database closed."        
