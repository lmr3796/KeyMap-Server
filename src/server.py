from httplib import HTTPConnection
from urllib import urlencode
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson as json
from facebook import GraphAPIError
from facebookMiner import FacebookMiner 
class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')

class FB(webapp.RequestHandler):
    def split(self, text):
        APP_ID = r'Tsvd7E3V34FE2Iva.bjSC0gdXsY.3KA4KMR3sRpHiradFSNyZ5wonLrX79u38NocIQCGqA--'
        data = {
            'format'    :'json',
            'appid'     :APP_ID,
            'content'   :text,
            'theshold'  :'0',
            'maxnum'    :'3',
        }
        YAHOO='asia.search.yahooapis.com'
        YAHOO_PATH='/cas/v1/ke'
        conn=HTTPConnection(YAHOO)
        conn.request('POST', YAHOO_PATH, urlencode(data), {'Content-type':'application/x-www-form-urlencoded'})
        response = conn.getresponse()
        result = []
        if response.status == 200:
            for keyword in json.loads(response.read()):
                result.append(keyword['token'])
        conn.close()
        return result

    def cloud_maker(self, lat, lng):
        tag_clouds={}
        try:
            places = self.facebook.find_places(lat, lng)
            for pid in places:
                #tag_clouds[pid] = self.facebook.load_checkins(str(pid)) 
                checkins = self.facebook.load_checkins(str(pid))
                if not checkins:
                    continue
                tag_clouds[pid] = []
                for ckin in checkins:
                    # TODO: solve this fucking encode error
                    tag_clouds[pid].append(self.split(ckin))
                    #tag_clouds[pid].append(ckin)
        except(GraphAPIError):
            return {'status':'1', 'message':'Facebook GraphAPIError'}
        return {'status':'0', 'result':tag_clouds}
    
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        try:
            token = self.request.get('tok')
            lng = self.request.get('lng')
            lat = self.request.get('lat')
        except (TypeError, ValueError):
            result = {'status':'1', 'message':'Bad input'}
        
        self.facebook = FacebookMiner(token) 
        result = self.cloud_maker(lat, lng)
        #result = {'status':'1', 'message':'UnknownError'}
        result = json.dumps(result ,ensure_ascii=False)
        self.response.out.write(result)


url = [
        ('/FB', FB),
        ('.+', MainPage),
        ]
application = webapp.WSGIApplication(
        url,
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
