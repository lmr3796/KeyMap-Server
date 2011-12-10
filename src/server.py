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
    def cloud_maker(self, lat, lng):
        tag_clouds={}
        try:
            self.facebook.find_places(lat, lng)
        except(GraphAPIError):
            return {'status':'1', 'message':'Facebook GraphAPIError'}
        return {'status':'0', 'result':tag_clouds}
    
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        try:
            token = self.request.get('tok')
            lng = self.request.get('lng')
            lat = self.request.get('lat')
            self.facebook = FacebookMiner(token) 
            result = self.cloud_maker(lat, lng)
        except (TypeError, ValueError):
            result = {'status':'1', 'message':'Bad input'}
        self.response.out.write(json.dumps(result ,ensure_ascii=False))




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
