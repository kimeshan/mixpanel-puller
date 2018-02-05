#! /usr/bin/env python
#
# Based on Python 2 Version by Mixpanel Inc. available at https://mixpanel.com/site_media/api/v2/mixpanel.py
#
# Copyright 2018 Jan Kyri
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import base64
import json
import urllib
import requests


class Mixpanel(object):

    ENDPOINT = 'https://data.mixpanel.com/api'
    VERSION = '2.0'

    def __init__(self, api_secret):
        self.api_secret = api_secret

    def request(self, params, http_method='GET', format='json'):
        """
            params - Extra parameters associated with method
        """
        params['format'] = format

        request_url = '/'.join([self.ENDPOINT, str(self.VERSION), 'export'])
        if http_method == 'GET':
            data = None
            request_url = request_url + '/?' + self.unicode_urlencode(params)
        else:
            data = self.unicode_urlencode(params)

        headers = {'Authorization': 'Basic {encoded_secret}'.format(
                encoded_secret=str(base64.b64encode(self.api_secret.encode()), 'utf-8'))}

        request = requests.get(request_url, headers=headers, timeout=120)
        response = request.text

        for line in response.split('\n'):
            return json.loads(line)

    def unicode_urlencode(self, params):
        """
            Convert lists to JSON encoded strings, and correctly handle any
            unicode URL parameters.
        """
        if isinstance(params, dict):
            params = list(params.items())
        for i, param in enumerate(params):
            if isinstance(param[1], list):
                params[i] = (param[0], json.dumps(param[1]),)

        return urllib.parse.urlencode(
            [(k, isinstance(v, str) and v.encode('utf-8') or v) for k, v in params]
        )


if __name__ == '__main__':
    api = Mixpanel(api_secret=os.environ['MIXPANEL_SECRET'])

    param_dict = {
        'event': ["ev1", "ev2", "ev3"],
        'from_date': "2017-01-10",
        'to_date': "2017-01-11",
    }

    data = api.request(param_dict)

    print(data)