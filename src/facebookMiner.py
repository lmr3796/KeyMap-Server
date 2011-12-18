# /usr/bin/env python
# coding=utf-8

import sys
import facebook
import json
from httplib import HTTPConnection
from httplib import HTTPSConnection
from urllib import urlencode

class FacebookMiner(object):
    def __init__(self,access_token):
        self.graph = facebook.GraphAPI(access_token);
        return

    def find_places(self,lat,lng,distance=200):
        arg = r'SELECT page_id, latitude, longitude, name FROM place WHERE distance(latitude,longitude,"'+lat+'","'+lng+'")<'+str(distance)
        args = {'q':arg}
        response = self.graph.request('fql',args)
        places = []
        for place in response['data']:
            result = {}
            result['pid'] = place['page_id']
            result['lat'] = place['latitude']
            result['long'] = place['longitude']
            result['name'] = place['name']
            places.append(result)
        return places

    def load_checkins(self, checkin_id):
        message = []
        response = self.graph.get_object(checkin_id+'/checkins')
        for checkin in response['data']:
            if checkin.has_key('message') == True:
                message.append(checkin['message'])
        return message

