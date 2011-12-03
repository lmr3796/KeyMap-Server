#! /usr/bin/env python
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
	def FindPlaces(self,lat,long,distance):
		arg = r'SELECT page_id FROM place WHERE distance(latitude,longitude,"'+lat+'","'+long+'")<'+str(distance)
		args = {'q':arg}
		response = self.graph.request('fql',args)
		places = []
		for place in response['data']:
			places.append(place['page_id'])
		return places
	def LoadCheckins(self,id):
		message = []
		response = self.graph.get_object(str(id)+'/checkins')
		for checkin in response['data']:
			if checkin.has_key('message') == True:
				message.append(checkin['message'])
		return message
	
