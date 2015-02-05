# README


## Introduction

These Python scripts pull data from Mixpanel using the Mixpanel API. It then extracts the relevant data and inserts it into various tables in a Postgres DB.

It consist of two main runnable scripts:

1. funnels_script.py - Pulls funnel data from Mixpanel for the previous 7 days (script to run once a week) and inserts it into the funnel transactions (funnel_trans) table.

2. raw_export_script.py - Pulls raw event data from Mixpanel for the previous day (script to run daily) and inserts it into 4 tables: 

    * *event_def*: Event definitions table
    * *event_trans*: Event transactions table.
    * *property_def*: Property definitions table.
    * *property_trans*: Property transactions table.

## How do I get set up?

### Files and libraries explained

####Description of Python script files

The two main scripts run from the following Python files:
1. Raw export: raw_export_script.py
2. Funnels: funnels_script.py

These two scripts will call:

1. mixpanel_puller.py - this is called by the scripts in order to pull the relevant data from Mixpanel.com. It contains three methods: 

    * *pull_raw_export* - pulls raw event data from Mixpanel.
    * *list_funnels* - pulls a list of funnels with funnel_id and funnel_name from Mixpanel.
    * *pull_funnels* - pulls funnel data for a given funnel_id, one of the parameters it takes.

2. to_postgres.py - this is called by the scripts to connect to the database and create tables. It contains 3 methods:
**connect_db* - accepts parameters hostname, db (database name), name (username) and pw (password) in order to connect to the Postgres database.
**create_raw_export_table* - creates tables that will be used to store raw event data exported from Mixpanel. These are the four tables event_def, property_def, property_trans and event_trans. Will only create the table if it doesn't already exist.
**create_funnel_table* - creates the funnel_trans table. Will only create the table if it doesn't already exist.

####Description of libraries used

*mixpanel_api: contains Mixpanel API Python library. Inside the folder *mixpanel_api* are the Python library API files for Mipxanel, one used for raw data export (*data_export.py*) and the other (*general.py*) for requesting funnel data. The Mixpanel API uses a slightly different syntax for requesting raw data so therefore has it's own API script which slight differs from the general

*simplejson - json module for encoding and decoding.

###Dependencies
* psycopg2: These scripts use psycopg2 which is a Python-Postgres database adaptor which allows PostgreSQL syntax to be used in Python scripts.

####How to install psycopg2
Visit [this page][install] for instructions on how to install on Linux, Windows or Mac OS X. On Linux servers or PC's running on Debian, Ubuntu and other deb-based distributions you should just need:
	sudo apt-get install python-psycopg2

Alternatively, install as a Python package using:
	pip install psycopg2

###What do I need to change before running scripts?

####Mixpanel API and Secret
The default Mixpanel API key and secret is that provided for BrighterMonday Kenya which is contained in the script files. This does not need to be changed when pulling data from Mixpanel from BrighterMonday Kenya.

To pull data using a different Mixpanel API key and secret simply change the variables:
**api_key* - Line 11 in *funnels_script.py*, Line 9 in *raw_export_script.py*.
**api_secret* - Line 12 in *funnels_script.py*, Line 10 in *raw_export_script.py*.

####Postgres database parameters
**Note: THIS MUST BE CHANGED BEFORE RUNNING ANY SCRIPT**
The following database parameter variables in each script will have to be changed in order to connect to the correct database:
**hostname*: This is the hostname such as "localhost" or "ec2-54-72-237-86.eu-west-1.compute.amazonaws.com". Change this in Line 26 in *funnels_script.py* and Line 32 in *raw_export_script.py*. 

**db*: This is the database name. Change it in Line 26 in *funnels_script.py* and Line 32 in *raw_export_script.py*.

**name*: This is the username to connect to the database, Line 26 in *funnels_script.py* and Line 32 in *raw_export_script.py*.

**pw*:This is the password to connect to the database. Change it in Line 26 in *funnels_script.py* and Line 32 in *raw_export_script.py*.

##Testing

###Limiting events for speed
Since the raw data export is pulling over 100 000 events per day, for testing purposes the script is setup to write just the first 1000 to database tables - so the sample results can be seen. This allows the script to complete much faster than it would when pulling 100 000 events and inserting 2.5 million properties.

##Once you have installed the dependencies and changed the relevant variables as described above, go ahead and run the scripts!

After running *funnels_script.py* and *raw_export_script.py*, you should see 5 tables in your Postgres database populated with the relevant columns and Mixpanel data.

[install]: http://initd.org/psycopg/docs/install.html  "How to instal Psycopg2"