from google.appengine.ext import ndb

import json
import logging
import time

class PageContent(ndb.Model):
    site_id = ndb.StringProperty()
    url = ndb.StringProperty()
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    create_at = ndb.DateProperty(auto_now_add=True)

    def to_json(self):
        create_at = self.create_at.strftime('%Y-%m-%d')

        j = {
            "site_id": self.site_id,
            "url": self.url,
            "title": self.title,
            "content": self.content,
            "create_at": create_at,
        }
        return j

