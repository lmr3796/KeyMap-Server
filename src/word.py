#! /usr/bin/env python
# coding=utf-8
import json
from httplib import HTTPConnection
from urllib import urlencode
SERVER='asia.search.yahooapis.com'
WWW_PATH='/cas/v1/ke'
APP_ID = r'Tsvd7E3V34FE2Iva.bjSC0gdXsY.3KA4KMR3sRpHiradFSNyZ5wonLrX79u38NocIQCGqA--'
conn = HTTPConnection(SERVER)
response = None
def main():
	headers = {}
	data = {}
	headers['Content-type']='application/x-www-form-urlencoded'
	data['format']	= 'json'
	data['appid']	= APP_ID
	data['content']	= '我肚子好餓我想吃肉，漢堡也不錯，有義大利麵會更好'
	data['theshold']= '0'
	data['maxnum']	= '10'
	conn.request('POST', WWW_PATH, urlencode(data), headers)
	response = conn.getresponse()
 
	if response.status == 200:
		for keyword in json.loads(response.read()):
			print keyword['token']+'\t'+str(keyword['score'])
	else:
		print >> sys.stderr, response.status, response.reason
		for k,v in response.getheaders():
			print >> sys.stderr, k+':', v
	return 0;

if __name__=='__main__':
	exit(main())
