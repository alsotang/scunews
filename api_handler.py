# coding=utf-8

import webapp2
import jinja2
import os

import json

from model import PageContent
from fetch_config import config as fetch_config

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class ApiHandler(webapp2.RequestHandler):
    def get(self, site_id=None, count=None):
        if (not site_id) or (not count):
            template_attrs = {
                "fetch_config": fetch_config,
                "title": "API",
            }
            api_template = jinja_environment.get_template('api_page.html')
            self.response.write(api_template.render(template_attrs))
            return

        count = int(count)
        results = PageContent.query(PageContent.site_id == site_id).order(PageContent.create_at).fetch(count)
        results = map(lambda x: x.to_json(), results)
        results = json.dumps(results, ensure_ascii=False)
        self.response.write(results)


app = webapp2.WSGIApplication([
    (r'/api', ApiHandler),
    (r'/api/(.*)/(.*)', ApiHandler)
], debug=True)
