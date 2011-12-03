#! /usr/bin/env python
# coding=utf-8

import sys
import facebook
import json
from httplib import HTTPConnection
from httplib import HTTPSConnection
from urllib import urlencode

class FacebookMiner()
	def __init__(self,access_token)
		self.graph = facebook.GrapthAPI(access_token);
		return
	def FindPlaces(lat,long)
		path = 'fql?q=SELECT page_id FROM place WHERE distance(latitude,longitude,"'+lat+'","'+long+'")<200';
		return
	def LoadCheckins()
		
		return
	
access_token = sys.argv[1]
graph = facebook.GraphAPI(access_token)
friend = graph.get_object("me/friends");
friendlist = friend['data']
print friendlist[0]
maggie = friendlist[0]
checkin = graph.get_object(maggie['id']+"/checkins")
print checkin
