# Module contains methods for exporting raw event data and pulling funnel
# list and funnel data. Uses Mixpanel API (Python libary) to send pull requests.
from mixpanel_api import data_export
from mixpanel_api import general


# Method to export raw data from Mixpanel and output JSON dump
def pull_raw_export(start_date, end_date, api_key, api_secret):
    api_raw_export = data_export.Mixpanel(api_key,api_secret)
    print("""Exporting raw data from Mixpanel. This might take a while depending on the number of events! 
             Grab a coffee in the meanwhile.""")

    exported_data = api_raw_export.request(['export'], {
        'from_date': start_date,
        'to_date': end_date
        })    

    return exported_data


# Pull list of funnels and return it
def list_funnels(api_key, api_secret):
    api = general.Mixpanel(api_key, api_secret)
    funnel_list = api.request(["funnels/list"], {})

    return funnel_list
#  Format:[{"funnel_id": 989319, "name": "Random"}] - array of objects/dicts


# Use list of funnels to pull each funnel and it's details
def pull_funnels(funnel_id, length, interval, from_date, to_date, api_key, api_secret):
    api = general.Mixpanel(api_key, api_secret)
    print("Data for funnel ID "+str(funnel_id)+" requested from Mixpanel.com...")
    funnel_data = api.request(["funnels"], {
        "funnel_id": funnel_id,
        "length": length,
        "interval": interval,
        "from_date": from_date,
        "to_date": to_date
        })

    return funnel_data

