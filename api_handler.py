# coding=utf-8

import webapp2

import json

from model import PageContent
from fetch_config import config as fetch_config


class ApiHandler(webapp2.RequestHandler):
    def get(self, site_id=None, count=None):
        if (not site_id) or (not count):
            api_page = """<p>scunews API 的使用方法为：</p>
            <p>GET /api/:site_id/:count ，site_id 是站点的前缀，count 是获取的数量。返回的数据格式为 JSON。目前支持的 sites 如下：</p>
            """ + ''.join(["<p><a href=\"/api/%s/5\">\
   _site_id         GET /%s/5</a></p>" % (_site_id, _site_id) for _site_id, site_attrs in fetch_config.iteritems()])

            self.response.write(api_page)
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
