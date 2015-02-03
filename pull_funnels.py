#Pull list of funnels and return it
from mixpanel_api import Mixpanel as Mixpanel_API
def listFunnels (api_key, api_secret):
    api = Mixpanel_API(api_key, api_secret)
    funnel_list = api.request(["funnels/list"],{})
    return funnel_list
# Format:[{"funnel_id": 989319, "name": "Random"}] - array of objects/dicts

"""
#Print list of funnels
print "Listing funnels with name and ID:"
for each in funnels:
    print each["name"]
    print each["funnel_id"]
"""

#Use list of funnels to pull each funnel and it's details
def pullFunnels (funnel_id,length,interval,from_date,to_date,api_key,api_secret):
    api = Mixpanel_API(api_key, api_secret)
    funnel_data = api.request(["funnels"], {
        "funnel_id":funnel_id,
        "length":length,
        "interval":interval,
        "from_date":from_date,
        "to_date":to_date
        })
    return funnel_data

"""
#Print data for each funnel
seven_days_ago = date.today()-timedelta(days=2)
yesterday = date.today()-timedelta(days=1)
for each in funnels:
    funnel_data = pullFunnels(each["funnel_id"],60,1,seven_days_ago,yesterday)
    print json.dumps(funnel_data)

#Trying to make sense of funnel data
for eachFunnel in funnels:
    funnel_data = pullFunnels(eachFunnel["funnel_id"],60,1,seven_days_ago,yesterday)
    print "Analysing funnel for: "+eachFunnel["name"]+"..."
    print "From date:"
    [from_date_funnel, to_date_funnel] = funnel_data["meta"]["dates"]
    print from_date_funnel
    print "To date:"
    print to_date_funnel
"""
