#Exports raw event data to Mixpanel and outputs JSON dump
from mixpanel_data_export_api import Mixpanel as Mixpanel_RawExport_API

#Method to export raw data from Mixpanel and output JSON dump
def pull (start_date,end_date,api_key,api_secret):
    api_raw_export = Mixpanel_RawExport_API(api_key,api_secret)
    print "Exporting raw data from Mixpanel. This might take a while depending on the number of events! Grab a coffee in the mean while."
    exported_data = api_raw_export.request(['export'], {
        'from_date':start_date,
        'to_date': end_date
        })    
    return exported_data


