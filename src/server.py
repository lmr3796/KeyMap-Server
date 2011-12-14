import logging
import urllib
from httplib import HTTPConnection
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson as json
from facebook import GraphAPIError
from facebookMiner import FacebookMiner 

YAHOO_APP_ID = r'Tsvd7E3V34FE2Iva.bjSC0gdXsY.3KA4KMR3sRpHiradFSNyZ5wonLrX79u38NocIQCGqA--'

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('We are key map!!!!')

class YahooAPI:
    def __init__(self, app_id=None, th=None):
        YAHOO='asia.search.yahooapis.com'
        self.conn=HTTPConnection(YAHOO)
        self.data = {
            'format'    :'json',
            'appid'     :app_id,
            'content'   :'',
            'threshold'  :100,
        }

    def split(self, text):
        YAHOO_SPLIT_PATH='/cas/v1/ke'
        self.data['content'] = text.encode('utf-8')
        self.conn.connect()
        self.conn.request('POST', YAHOO_SPLIT_PATH, urllib.urlencode(self.data), {'Content-type':'application/x-www-form-urlencoded'})
        response = self.conn.getresponse()
        words = json.loads(response.read())
        result = []
        if response.status == 200:
            if words is not None:
                #for w in words:
                #    result.append((w['token'], w['score']))
                result=[(w['token'], w['score']) for w in words]
        else:
            raise NameError(str(response.status) + ' ' + response.reason)
        self.conn.close()
        return result

class FB(webapp.RequestHandler):
    
    def cloud_maker(self, lat, lng):
        global YAHOO_APP_ID
        yahoo = YahooAPI(YAHOO_APP_ID)
        tag_cloud=[]
        places = self.facebook.find_places(lat, lng)
        for pid in places:
            checkins = self.facebook.load_checkins(str(pid))
            if not checkins:
                continue
            place = sum([yahoo.split(ckin) for ckin in checkins], [])
            tag_cloud.append()
        return tag_cloud
    
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        result={'status':'1'}
        try:
            token = self.request.get('tok')
            lng = self.request.get('lng')
            lat = self.request.get('lat')
        except (TypeError, ValueError):
            result['message'] ='Bad input'
        except Exception as (errno, strerror):
            result['message'] = 'Unknown Error' 
            logging.error('Some uncaptured exceptions thrown')
            raise
        else:
            self.facebook = FacebookMiner(token) 
            try:
                tag_cloud = self.cloud_maker(lat, lng)
            except GraphAPIError:
                result['message'] = 'Facebook Graph API Error'
            except:
                result['message'] = 'Unknown Error' 
                logging.error('Some uncaptured exceptions thrown')
                raise
            else:
                result['result'] = tag_cloud
                result['status'] = '0'
        finally:
            self.response.out.write(json.dumps(result, ensure_ascii=False))

########################################WSGI#####################################
url = [
        ('/FB', FB),
        ('.+', MainPage),
        ]
application = webapp.WSGIApplication(url, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
