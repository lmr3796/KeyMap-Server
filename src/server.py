import logging
import urllib
from httplib import HTTPConnection
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson as json
from facebook import GraphAPIError
from facebookMiner import FacebookMiner 

YAHOO_APP_ID1 = r'Tsvd7E3V34FE2Iva.bjSC0gdXsY.3KA4KMR3sRpHiradFSNyZ5wonLrX79u38NocIQCGqA--'
YAHOO_APP_ID2 = r'Gv5SAfHV34F7pX6ttIe8G9.2EeHW50BjkGSHX7LO9geKHMBYALrJ9L4ujjsdDvDRAeEaeQ--'

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('We are key map!!!!')

class YahooAPI:
    def __init__(self, app_id=None, th=None):
        self.server='asia.search.yahooapis.com'
        #self.conn=HTTPConnection(YAHOO)
        self.data = {
            'format'    :'json',
            'appid'     :app_id,
            'content'   :'',
            'threshold' :0,
        }

    def split(self, text):
        SPLIT_PATH='/cas/v1/ke'
        self.data['content'] = text.encode('utf-8')
        response = urlfetch.fetch('http://'+self.server+SPLIT_PATH, urllib.urlencode(self.data), 
                                    urlfetch.POST,{'Content-type':'application/x-www-form-urlencoded'})
        #self.conn.connect()
        #self.conn.request('POST', YAHOO_SPLIT_PATH, urllib.urlencode(self.data), {'Content-type':'application/x-www-form-urlencoded'})
        #response = self.conn.getresponse()
        if response.status_code == 200:
            if response.content_was_truncated:
                raise NameError('Content was truncated')
            words = response.content
            words = json.loads(words)
            result = [] 
            if words is not None:
                result = [(w['token'], w['score']) for w in words]
        else:
            raise NameError(str(response.status) + ' ' + response.reason)
        #self.conn.close()
        return result

class FB(webapp.RequestHandler):
    def key_word_group(self, kw_list):
        limit = (4, 8, 16)
        result = [[],[],[]]
        for kw in kw_list:
            for i in range(0, len(limit)):
                if len(result[i]) < limit[i]:
                    result[i].append(kw)
                    break
        return result

    def cloud_maker(self, lat, lng):
        global YAHOO_APP_ID2
        yahoo = YahooAPI(YAHOO_APP_ID2)
        tag_cloud=[]
        places = self.facebook.find_places(lat, lng)
        for p in places:
            checkins = self.facebook.load_checkins(str(p['pid']))
            if not checkins:
                continue
            all_checkin = '\n'.join([ckin for ckin in checkins])
            #logging.info(unicode(all_checkin).encode('utf-8'))
            kw = yahoo.split(all_checkin)
            kw = sorted(kw, key=lambda keyword: keyword[1], reverse=True)
            kw = self.key_word_group([k[0] for k in kw])
            tag_cloud.append({'id':str(p['pid']), 'name':p['name'],
                                'lat': p['lat'], 'lng': p['long'], 'kw':kw})
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
        except Exception as e:
            result['message'] = 'Unknown Error' 
            logging.error(str(e))
        else:
            self.facebook = FacebookMiner(token) 
            try:
                tag_cloud = self.cloud_maker(lat, lng)
            except GraphAPIError:
                result['message'] = 'Facebook Graph API Error'
            except Exception as e:
                result['message'] = 'Unknown Error' 
                logging.error(str(e))
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
