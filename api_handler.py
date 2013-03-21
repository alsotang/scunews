import webapp2

import json
import logging

from model import PageContent

class ApiHandler(webapp2.RequestHandler):
    def get(self, site_id=None, count=None):
        if (not site_id) or (not count):
            self.response.write('How to use this API')
            return

        count = int(count)
        results = PageContent.query(PageContent.site_id == site_id).fetch(count)
        results = map(lambda x: x.to_json(), results)
        results = json.dumps(results, ensure_ascii=False)
        self.response.write(results)
        

app = webapp2.WSGIApplication([
    (r'/api', ApiHandler),
    (r'/api/(.*)/(.*)', ApiHandler)
], debug=True)

