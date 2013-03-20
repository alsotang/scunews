from google.appengine.ext import db

class PageContent(db.Model):
	site_id = db.StringProperty()
	url = db.StringProperty()
	title = db.StringProperty()
	content = db.TextProperty()