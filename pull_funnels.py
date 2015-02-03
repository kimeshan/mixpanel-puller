#Pull list of funnels and return it
from mixpanel_api import Mixpanel as Mixpanel_API
def listFunnels (api_key, api_secret):
    api = Mixpanel_API(api_key, api_secret)
    funnel_list = api.request(["funnels/list"],{})
    return funnel_list
# Format:[{"funnel_id": 989319, "name": "Random"}] - array of objects/dicts

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


