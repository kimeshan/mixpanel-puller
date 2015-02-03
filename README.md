# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
Python scripts that pull data from Mixpanel using the Mixpanel API. Extracts relevant data and inserts into Postgres DB.

* Version
In development

* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
Mixpanel API key and secret is currently stored in playbox.py. All other modules and methods are called from here.

* Configuration
Mixpanel Python API libraries: mixpanel_api.py and mixpanel_data_export.py
Modules pulling Mixpanel data: pull_funnels.py and raw_export.py

* Dependencies
Uses psycopg2 as Python-Postgres adaptor

* Database configuration
playbox.py is currently configured to connect to localhost Postgres database server. Change host, db, user and pw (password) parameters to connect to a different database. 

* How to run tests
Loop through first 1000 events instead of all 100 000+ pulled on a daily basis for quicker testing. Just change for loops to run through range 0:1000 of event_dicts instead of the all events.

* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact