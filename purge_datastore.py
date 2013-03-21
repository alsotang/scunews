import webapp2

from google.appengine.ext import db

class PurgeDSHandler(webapp2.RequestHandler):
    def get(self):
        db.delete(db.Query(keys_only=True))
        self.response.write('Purging datastore')



app = webapp2.WSGIApplication([
    ('/purge_datastore', MainHandler)
], debug=True)