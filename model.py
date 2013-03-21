from google.appengine.ext import ndb

class PageContent(ndb.Model):
    site_id = ndb.StringProperty()
    url = ndb.StringProperty()
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    create_at = ndb.DateProperty(auto_now_add=True)